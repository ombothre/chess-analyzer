from __future__ import annotations

import os
import shutil
from pathlib import Path


def resolve_stockfish_path() -> str:
    candidates = [
        os.environ.get("STOCKFISH_PATH"),
        shutil.which("stockfish"),
        "/usr/games/stockfish",
        "/usr/bin/stockfish",
        "/usr/local/bin/stockfish",
        "/opt/homebrew/bin/stockfish",
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate

    return "stockfish"


STOCKFISH_PATH = resolve_stockfish_path()

DEFAULT_ENGINE_DEPTH = 14
MIN_ENGINE_DEPTH = 6
MAX_ENGINE_DEPTH = 22

MISTAKE_THRESHOLD = 80
BLUNDER_THRESHOLD = 180

SAMPLE_PGN = """[Event "Training Game"]
[White "White"]
[Black "Black"]
[Result "*"]

1. e4 c5
2. Nc3 Nc6
3. Bc4 Nf6
4. Nf3 d6
5. d3 e6
6. Be3 *
"""

SAMPLE_FEN = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 2 3"
