from __future__ import annotations

import chess
import chess.engine

from config import BLUNDER_THRESHOLD, MISTAKE_THRESHOLD


def score_to_cp(score: chess.engine.PovScore) -> int:
    pov = score.white()

    if pov.is_mate():
        mate = pov.mate()
        if mate is None:
            return 0
        return 100000 if mate > 0 else -100000

    return pov.score() or 0


def format_eval(cp: int, perspective: chess.Color = chess.WHITE) -> str:
    display_cp = cp if perspective == chess.WHITE else -cp
    perspective_name = "White" if perspective == chess.WHITE else "Black"
    opponent_name = "Black" if perspective == chess.WHITE else "White"

    if display_cp >= 100000:
        return f"{perspective_name} has mate"
    if display_cp <= -100000:
        return f"{opponent_name} has mate"

    pawns = display_cp / 100
    return f"+{pawns:.2f}" if pawns > 0 else f"{pawns:.2f}"


def classify_move(side_to_move: chess.Color, before_cp: int, after_cp: int) -> str:
    if side_to_move == chess.WHITE:
        loss = before_cp - after_cp
    else:
        loss = after_cp - before_cp

    if loss >= BLUNDER_THRESHOLD:
        return "Blunder"
    if loss >= MISTAKE_THRESHOLD:
        return "Mistake"
    if loss >= 40:
        return "Inaccuracy"
    return "OK"


def label_class(label: str) -> str:
    return {
        "OK": "ok",
        "Inaccuracy": "inaccuracy",
        "Mistake": "mistake",
        "Blunder": "blunder",
    }.get(label, "ok")


def analyze_position(
    engine: chess.engine.SimpleEngine,
    board: chess.Board,
    depth: int,
) -> tuple[chess.Move | None, int]:
    info = engine.analyse(board, chess.engine.Limit(depth=depth))

    best_move = None
    if "pv" in info and info["pv"]:
        best_move = info["pv"][0]

    cp = score_to_cp(info["score"])
    return best_move, cp
