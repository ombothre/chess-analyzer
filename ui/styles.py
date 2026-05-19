from __future__ import annotations

import streamlit as st


def inject_app_css() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg: #f3eee4;
                --paper: #fffaf1;
                --paper-2: #f7ead8;
                --ink: #1f2933;
                --muted: #6b6258;
                --wood: #9a673d;
                --wood-dark: #4b2f1d;
                --green: #2f7d46;
                --green-dark: #1f5c35;
                --line: #dccbb5;
                --shadow: rgba(76, 52, 31, 0.18);
            }

            html,
            body,
            .stApp {
                color-scheme: light !important;
            }

            body,
            [class*="css"] {
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            .stApp {
                background:
                    linear-gradient(45deg, rgba(154, 103, 61, 0.045) 25%, transparent 25%),
                    linear-gradient(-45deg, rgba(154, 103, 61, 0.045) 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, rgba(154, 103, 61, 0.045) 75%),
                    linear-gradient(-45deg, transparent 75%, rgba(154, 103, 61, 0.045) 75%),
                    radial-gradient(circle at 12% 0%, rgba(47, 125, 70, 0.13), transparent 30rem),
                    linear-gradient(180deg, #fbf7ef 0%, var(--bg) 100%);
                background-size: 72px 72px, 72px 72px, 72px 72px, 72px 72px, auto, auto;
                background-position: 0 0, 0 36px, 36px -36px, -36px 0, 0 0, 0 0;
                color: var(--ink);
            }

            header[data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            #MainMenu,
            footer {
                display: none !important;
            }

            .block-container {
                max-width: 1440px;
                padding: 30px 42px 72px;
            }

            .element-container {
                margin-bottom: 0 !important;
            }

            .app-title {
                position: relative;
                display: grid;
                grid-template-columns: minmax(0, 1fr) 310px;
                align-items: center;
                gap: 48px;
                min-height: 320px;
                margin-bottom: 34px;
                padding: 50px 58px;
                border-radius: 30px;
                overflow: hidden;
                color: #fffaf1;
                background:
                    radial-gradient(circle at 82% 16%, rgba(248, 215, 154, 0.20), transparent 20rem),
                    linear-gradient(135deg, #2b1b12 0%, #163321 55%, #0f1f17 100%);
                border: 1px solid rgba(255, 250, 241, 0.16);
                box-shadow: 0 34px 80px var(--shadow);
                transition: transform 180ms ease, box-shadow 180ms ease;
            }

            .app-title:hover {
                transform: translateY(-2px);
                box-shadow: 0 40px 92px rgba(76, 52, 31, 0.22);
            }

            .app-title::after {
                content: "";
                position: absolute;
                inset: auto 0 0 0;
                height: 8px;
                background: linear-gradient(90deg, var(--wood), #d7a15f, var(--green));
            }

            .app-title-copy {
                position: relative;
                z-index: 1;
                max-width: 900px;
            }

            .eyebrow {
                display: inline-flex;
                align-items: center;
                min-height: 32px;
                padding: 0 13px;
                border-radius: 999px;
                background: rgba(255, 250, 241, 0.12);
                border: 1px solid rgba(255, 250, 241, 0.20);
                color: #f8d79a;
                font-size: 12px;
                font-weight: 900;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            .eyebrow.dark {
                background: #edf7ed;
                border-color: #b9dfc4;
                color: var(--green-dark);
                margin-bottom: 12px;
            }

            .app-title h1 {
                margin: 18px 0 14px;
                color: #fffaf1;
                font-size: 54px;
                line-height: 1.02;
                letter-spacing: 0;
                font-weight: 950;
            }

            .app-title p {
                margin: 0;
                max-width: 770px;
                color: #eadfcf;
                font-size: 18px;
                line-height: 1.65;
                font-weight: 650;
            }

            .hero-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 24px;
            }

            .hero-actions span {
                display: inline-flex;
                align-items: center;
                min-height: 34px;
                padding: 0 12px;
                border-radius: 999px;
                background: rgba(255, 250, 241, 0.10);
                border: 1px solid rgba(255, 250, 241, 0.16);
                color: #fffaf1;
                font-size: 13px;
                font-weight: 850;
                transition: background 160ms ease, transform 160ms ease;
            }

            .hero-actions span:hover {
                background: rgba(255, 250, 241, 0.18);
                transform: translateY(-1px);
            }

            .hero-board {
                position: relative;
                z-index: 1;
                width: 320px;
                aspect-ratio: 1;
                padding: 16px;
                border-radius: 28px;
                background: rgba(255, 250, 241, 0.12);
                border: 1px solid rgba(255, 250, 241, 0.22);
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.22);
                transition: transform 220ms ease, box-shadow 220ms ease;
            }

            .hero-board:hover {
                transform: rotate(-1deg) translateY(-2px);
                box-shadow: 0 30px 70px rgba(0, 0, 0, 0.28);
            }

            .hero-board-grid {
                display: grid;
                grid-template-columns: repeat(8, 1fr);
                width: 100%;
                height: 100%;
                border: 10px solid #2b1b12;
                border-radius: 18px;
                overflow: hidden;
                background: #f0c98f;
                position: relative;
            }

            .hero-board-grid::after,
            .setup-board::after {
                content: "";
                position: absolute;
                inset: 0;
                pointer-events: none;
                background: linear-gradient(120deg, transparent 0%, rgba(255, 250, 241, 0.22) 45%, transparent 62%);
                transform: translateX(-130%);
                animation: board-sheen 5.5s ease-in-out infinite;
            }

            .chess-board span {
                position: relative;
                display: grid;
                place-items: center;
                min-width: 0;
                color: #1f160f;
                line-height: 1;
                font-family: "Times New Roman", "DejaVu Serif", serif;
                text-shadow: 0 1px 0 rgba(255, 250, 241, 0.35);
                transition: transform 150ms ease, filter 150ms ease, background 150ms ease;
            }

            .hero-board-grid span {
                font-size: 25px;
            }

            .chess-board span.light {
                background: #f0c98f;
            }

            .chess-board span.dark {
                background: #a66b3d;
            }

            .chess-board span.focus {
                box-shadow: inset 0 0 0 3px rgba(47, 125, 70, 0.58);
                background: #d8dda2;
            }

            .chess-board span:not(:empty):hover {
                transform: scale(1.18);
                filter: drop-shadow(0 5px 5px rgba(43, 27, 18, 0.28));
                z-index: 2;
            }

            .chess-board span[data-square="a8"]::before,
            .chess-board span[data-square="h1"]::before {
                content: attr(data-square);
                position: absolute;
                left: 4px;
                bottom: 3px;
                color: rgba(43, 27, 18, 0.58);
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                font-size: 9px;
                font-weight: 900;
                text-transform: uppercase;
            }

            .st-key-analysis_input_panel {
                position: relative;
                padding: 34px;
                margin-bottom: 34px;
                border-radius: 30px;
                border: 1px solid var(--line);
                background: rgba(255, 250, 241, 0.94);
                box-shadow: 0 26px 64px var(--shadow);
                transition: box-shadow 180ms ease, transform 180ms ease;
            }

            .st-key-analysis_input_panel:hover {
                box-shadow: 0 30px 74px rgba(76, 52, 31, 0.20);
            }

            .input-head {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 22px;
                margin-bottom: 26px;
            }

            .input-card-title {
                margin: 0 0 8px;
                color: var(--ink);
                font-size: 26px;
                line-height: 1.1;
                font-weight: 950;
            }

            .input-card-subtitle {
                margin: 0;
                color: var(--muted);
                font-size: 16px;
                line-height: 1.6;
                font-weight: 700;
            }

            .input-card-subtitle code {
                display: inline-flex;
                padding: 4px 8px;
                border-radius: 8px;
                background: #2b1b12;
                color: #8ce99a;
                font-family: "SFMono-Regular", Consolas, Menlo, monospace;
                font-size: 13px;
                font-weight: 900;
            }

            .input-chip {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-height: 40px;
                padding: 0 16px;
                border-radius: 999px;
                background: #edf7ed;
                border: 1px solid #b9dfc4;
                color: var(--green-dark);
                font-size: 14px;
                font-weight: 900;
                white-space: nowrap;
                transition: transform 160ms ease, background 160ms ease;
            }

            .input-chip:hover {
                transform: translateY(-1px);
                background: #dcfce7;
            }

            .field-label,
            [data-testid="stWidgetLabel"] p {
                margin: 0 !important;
                color: var(--wood-dark) !important;
                font-size: 14px !important;
                font-weight: 950 !important;
                letter-spacing: 0 !important;
            }

            .field-label {
                margin-bottom: 10px !important;
            }

            .st-key-pgn_input [data-baseweb="textarea"],
            .st-key-pgn_input textarea,
            .depth-value {
                color-scheme: light !important;
                background-color: #fffdf8 !important;
                color: var(--ink) !important;
                -webkit-text-fill-color: var(--ink) !important;
            }

            .st-key-pgn_input [data-baseweb="textarea"] {
                border: 1px solid #cbb79b !important;
                border-radius: 22px !important;
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.58) !important;
                overflow: hidden !important;
                transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease !important;
            }

            .st-key-pgn_input [data-baseweb="textarea"]:focus-within {
                border-color: var(--green) !important;
                box-shadow: 0 0 0 4px rgba(47, 125, 70, 0.14) !important;
                transform: translateY(-1px);
            }

            .st-key-pgn_input textarea {
                min-height: 640px !important;
                padding: 22px 24px !important;
                border: 0 !important;
                font-family: "SFMono-Regular", Consolas, Menlo, monospace !important;
                font-size: 15px !important;
                line-height: 1.68 !important;
                font-weight: 750 !important;
                box-shadow: none !important;
                caret-color: var(--green) !important;
            }

            .st-key-study_setup {
                min-height: 690px;
                padding: 24px;
                border-radius: 26px;
                background:
                    linear-gradient(180deg, #f8eddd 0%, #fffaf1 100%);
                border: 1px solid #d9c4a8;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.62);
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }

            .st-key-study_setup:hover {
                transform: translateY(-2px);
                border-color: #c49d6d;
                box-shadow: 0 18px 42px rgba(76, 52, 31, 0.14), inset 0 1px 0 rgba(255, 255, 255, 0.62);
            }

            .setup-card-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 14px;
                margin-bottom: 16px;
            }

            .setup-kicker {
                margin: 0 0 4px;
                color: var(--green-dark);
                font-size: 12px;
                font-weight: 950;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            .setup-card-head h2 {
                margin: 0;
                color: var(--ink);
                font-size: 22px;
                line-height: 1.15;
                font-weight: 950;
            }

            .setup-mark {
                display: grid;
                place-items: center;
                width: 48px;
                height: 48px;
                border-radius: 16px;
                background: #2b1b12;
                color: #f0c98f;
                font-size: 28px;
                transition: transform 180ms ease, background 180ms ease;
            }

            .st-key-study_setup:hover .setup-mark {
                transform: rotate(-5deg) scale(1.05);
                background: var(--green-dark);
            }

            .side-state {
                display: grid;
                grid-template-columns: 42px 1fr;
                align-items: center;
                gap: 12px;
                min-height: 58px;
                margin: 4px 0 16px;
                padding: 9px 12px;
                border-radius: 16px;
                border: 1px solid #cbb79b;
                background: #fffdf8;
                animation: state-in 220ms ease;
            }

            .side-state span {
                display: grid;
                place-items: center;
                width: 42px;
                height: 42px;
                border-radius: 13px;
                background: var(--green);
                color: #fffaf1;
                font-family: "Times New Roman", "DejaVu Serif", serif;
                font-size: 26px;
                line-height: 1;
            }

            .side-state.black span {
                background: #2b1b12;
                color: #f0c98f;
            }

            .side-state p {
                margin: 0;
                color: var(--muted);
                font-size: 13px;
                line-height: 1.35;
                font-weight: 800;
            }

            .setup-board {
                display: grid;
                grid-template-columns: repeat(8, 1fr);
                aspect-ratio: 1;
                margin-bottom: 20px;
                border: 8px solid #2b1b12;
                border-radius: 18px;
                overflow: hidden;
                background: #f0c98f;
                position: relative;
                box-shadow: 0 14px 30px rgba(43, 27, 18, 0.18);
                transition: transform 220ms ease, box-shadow 220ms ease;
            }

            .setup-board.black-view {
                border-color: #1f160f;
            }

            .setup-board:hover {
                box-shadow: 0 18px 38px rgba(43, 27, 18, 0.22);
            }

            .setup-board span {
                font-size: 24px;
            }

            .st-key-perspective_control,
            .st-key-depth_control {
                margin-bottom: 16px;
            }

            .st-key-perspective_control [data-testid="stWidgetLabel"],
            .st-key-depth_control [data-testid="stWidgetLabel"] {
                margin-bottom: 8px;
            }

            .st-key-perspective_control [data-testid="stSegmentedControl"] {
                width: 100%;
                min-height: 48px;
                padding: 5px;
                border: 1px solid #cbb79b;
                border-radius: 14px;
                background: #fffdf8;
            }

            .st-key-perspective_control [data-testid="stSegmentedControl"] button {
                min-height: 38px !important;
                border: 0 !important;
                border-radius: 10px !important;
                background: transparent !important;
                color: var(--wood-dark) !important;
                -webkit-text-fill-color: var(--wood-dark) !important;
                font-weight: 950 !important;
                box-shadow: none !important;
                transition: background 150ms ease, color 150ms ease, transform 150ms ease !important;
            }

            .st-key-perspective_control [data-testid="stSegmentedControl"] button:hover {
                transform: translateY(-1px);
            }

            .st-key-perspective_control [data-testid="stSegmentedControl"] button p {
                color: inherit !important;
                -webkit-text-fill-color: inherit !important;
                font-weight: 950 !important;
            }

            .st-key-perspective_control [data-testid="stSegmentedControl"] button[aria-pressed="true"],
            .st-key-perspective_control [data-testid="stSegmentedControl"] button[aria-selected="true"] {
                background: var(--green) !important;
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                box-shadow: 0 8px 18px rgba(47, 125, 70, 0.24) !important;
            }

            .st-key-depth_control {
                padding: 0;
            }

            .depth-label {
                margin-bottom: 9px !important;
            }

            .st-key-depth_control [data-testid="stHorizontalBlock"] {
                align-items: stretch;
                gap: 8px;
                min-height: 52px;
                flex-wrap: nowrap !important;
                flex-direction: row !important;
            }

            .st-key-depth_control [data-testid="column"] {
                min-width: 0 !important;
            }

            .st-key-depth_control [data-testid="column"]:nth-child(1),
            .st-key-depth_control [data-testid="column"]:nth-child(3) {
                flex: 0 0 64px !important;
                width: 64px !important;
            }

            .st-key-depth_control [data-testid="column"]:nth-child(2) {
                flex: 1 1 auto !important;
                width: auto !important;
            }

            .depth-value {
                display: flex;
                align-items: center;
                height: 52px;
                padding: 0 18px;
                border: 1px solid #cbb79b;
                border-radius: 14px;
                font-size: 18px;
                font-weight: 950;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.62);
                transition: border-color 150ms ease, box-shadow 150ms ease, transform 150ms ease;
            }

            .st-key-depth_control:hover .depth-value {
                border-color: var(--green);
                box-shadow: 0 0 0 4px rgba(47, 125, 70, 0.10);
            }

            .st-key-depth_decrease button,
            .st-key-depth_increase button {
                height: 52px !important;
                min-height: 52px !important;
                border: 0 !important;
                border-radius: 14px !important;
                background: #2b1b12 !important;
                color: #fffaf1 !important;
                -webkit-text-fill-color: #fffaf1 !important;
                font-size: 22px !important;
                font-weight: 950 !important;
                line-height: 1 !important;
                padding: 0 !important;
                box-shadow: 0 8px 18px rgba(43, 27, 18, 0.15) !important;
                transition: transform 120ms ease, background 120ms ease !important;
            }

            .st-key-depth_increase button {
                background: var(--green-dark) !important;
            }

            .st-key-depth_decrease button:hover,
            .st-key-depth_increase button:hover {
                background: var(--green-dark) !important;
                transform: translateY(-1px);
            }

            .st-key-depth_decrease button:active,
            .st-key-depth_increase button:active {
                transform: translateY(1px) scale(0.98);
            }

            .st-key-analyze_button button {
                height: 52px !important;
                border: 0 !important;
                border-radius: 15px !important;
                background:
                    linear-gradient(135deg, var(--green) 0%, var(--green-dark) 100%) !important;
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-size: 16px !important;
                font-weight: 950 !important;
                box-shadow: 0 14px 28px rgba(47, 125, 70, 0.26) !important;
                transition: transform 150ms ease, box-shadow 150ms ease, filter 150ms ease !important;
            }

            .st-key-analyze_button button:hover {
                transform: translateY(-1px);
                box-shadow: 0 18px 34px rgba(47, 125, 70, 0.30) !important;
                filter: saturate(1.08);
            }

            .st-key-analyze_button button:active {
                transform: translateY(1px) scale(0.995);
            }

            [data-testid="stAlert"] {
                border-radius: 16px;
            }

            iframe {
                border-radius: 28px;
                box-shadow: 0 26px 64px var(--shadow);
                width: 100%;
            }

            @keyframes board-sheen {
                0%, 58% {
                    transform: translateX(-130%);
                }
                74%, 100% {
                    transform: translateX(130%);
                }
            }

            @keyframes state-in {
                from {
                    opacity: 0;
                    transform: translateY(4px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @media (max-width: 900px) {
                .block-container {
                    padding: 12px 10px 38px;
                }

                .app-title {
                    display: block;
                    min-height: auto;
                    padding: 26px 20px 34px;
                    margin-bottom: 18px;
                    border-radius: 22px;
                }

                .app-title h1 {
                    font-size: 31px;
                    line-height: 1.08;
                }

                .app-title p {
                    font-size: 15px;
                    line-height: 1.5;
                }

                .hero-actions {
                    gap: 8px;
                    margin-top: 18px;
                }

                .hero-actions span {
                    min-height: 30px;
                    font-size: 12px;
                }

                .hero-board {
                    display: none;
                }

                .st-key-pgn_input textarea {
                    min-height: 380px !important;
                    font-size: 14px !important;
                    line-height: 1.55 !important;
                    padding: 18px 18px !important;
                }

                .st-key-study_setup {
                    min-height: auto;
                    padding: 18px;
                    border-radius: 22px;
                }

                .st-key-analysis_input_panel {
                    padding: 20px 14px;
                    margin-bottom: 24px;
                    border-radius: 24px;
                }

                .input-head {
                    display: block;
                    margin-bottom: 18px;
                }

                .input-card-title {
                    font-size: 23px;
                }

                .input-card-subtitle {
                    font-size: 14px;
                }

                .input-chip {
                    margin-top: 12px;
                    min-height: 34px;
                    font-size: 13px;
                }

                .setup-card-head {
                    margin-bottom: 12px;
                }

                .setup-card-head h2 {
                    font-size: 20px;
                }

                .setup-mark {
                    width: 42px;
                    height: 42px;
                    border-radius: 14px;
                    font-size: 25px;
                }

                .side-state {
                    grid-template-columns: 40px 1fr;
                    margin-bottom: 14px;
                    padding: 8px 10px;
                }

                .side-state span {
                    width: 40px;
                    height: 40px;
                }

                .side-state p {
                    font-size: 12px;
                }

                .setup-board {
                    width: min(100%, 380px);
                    margin-left: auto;
                    margin-right: auto;
                    border-width: 7px;
                    border-radius: 16px;
                }

                .setup-board span {
                    font-size: clamp(17px, 5.4vw, 24px);
                }

                .st-key-depth_control {
                    margin-bottom: 18px;
                }

                .st-key-depth_control [data-testid="stHorizontalBlock"] {
                    display: flex !important;
                    flex-direction: row !important;
                    flex-wrap: nowrap !important;
                    gap: 8px !important;
                }

                .st-key-depth_control [data-testid="column"]:nth-child(1),
                .st-key-depth_control [data-testid="column"]:nth-child(3) {
                    flex: 0 0 56px !important;
                    width: 56px !important;
                }

                .st-key-depth_control [data-testid="column"]:nth-child(2) {
                    flex: 1 1 auto !important;
                    width: auto !important;
                }

                .depth-value,
                .st-key-depth_decrease button,
                .st-key-depth_increase button,
                .st-key-analyze_button button {
                    height: 50px !important;
                    min-height: 50px !important;
                }

                .st-key-analyze_button button {
                    margin-top: 2px !important;
                }

                iframe {
                    border-radius: 18px;
                    box-shadow: 0 16px 38px var(--shadow);
                }
            }

            @media (min-width: 901px) and (max-width: 1280px) {
                .block-container {
                    padding-left: 26px;
                    padding-right: 26px;
                }

                .app-title {
                    grid-template-columns: minmax(0, 1fr) 260px;
                    gap: 32px;
                    padding: 42px 44px;
                }

                .app-title h1 {
                    font-size: 44px;
                }

                .hero-board {
                    width: 260px;
                }

                .st-key-analysis_input_panel {
                    padding: 28px;
                }

                .setup-board span {
                    font-size: 20px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
