from __future__ import annotations

import streamlit as st

from config import (
    DEFAULT_ENGINE_DEPTH,
    MAX_ENGINE_DEPTH,
    MIN_ENGINE_DEPTH,
    SAMPLE_PGN,
    STOCKFISH_PATH,
)
from services.html_service import build_analysis_html
from services.pgn_service import analyze_pgn
from ui.styles import inject_app_css

import streamlit.components.v1 as components


BOARD_PIECES = {
    0: "♜",
    1: "♞",
    2: "♝",
    3: "♛",
    4: "♚",
    5: "♝",
    6: "♞",
    7: "♜",
    8: "♟",
    9: "♟",
    10: "♟",
    11: "♟",
    12: "♟",
    13: "♟",
    14: "♟",
    15: "♟",
    48: "♙",
    49: "♙",
    50: "♙",
    51: "♙",
    52: "♙",
    53: "♙",
    54: "♙",
    55: "♙",
    56: "♖",
    57: "♘",
    58: "♗",
    59: "♕",
    60: "♔",
    61: "♗",
    62: "♘",
    63: "♖",
}


def render_static_board(class_name: str, perspective: str = "White") -> str:
    cells = []
    indices = range(64)

    if perspective == "Black":
        indices = reversed(range(64))

    for index in indices:
        row = index // 8
        col = index % 8
        square = "light" if (row + col) % 2 == 0 else "dark"
        piece = BOARD_PIECES.get(index, "")
        square_name = f"{chr(97 + col)}{8 - row}"
        focus_class = ""

        if perspective == "White" and square_name in {"e2", "e4"}:
            focus_class = " focus"
        elif perspective == "Black" and square_name in {"e7", "e5"}:
            focus_class = " focus"

        cells.append(
            f'<span class="{square}{focus_class}" data-square="{square_name}">{piece}</span>'
        )

    return (
        f'<div class="{class_name} chess-board {perspective.lower()}-view" '
        f'aria-hidden="true">{"".join(cells)}</div>'
    )


def render_header() -> None:
    st.markdown(
        f"""
        <div class="app-title">
            <div class="app-title-copy">
                <span class="eyebrow">Chess analysis lab</span>
                <h1>Chess Coach PGN Analyzer</h1>
                <p>Review every move with Stockfish, board diagrams, and coach-style explanations.</p>
                <div class="hero-actions">
                    <span>White or Black perspective</span>
                    <span>Move-by-move accuracy</span>
                    <span>Visual arrows</span>
                </div>
            </div>
            <div class="hero-board" aria-hidden="true">
                {render_static_board("hero-board-grid")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_depth_control() -> int:
    if "engine_depth" not in st.session_state:
        st.session_state.engine_depth = DEFAULT_ENGINE_DEPTH

    st.markdown('<p class="field-label depth-label">Engine depth</p>', unsafe_allow_html=True)
    minus_col, value_col, plus_col = st.columns([0.22, 0.56, 0.22], gap="small")

    with minus_col:
        if st.button("−", key="depth_decrease", use_container_width=True):
            st.session_state.engine_depth = max(MIN_ENGINE_DEPTH, st.session_state.engine_depth - 1)

    with value_col:
        st.markdown(
            f'<div class="depth-value" aria-live="polite">{st.session_state.engine_depth}</div>',
            unsafe_allow_html=True,
        )

    with plus_col:
        if st.button("+", key="depth_increase", use_container_width=True):
            st.session_state.engine_depth = min(MAX_ENGINE_DEPTH, st.session_state.engine_depth + 1)

    return int(st.session_state.engine_depth)


def render_input_panel() -> tuple[str, int, str, bool]:
    with st.container(key="analysis_input_panel"):
        st.markdown(
            """
            <div class="input-head">
                <div>
                    <span class="eyebrow dark">Analyze a game</span>
                    <p class="input-card-title">Paste your PGN</p>
                    <p class="input-card-subtitle">
                        Paste a full PGN or a simple move list. Example:
                        <code>1. e4 c5 2. Nf3 d6</code>
                    </p>
                </div>
                <span class="input-chip">Stockfish report</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        editor_col, setup_col = st.columns([2.05, 1], gap="large", vertical_alignment="top")

        with editor_col:
            st.markdown('<p class="field-label">PGN / Move list</p>', unsafe_allow_html=True)
            pgn_text = st.text_area(
                "PGN / Move list",
                value=SAMPLE_PGN,
                height=640,
                label_visibility="collapsed",
                key="pgn_input",
            )

        with setup_col:
            with st.container(key="study_setup"):
                st.markdown(
                    f"""
                    <div class="setup-card-head">
                        <div>
                            <p class="setup-kicker">Study setup</p>
                            <h2>Choose your side</h2>
                        </div>
                        <div class="setup-mark">♞</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                perspective = st.segmented_control(
                    "Report perspective",
                    options=["White", "Black"],
                    default="White",
                    key="perspective_control",
                )

                selected_side = perspective or "White"
                side_class = selected_side.lower()
                side_piece = "♔" if selected_side == "White" else "♚"
                side_copy = (
                    "Boards and evaluations are shown from White's point of view."
                    if selected_side == "White"
                    else "Boards and evaluations flip to Black's point of view."
                )

                st.markdown(
                    f"""
                    <div class="side-state {side_class}">
                        <span>{side_piece}</span>
                        <p>{side_copy}</p>
                    </div>
                    {render_static_board("setup-board", selected_side)}
                    """,
                    unsafe_allow_html=True,
                )

                with st.container(key="depth_control"):
                    depth = render_depth_control()

                analyze_clicked = st.button("Analyze game", use_container_width=True, key="analyze_button")

    return pgn_text, int(depth), perspective or "White", analyze_clicked


def render_analysis(pgn_text: str, depth: int, perspective: str) -> None:
    if not pgn_text.strip():
        st.error("Paste a PGN first.")
        return

    with st.spinner("Analyzing with Stockfish..."):
        analysis = analyze_pgn(pgn_text, depth, perspective)
        html = build_analysis_html(analysis)

    components.html(
        html,
        height=1200,
        scrolling=True,
    )

def main() -> None:
    st.set_page_config(
        page_title="Chess Coach",
        page_icon="♟️",
        layout="wide",
    )

    inject_app_css()
    render_header()

    pgn_text, depth, perspective, analyze_clicked = render_input_panel()

    if analyze_clicked:
        try:
            render_analysis(pgn_text, depth, perspective)

        except FileNotFoundError:
            st.error(
                "Stockfish was not found on this server. "
                f"Tried `{STOCKFISH_PATH}`. "
                "For Streamlit Cloud, make sure `packages.txt` contains `stockfish`, "
                "commit it to GitHub, and reboot the app."
            )

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")


if __name__ == "__main__":
    main()
