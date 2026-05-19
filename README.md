# Chess Coach PGN / FEN Analyzer

A Streamlit app for analyzing chess games and positions with Stockfish. Paste a PGN or move list for a move-by-move report, or paste a FEN to analyze only the current side to move. Choose White or Black perspective and generate a themed report with board diagrams, engine-best moves, evaluations, and coach-style explanations.

## Features

- Paste full PGN or simple move lists.
- Paste a FEN position for single-position analysis.
- Analyze positions with Stockfish.
- Choose report perspective: White or Black.
- View move quality labels: OK, Inaccuracy, Mistake, Blunder.
- See played move and engine-best move arrows on each board.
- For FEN input, see only the current-position recommendation.
- Generate a styled chess-themed analysis report.
- Streamlit UI with custom wood/green chess styling.

## Demo

Run locally:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Requirements

- Python 3.11+
- Stockfish installed on the host machine
- Python packages from `requirements.txt`

Install Stockfish:

```bash
# macOS
brew install stockfish

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install stockfish
```

The app resolves Stockfish with:

```python
shutil.which("stockfish")
```

It also checks common deployment paths such as `/usr/games/stockfish`, which is where Streamlit Cloud commonly installs the apt package.

If your binary is somewhere unusual, set a `STOCKFISH_PATH` environment variable or update `config.py`.

## Local Setup

Clone the repo:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Project Structure

```text
.
├── app.py                    # Streamlit UI and app flow
├── config.py                 # Stockfish path, depth, thresholds, sample PGN
├── requirements.txt          # Python dependencies
├── packages.txt              # System dependency for Streamlit Cloud
├── services/
│   ├── engine_service.py      # Stockfish scoring and move classification
│   ├── explanation_service.py # Coach-style move explanations
│   ├── html_service.py        # Rendered analysis report HTML
│   └── pgn_service.py         # PGN parsing and board SVG generation
├── ui/
│   └── styles.py              # Custom Streamlit CSS
└── .streamlit/
    └── config.toml            # Streamlit theme
```

## Configuration

Edit `config.py` to tune behavior:

```python
DEFAULT_ENGINE_DEPTH = 14
MIN_ENGINE_DEPTH = 6
MAX_ENGINE_DEPTH = 22

MISTAKE_THRESHOLD = 80
BLUNDER_THRESHOLD = 180
```

Higher depth is stronger but slower.

## Deployment

### Streamlit Community Cloud

This repo includes:

- `requirements.txt`
- `packages.txt` with `stockfish`
- `.streamlit/config.toml`

Steps:

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the repo.
4. Set the main file to:

```text
app.py
```

Streamlit Cloud should install Python dependencies from `requirements.txt` and Stockfish from `packages.txt`.

If you still see a Stockfish error after deployment:

1. Confirm `packages.txt` is committed to GitHub.
2. Confirm it contains exactly:

```text
stockfish
```

3. Reboot the app from Streamlit Cloud's Manage app menu.

### Render

Render also works well, but you need to install Stockfish during build. A typical start command is:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

Example build command:

```bash
apt-get update && apt-get install -y stockfish && pip install -r requirements.txt
```

## Notes

- Evaluations are stored internally from White's point of view, then displayed from the selected report perspective.
- Blue arrows show the played move.
- Green arrows show Stockfish's preferred move from the same position.
- The app is meant for training and review, not official engine adjudication.

## License

Add your preferred license before publishing if you want others to reuse or modify the project.
