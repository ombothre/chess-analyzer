from __future__ import annotations

from html import escape

import chess

from services.engine_service import format_eval


def build_explanation(
    side: str,
    played_san: str,
    best_san: str | None,
    label: str,
    before_cp: int,
    after_cp: int,
    perspective: chess.Color = chess.WHITE,
) -> str:
    if label == "OK":
        return (
            f"{side} played <code>{escape(played_san)}</code>. "
            f"This is close to the engine recommendation. "
            f"The evaluation remains stable."
        )

    return (
        f"{side} played <code>{escape(played_san)}</code>, but Stockfish preferred "
        f"<code>{escape(best_san or 'N/A')}</code>. "
        f"The evaluation changed from <code>{format_eval(before_cp, perspective)}</code> to "
        f"<code>{format_eval(after_cp, perspective)}</code>, so this is marked as "
        f"<strong>{escape(label)}</strong>."
    )
