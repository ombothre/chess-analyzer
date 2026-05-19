# Chess Coach PGN Analyzer: End-to-End Project Guide

This document teaches the full project from the top down: what it does, how the files connect, how PGN analysis works, how Stockfish is used, how the UI is built, how the analysis HTML report is generated, and how deployment works.

## 1. What This Project Is

Chess Coach PGN Analyzer is a Streamlit web app that lets a user paste a chess PGN or simple move list, analyze every move with Stockfish, and view a visual move-by-move coaching report.

The app answers questions like:

- What move was played?
- What did Stockfish recommend?
- Did the move lose evaluation?
- Was the move OK, an inaccuracy, a mistake, or a blunder?
- What did the board look like after the move?
- Was the report shown from White's or Black's perspective?

The project has two main user experiences:

1. The Streamlit input app where the user pastes PGN and chooses settings.
2. The generated HTML analysis report shown inside the Streamlit page.

## 2. High-Level Architecture

The project is intentionally small and split by responsibility.

```text
.
├── app.py
├── config.py
├── requirements.txt
├── packages.txt
├── .streamlit/
│   └── config.toml
├── services/
│   ├── engine_service.py
│   ├── explanation_service.py
│   ├── html_service.py
│   └── pgn_service.py
└── ui/
    └── styles.py
```

The flow is:

```text
User pastes PGN in Streamlit
        ↓
app.py receives PGN, depth, perspective
        ↓
services/pgn_service.py parses moves
        ↓
services/engine_service.py asks Stockfish for evaluations
        ↓
services/explanation_service.py creates coach text
        ↓
services/html_service.py builds final HTML report
        ↓
Streamlit embeds report with components.html()
```

## 3. Main Dependencies

The Python dependencies are in `requirements.txt`:

```txt
python-chess>=1.999
streamlit>=1.57.0
watchdog>=6.0.0
```

What each dependency does:

- `streamlit`: Builds the web app.
- `python-chess`: Parses PGN, manages board state, generates legal moves, talks to UCI engines, and renders SVG boards.
- `watchdog`: Improves Streamlit local file watching.

There is also a system dependency in `packages.txt`:

```txt
stockfish
```

This matters for Streamlit Community Cloud. Python packages are installed from `requirements.txt`, but Stockfish is not a Python package. It is a system binary, so Streamlit Cloud installs it from `packages.txt`.

## 4. Configuration: `config.py`

`config.py` stores app-level constants.

### Stockfish Path Resolution

The most important part is:

```python
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
```

This function checks common places where Stockfish might exist.

Why this exists:

- On macOS with Homebrew, Stockfish may be at `/opt/homebrew/bin/stockfish`.
- On Streamlit Cloud, apt often installs it at `/usr/games/stockfish`.
- On many Linux servers, it may be at `/usr/bin/stockfish`.
- If you set an environment variable named `STOCKFISH_PATH`, that takes priority.

The final value is:

```python
STOCKFISH_PATH = resolve_stockfish_path()
```

### Engine Settings

```python
DEFAULT_ENGINE_DEPTH = 14
MIN_ENGINE_DEPTH = 6
MAX_ENGINE_DEPTH = 22
```

Depth controls how deeply Stockfish searches.

- Lower depth is faster.
- Higher depth is stronger but slower.
- The UI limits the user to a reasonable range.

### Move Classification Thresholds

```python
MISTAKE_THRESHOLD = 80
BLUNDER_THRESHOLD = 180
```

These values are centipawns.

One pawn is roughly 100 centipawns, so:

- `80` means about 0.8 pawns.
- `180` means about 1.8 pawns.

The app classifies moves based on how much evaluation was lost.

### Sample PGN

`SAMPLE_PGN` is the default text shown in the PGN box.

## 5. Streamlit App Entry Point: `app.py`

`app.py` is the top-level web app.

It handles:

- Page configuration.
- Custom UI rendering.
- User input.
- Button clicks.
- Calling the analyzer.
- Embedding the generated report.

### Imports

```python
import streamlit as st
import streamlit.components.v1 as components
```

`st` is the main Streamlit API.

`components.html()` lets the app render raw HTML inside Streamlit. This is used for the final analysis report.

The app also imports:

```python
from services.html_service import build_analysis_html
from services.pgn_service import analyze_pgn
from ui.styles import inject_app_css
```

These are the main local project functions.

## 6. Decorative Chess Board in `app.py`

The app uses Unicode chess pieces for decorative boards in the UI.

```python
BOARD_PIECES = {
    0: "♜",
    1: "♞",
    ...
    63: "♖",
}
```

The numbers are 0-based square indexes in a visual 8x8 board.

`render_static_board()` builds an HTML board:

```python
def render_static_board(class_name: str, perspective: str = "White") -> str:
```

It:

- Creates 64 cells.
- Alternates light and dark squares.
- Places pieces.
- Adds focus highlights for example squares.
- Reverses square order when Black perspective is selected.

This board is decorative. It is not used for engine analysis. The actual analysis board comes from `python-chess` SVG rendering in `pgn_service.py`.

## 7. Header Rendering

`render_header()` builds the hero section:

```python
def render_header() -> None:
```

It uses:

- Custom HTML.
- Chess-themed copy.
- Action chips.
- A decorative board.

The HTML is sent through:

```python
st.markdown(..., unsafe_allow_html=True)
```

`unsafe_allow_html=True` is required because Streamlit normally escapes raw HTML.

## 8. Input Panel Rendering

`render_input_panel()` is the main input UI:

```python
def render_input_panel() -> tuple[str, int, str, bool]:
```

It returns:

```python
pgn_text, depth, perspective, analyze_clicked
```

Meaning:

- `pgn_text`: The PGN or move list.
- `depth`: Engine search depth.
- `perspective`: `"White"` or `"Black"`.
- `analyze_clicked`: Whether the user pressed the analyze button.

### Streamlit Container Keys

The UI uses keys:

```python
with st.container(key="analysis_input_panel"):
```

Keys are not only for state. In this project, they are also used by CSS.

Streamlit creates CSS classes like:

```css
.st-key-analysis_input_panel
.st-key-pgn_input
.st-key-depth_input
.st-key-analyze_button
```

This allows `ui/styles.py` to target specific widgets.

### PGN Textarea

```python
pgn_text = st.text_area(
    "PGN / Move list",
    value=SAMPLE_PGN,
    height=640,
    label_visibility="collapsed",
    key="pgn_input",
)
```

The visible label is custom HTML. The Streamlit label is collapsed.

### Perspective Selector

```python
perspective = st.segmented_control(
    "Report perspective",
    options=["White", "Black"],
    default="White",
    key="perspective_control",
)
```

This controls how evaluations and boards are displayed.

Important: it does not change what Stockfish calculates. Stockfish scores are stored internally from White's perspective. The app flips display values for Black perspective.

### Engine Depth Input

```python
depth = st.number_input(
    "Engine depth",
    min_value=MIN_ENGINE_DEPTH,
    max_value=MAX_ENGINE_DEPTH,
    value=DEFAULT_ENGINE_DEPTH,
    step=1,
    key="depth_input",
)
```

This is the safest widget for depth because Streamlit handles the value and min/max validation.

### Analyze Button

```python
analyze_clicked = st.button(
    "Analyze game",
    use_container_width=True,
    key="analyze_button",
)
```

When clicked, `main()` calls `render_analysis()`.

## 9. Analysis Flow in `app.py`

`render_analysis()` performs the main action:

```python
def render_analysis(pgn_text: str, depth: int, perspective: str) -> None:
```

It first validates input:

```python
if not pgn_text.strip():
    st.error("Paste a PGN first.")
    return
```

Then it runs analysis:

```python
analysis = analyze_pgn(pgn_text, depth, perspective)
html = build_analysis_html(analysis)
```

Then it embeds the final report:

```python
components.html(
    html,
    height=report_height,
    scrolling=False,
)
```

### Why `report_height` Exists

Streamlit embeds raw HTML in an iframe. Iframes need a height.

The app estimates report height based on number of moves:

```python
report_height = min(760 + (len(analysis["moves"]) * 850), 22000)
```

This tries to avoid:

- A tiny iframe that cuts off the report.
- A giant iframe that creates blank space.

This is an approximation. If reports are much longer or shorter, tune this formula.

## 10. Main App Function

```python
def main() -> None:
```

This function:

1. Configures Streamlit.
2. Injects CSS.
3. Renders the header.
4. Renders the input panel.
5. Runs analysis when clicked.
6. Handles errors.

The bottom of `app.py` runs the app:

```python
if __name__ == "__main__":
    main()
```

## 11. Engine Logic: `services/engine_service.py`

This file handles Stockfish scores and move classification.

### Stockfish Score Conversion

```python
def score_to_cp(score: chess.engine.PovScore) -> int:
```

Stockfish can return:

- Centipawn score.
- Mate score.

The app converts both into a single integer centipawn-like value.

```python
pov = score.white()
```

This means internal scores are from White's perspective.

Examples:

- `+100`: White is about one pawn better.
- `-100`: Black is about one pawn better.

Mate scores are converted to large values:

```python
100000
-100000
```

### Formatting Evaluations

```python
def format_eval(cp: int, perspective: chess.Color = chess.WHITE) -> str:
```

If the user selected Black perspective, the value is flipped:

```python
display_cp = cp if perspective == chess.WHITE else -cp
```

So if White is `+1.00`, Black sees `-1.00`.

This is display-only. It does not change the raw engine analysis.

### Move Classification

```python
def classify_move(side_to_move: chess.Color, before_cp: int, after_cp: int) -> str:
```

This decides whether a move is:

- OK
- Inaccuracy
- Mistake
- Blunder

The logic is different depending on who moved.

For White:

```python
loss = before_cp - after_cp
```

For Black:

```python
loss = after_cp - before_cp
```

Why?

Because internal eval is from White's perspective.

If White moves and the eval drops from `+1.0` to `0.0`, White lost 1 pawn.

If Black moves and the eval rises from `0.0` to `+1.0`, Black lost 1 pawn because White became better.

### Engine Call

```python
def analyze_position(engine, board, depth):
```

This asks Stockfish to analyze:

```python
info = engine.analyse(board, chess.engine.Limit(depth=depth))
```

Then it extracts:

- Best move from principal variation.
- Evaluation score.

## 12. PGN Logic: `services/pgn_service.py`

This is the most important service file.

It parses the game, loops through moves, calls Stockfish, builds board SVGs, and returns structured data.

### Board Colors

```python
BOARD_COLORS = {
    "square light": "#f0c98f",
    "square dark": "#a66b3d",
    ...
}
```

These colors customize the SVG boards produced by `python-chess`.

### Board SVG Generation

```python
def make_board_svg(board, played_move, best_move, perspective):
```

This creates arrows:

- Blue arrow: actual played move.
- Green arrow: engine best move.

```python
if played_move:
    arrows.append(chess.svg.Arrow(..., color="#2563eb"))
```

If the played move differs from Stockfish's move, it adds the green arrow:

```python
if best_move and played_move != best_move:
```

Then it renders:

```python
return chess.svg.board(
    board=board,
    size=420,
    coordinates=True,
    orientation=perspective,
    arrows=arrows,
    squares=squares,
    colors=BOARD_COLORS,
)
```

The `orientation` argument flips the board for Black perspective.

### PGN Analysis Function

```python
def analyze_pgn(pgn_text: str, depth: int, perspective_name: str = "White") -> dict:
```

This is the core pipeline.

It reads the PGN:

```python
game = chess.pgn.read_game(StringIO(pgn_text))
```

If parsing fails:

```python
raise ValueError("Invalid PGN. Paste a valid PGN or move list.")
```

It creates the starting board:

```python
board = game.board()
```

It opens Stockfish:

```python
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
```

Then it loops through every move:

```python
for index, node in enumerate(game.mainline()):
```

For each move:

1. Copy board before move.
2. Determine side to move.
3. Convert move to SAN.
4. Analyze position before move.
5. Get Stockfish best move.
6. Push played move.
7. Analyze position after move.
8. Classify the move.
9. Generate board SVG.
10. Generate explanation.
11. Append result to `moves`.

The engine is always closed:

```python
finally:
    engine.quit()
```

This is important. External processes should not be left running.

### Returned Analysis Shape

The function returns:

```python
{
    "game": {
        "event": ...,
        "white": ...,
        "black": ...,
        "result": ...,
        "perspective": ...
    },
    "moves": [...]
}
```

Each move contains:

```python
{
    "index": 1,
    "move_title": "1. e4",
    "played_san": "e4",
    "best_san": "e4",
    "label": "OK",
    "label_class": "ok",
    "eval_before": "+0.48",
    "eval_after": "+0.45",
    "fen_after": "...",
    "board_svg": "<svg>...</svg>",
    "explanation": "..."
}
```

This object is designed for `html_service.py`.

## 13. Explanation Logic: `services/explanation_service.py`

This file turns raw analysis into human-readable text.

```python
def build_explanation(...):
```

If the move is OK:

```python
return (
    f"{side} played <code>{escape(played_san)}</code>. "
    f"This is close to the engine recommendation. "
    f"The evaluation remains stable."
)
```

If the move is not OK:

```python
return (
    f"{side} played <code>{escape(played_san)}</code>, but Stockfish preferred "
    f"<code>{escape(best_san or 'N/A')}</code>. "
    ...
)
```

### Why `escape()` Is Used

PGN text can contain unexpected characters. Because explanations are inserted into HTML, values like SAN moves are escaped to prevent broken HTML or injection.

## 14. HTML Report: `services/html_service.py`

This file builds the final analysis report as a full HTML document.

```python
def build_analysis_html(analysis: dict) -> str:
```

It receives the structured object from `analyze_pgn()`.

It builds:

- Hero/report header.
- Summary instructions.
- One card per move.
- Board SVG.
- Details table.
- Coach explanation.
- FEN details.

### Move Cards

For each move:

```python
<article class="analysis-card {move["label_class"]}">
```

The class controls card color:

- `ok`
- `inaccuracy`
- `mistake`
- `blunder`

The board SVG is inserted directly:

```python
{move["board_svg"]}
```

This is why `pgn_service.py` returns ready-to-render SVG.

### Report Styling

The report uses its own CSS inside the HTML string.

This is necessary because the report is rendered inside an iframe with:

```python
components.html(...)
```

CSS from `ui/styles.py` does not automatically style content inside the iframe. That is why the report has its own CSS.

## 15. UI Styling: `ui/styles.py`

This file injects custom CSS into Streamlit:

```python
def inject_app_css() -> None:
    st.markdown("<style>...</style>", unsafe_allow_html=True)
```

The CSS does several jobs:

- Sets the chess-themed background.
- Hides Streamlit chrome.
- Styles the hero.
- Styles the PGN input panel.
- Styles the setup card.
- Styles the decorative chess boards.
- Styles the segmented control.
- Styles the number input.
- Styles the analyze button.
- Adds responsive mobile behavior.

### Why CSS Uses `.st-key-*`

Streamlit gives elements with keys generated CSS classes.

For example:

```python
st.text_area(..., key="pgn_input")
```

Can be targeted with:

```css
.st-key-pgn_input textarea {
    ...
}
```

This is much more stable than targeting every Streamlit textarea globally.

### Responsive CSS

The mobile layout is controlled with:

```css
@media (max-width: 900px) {
    ...
}
```

This reduces padding, stacks layout, hides the hero board, scales the setup board, and prevents horizontal overflow.

## 16. Streamlit Theme: `.streamlit/config.toml`

The project includes:

```toml
[theme]
base = "light"
primaryColor = "#2f7d46"
backgroundColor = "#f3eee4"
secondaryBackgroundColor = "#fffaf1"
textColor = "#1f2933"
```

This helps Streamlit use a light theme by default.

This matters because browser/system dark mode or Streamlit defaults can otherwise make input text hard to read.

## 17. Deployment Files

### `requirements.txt`

Used by Streamlit Cloud and other hosts to install Python packages.

### `packages.txt`

Used by Streamlit Cloud to install system packages.

For this app:

```txt
stockfish
```

Without this file, the deployed app may run but fail when the user clicks Analyze.

## 18. Local Development

Install Stockfish:

```bash
brew install stockfish
```

Create environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## 19. Streamlit Cloud Deployment

Steps:

1. Push repo to GitHub.
2. Ensure `requirements.txt` is committed.
3. Ensure `packages.txt` is committed.
4. Ensure `.streamlit/config.toml` is committed.
5. Create a Streamlit Cloud app from the GitHub repo.
6. Set main file to `app.py`.
7. Deploy.

If Stockfish fails:

1. Check `packages.txt` contains `stockfish`.
2. Reboot the app in Streamlit Cloud.
3. Confirm `config.py` checks `/usr/games/stockfish`.

## 20. Important Chess Concepts in the Code

### PGN

PGN means Portable Game Notation. It stores chess games as text.

Example:

```pgn
[Event "Training Game"]
[White "White"]
[Black "Black"]
[Result "*"]

1. e4 c5
2. Nf3 d6
```

`python-chess` can parse this and replay the game move by move.

### SAN

SAN means Standard Algebraic Notation.

Examples:

- `e4`
- `Nf3`
- `Bxe6`
- `O-O`

The app displays moves in SAN.

### FEN

FEN means Forsyth-Edwards Notation. It describes one board position.

The app stores `fen_after` for every move so users can inspect the exact position after that move.

### Centipawns

Stockfish evaluation is often represented in centipawns.

- `+100` means White is about one pawn better.
- `-100` means Black is about one pawn better.

The app displays this as:

- `+1.00`
- `-1.00`

### Perspective

Internally, evaluations are from White's perspective.

When user selects Black perspective:

```python
display_cp = -cp
```

That makes positive values mean Black is better.

## 21. Why Move Classification Needs Side-to-Move

Move classification must consider who played the move.

If White plays and the eval goes down, White made the position worse.

If Black plays and the eval goes up, Black made the position worse because White became better.

That is why:

```python
if side_to_move == chess.WHITE:
    loss = before_cp - after_cp
else:
    loss = after_cp - before_cp
```

This is one of the most important pieces of logic in the project.

## 22. Common Issues and Fixes

### Stockfish Not Found

Symptom:

```text
Stockfish was not found on this server
```

Fix:

- Install Stockfish locally.
- On Streamlit Cloud, commit `packages.txt`.
- Set `STOCKFISH_PATH` if needed.

### Report Cut Off

The HTML report is inside an iframe. If the iframe height is too small, the report may be cut off.

Tune this line in `app.py`:

```python
report_height = min(760 + (len(analysis["moves"]) * 850), 22000)
```

Increase `850` if cards are being cut.

Decrease it if there is too much blank space.

### Mobile Layout Broken

Most mobile layout fixes live in `ui/styles.py` under:

```css
@media (max-width: 900px) {
    ...
}
```

### Depth Control Styling Weird

The depth control is a native Streamlit `number_input`.

Its CSS is targeted through:

```css
.st-key-depth_input ...
```

Avoid replacing it with custom Streamlit columns unless absolutely needed. Streamlit columns can behave unpredictably on small screens.

## 23. How to Add a New Feature

### Add a New Move Label

Change:

- `classify_move()` in `engine_service.py`
- `label_class()` in `engine_service.py`
- CSS badge/card styles in `html_service.py`

### Change Board Colors

Change:

```python
BOARD_COLORS
```

in `pgn_service.py`.

Also update matching UI colors in `ui/styles.py`.

### Change Evaluation Thresholds

Change:

```python
MISTAKE_THRESHOLD
BLUNDER_THRESHOLD
```

in `config.py`.

### Add More Explanation Detail

Change:

```python
build_explanation()
```

in `explanation_service.py`.

For example, you could include:

- Exact centipawn loss.
- Whether a tactic was missed.
- Whether the best move was a capture/check.

## 24. Design Decisions

### Why Streamlit?

Streamlit makes it fast to build a Python web app without a separate frontend framework.

### Why Custom HTML/CSS?

Default Streamlit UI looks generic. This project uses custom HTML/CSS to create a more chess-themed experience.

### Why Generate HTML Report Instead of Streamlit Cards?

The report has complex styling and repeated move cards. Building it as HTML gives full control over layout and makes it easier to render board SVGs.

### Why Use Stockfish Locally Instead of an API?

Stockfish is free, strong, and fast. Running it locally avoids API costs and rate limits.

## 25. Mental Model of the Whole App

Think of the project as four layers:

```text
UI Layer
Streamlit widgets, CSS, user input

Parsing Layer
python-chess reads PGN and replays moves

Engine Layer
Stockfish evaluates positions and recommends moves

Report Layer
HTML/CSS turns structured analysis into a readable report
```

Each layer has its own file:

```text
UI Layer       → app.py, ui/styles.py
Parsing Layer  → services/pgn_service.py
Engine Layer   → services/engine_service.py
Report Layer   → services/html_service.py
```

## 26. End-to-End Example

User enters:

```pgn
1. e4 c5
```

The app:

1. Reads the game.
2. Starts from the initial board.
3. Before `e4`, asks Stockfish for best move and eval.
4. Pushes `e4`.
5. Asks Stockfish for eval after `e4`.
6. Compares before and after.
7. Labels the move.
8. Generates board after `e4`.
9. Repeats for `c5`.
10. Builds final report.

## 27. What to Learn From This Project

This project teaches:

- Building Streamlit apps.
- Using custom CSS in Streamlit.
- Parsing chess games with `python-chess`.
- Communicating with UCI chess engines.
- Handling centipawn and mate evaluations.
- Designing data flow between services.
- Generating HTML reports.
- Deploying apps with system dependencies.

## 28. Suggested Next Improvements

Useful future upgrades:

- Add downloadable HTML report.
- Add PGN upload.
- Add accuracy percentage per side.
- Add opening name detection.
- Add move filtering by blunders only.
- Add caching for repeated analysis.
- Add async/progress per move.
- Add board size setting.
- Add support for engine time limit instead of depth.

## 29. Quick Reference

Run locally:

```bash
streamlit run app.py
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Stockfish:

```bash
brew install stockfish
```

Core function:

```python
analyze_pgn(pgn_text, depth, perspective)
```

Report builder:

```python
build_analysis_html(analysis)
```

Main UI file:

```text
app.py
```

Main CSS file:

```text
ui/styles.py
```

## 30. Final Summary

Chess Coach PGN Analyzer is a Streamlit app that combines a Python UI, `python-chess`, Stockfish, custom SVG board rendering, and generated HTML reports.

The most important flow is:

```text
PGN → python-chess board states → Stockfish evals → move labels → board SVGs → HTML report
```

Once you understand that pipeline, the whole project becomes straightforward to modify and extend.
