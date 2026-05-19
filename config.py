from __future__ import annotations

import shutil

STOCKFISH_PATH = shutil.which("stockfish") or "/opt/homebrew/bin/stockfish"

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