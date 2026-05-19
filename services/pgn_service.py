from __future__ import annotations

from io import StringIO

import chess
import chess.engine
import chess.pgn
import chess.svg

from config import STOCKFISH_PATH
from services.engine_service import (
    analyze_position,
    classify_move,
    format_eval,
    label_class,
)
from services.explanation_service import build_explanation


BOARD_COLORS = {
    "square light": "#f0c98f",
    "square dark": "#a66b3d",
    "square light lastmove": "#d8dda2",
    "square dark lastmove": "#8fb66f",
    "margin": "#2b1b12",
    "inner border": "#2b1b12",
    "outer border": "#2b1b12",
    "coord": "#fffaf1",
    "arrow blue": "#2563ebcc",
    "arrow green": "#2f7d46cc",
}


def make_board_svg(
    board: chess.Board,
    played_move: chess.Move | None,
    best_move: chess.Move | None,
    perspective: chess.Color,
) -> str:
    arrows = []

    if played_move:
        arrows.append(
            chess.svg.Arrow(
                played_move.from_square,
                played_move.to_square,
                color="#2563eb",
            )
        )

    if best_move and played_move != best_move:
        arrows.append(
            chess.svg.Arrow(
                best_move.from_square,
                best_move.to_square,
                color="#16a34a",
            )
        )

    squares = []

    if played_move:
        squares.extend([played_move.from_square, played_move.to_square])

    if best_move:
        squares.extend([best_move.from_square, best_move.to_square])

    return chess.svg.board(
        board=board,
        size=420,
        coordinates=True,
        orientation=perspective,
        arrows=arrows,
        squares=squares,
        colors=BOARD_COLORS,
    )


def analyze_pgn(pgn_text: str, depth: int, perspective_name: str = "White") -> dict:
    game = chess.pgn.read_game(StringIO(pgn_text))

    if game is None:
        raise ValueError("Invalid PGN. Paste a valid PGN or move list.")

    board = game.board()
    moves = []
    perspective = chess.BLACK if perspective_name == "Black" else chess.WHITE

    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    try:
        for index, node in enumerate(game.mainline()):
            board_before = board.copy()
            side_to_move = board_before.turn
            side = "White" if side_to_move == chess.WHITE else "Black"

            played_move = node.move
            played_san = board_before.san(played_move)

            best_move, before_cp = analyze_position(engine, board_before, depth)
            best_san = board_before.san(best_move) if best_move else None

            board.push(played_move)

            _, after_cp = analyze_position(engine, board, depth)

            label = classify_move(side_to_move, before_cp, after_cp)

            move_title = (
                f"{board_before.fullmove_number}. {played_san}"
                if side_to_move == chess.WHITE
                else f"{board_before.fullmove_number}... {played_san}"
            )

            moves.append(
                {
                    "index": index + 1,
                    "move_title": move_title,
                    "played_san": played_san,
                    "best_san": best_san or "N/A",
                    "label": label,
                    "label_class": label_class(label),
                    "eval_before": format_eval(before_cp, perspective),
                    "eval_after": format_eval(after_cp, perspective),
                    "fen_after": board.fen(),
                    "board_svg": make_board_svg(
                        board=board,
                        played_move=played_move,
                        best_move=best_move,
                        perspective=perspective,
                    ),
                    "explanation": build_explanation(
                        side=side,
                        played_san=played_san,
                        best_san=best_san,
                        label=label,
                        before_cp=before_cp,
                        after_cp=after_cp,
                        perspective=perspective,
                    ),
                }
            )

    finally:
        engine.quit()

    return {
        "game": {
            "event": game.headers.get("Event", "Training Game"),
            "white": game.headers.get("White", "White"),
            "black": game.headers.get("Black", "Black"),
            "result": game.headers.get("Result", "*"),
            "perspective": perspective_name,
            "input_type": "pgn",
        },
        "moves": moves,
    }


def analyze_fen(fen_text: str, depth: int, perspective_name: str = "White") -> dict:
    try:
        board = chess.Board(fen_text.strip())
    except ValueError as exc:
        raise ValueError("Invalid FEN. Paste a complete legal FEN position.") from exc

    if not board.is_valid():
        raise ValueError("Invalid FEN. Paste a complete legal FEN position.")

    perspective = chess.BLACK if perspective_name == "Black" else chess.WHITE
    side_to_move = board.turn
    side = "White" if side_to_move == chess.WHITE else "Black"

    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    try:
        best_move, current_cp = analyze_position(engine, board, depth)
        best_san = board.san(best_move) if best_move else None

        board_after_best = board.copy()
        if best_move:
            board_after_best.push(best_move)
            _, after_best_cp = analyze_position(engine, board_after_best, depth)
        else:
            after_best_cp = current_cp

    finally:
        engine.quit()

    best_move_text = best_san or "No legal move"

    return {
        "game": {
            "event": "FEN Position",
            "white": "Current",
            "black": "Position",
            "result": "*",
            "perspective": perspective_name,
            "input_type": "fen",
            "side_to_move": side,
        },
        "moves": [
            {
                "index": 1,
                "move_title": f"Current position: {side} to move",
                "played_san": f"{side} to move",
                "best_san": best_move_text,
                "label": "Current Position",
                "label_class": "ok",
                "eval_before": format_eval(current_cp, perspective),
                "eval_after": format_eval(after_best_cp, perspective),
                "fen_after": board.fen(),
                "board_svg": make_board_svg(
                    board=board,
                    played_move=None,
                    best_move=best_move,
                    perspective=perspective,
                ),
                "explanation": (
                    f"{side} is to move. Stockfish recommends "
                    f"<code>{best_move_text}</code> from the current position. "
                    f"The evaluation is <code>{format_eval(current_cp, perspective)}</code> "
                    f"from {perspective_name}'s perspective."
                ),
            }
        ],
    }
