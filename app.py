from __future__ import annotations

import streamlit as st

from config import (
    DEFAULT_ENGINE_DEPTH,
    MAX_ENGINE_DEPTH,
    MIN_ENGINE_DEPTH,
    SAMPLE_FEN,
    SAMPLE_PGN,
    STOCKFISH_PATH,
)
from services.html_service import build_analysis_html
from services.pgn_service import analyze_fen, analyze_pgn
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


def render_input_panel() -> tuple[str, str, int, str, bool]:
    with st.container(key="analysis_input_panel"):
        st.markdown(
            """
            <div class="input-head">
                <div>
                    <span class="eyebrow dark">Analyze a game</span>
                    <p class="input-card-title">Paste your PGN or FEN</p>
                    <p class="input-card-subtitle">
                        Use PGN for move-by-move review, or FEN to analyze only the current side to move.
                    </p>
                </div>
                <span class="input-chip">Stockfish report</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        editor_col, setup_col = st.columns([2.05, 1], gap="large", vertical_alignment="top")

        with editor_col:
            input_mode = st.segmented_control(
                "Input type",
                options=["PGN / Move list", "FEN position"],
                default="PGN / Move list",
                key="input_mode_control",
            )
            selected_input_mode = input_mode or "PGN / Move list"
            is_fen_mode = selected_input_mode == "FEN position"
            field_label = "FEN position" if is_fen_mode else "PGN / Move list"
            field_value = SAMPLE_FEN if is_fen_mode else SAMPLE_PGN
            field_key = "fen_input" if is_fen_mode else "pgn_input"

            st.markdown(f'<p class="field-label">{field_label}</p>', unsafe_allow_html=True)
            input_text = st.text_area(
                field_label,
                value=field_value,
                height=640,
                label_visibility="collapsed",
                key=field_key,
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

                depth = st.number_input(
                    "Engine depth",
                    min_value=MIN_ENGINE_DEPTH,
                    max_value=MAX_ENGINE_DEPTH,
                    value=DEFAULT_ENGINE_DEPTH,
                    step=1,
                    key="depth_input",
                )

                button_label = "Analyze position" if is_fen_mode else "Analyze game"
                analyze_clicked = st.button(button_label, use_container_width=True, key="analyze_button")

    return input_text, selected_input_mode, int(depth), perspective or "White", analyze_clicked


def render_analysis(input_text: str, input_mode: str, depth: int, perspective: str) -> None:
    if not input_text.strip():
        input_name = "FEN" if input_mode == "FEN position" else "PGN"
        st.error(f"Paste a {input_name} first.")
        return

    with st.spinner("Analyzing with Stockfish..."):
        if input_mode == "FEN position":
            analysis = analyze_fen(input_text, depth, perspective)
        else:
            analysis = analyze_pgn(input_text, depth, perspective)
        html = build_analysis_html(analysis)

    report_height = min(760 + (len(analysis["moves"]) * 850), 22000)

    components.html(
        html,
        height=report_height,
        scrolling=False,
    )

def main() -> None:
    st.set_page_config(
        page_title="Chess Coach",
        page_icon="♟️",
        layout="wide",
    )

    inject_app_css()
    render_header()

    input_text, input_mode, depth, perspective, analyze_clicked = render_input_panel()

    if analyze_clicked:
        try:
            render_analysis(input_text, input_mode, depth, perspective)

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
