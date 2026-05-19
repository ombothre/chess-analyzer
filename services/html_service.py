from __future__ import annotations

from html import escape


def build_analysis_html(analysis: dict) -> str:
    game = analysis["game"]
    moves = analysis["moves"]
    perspective = game.get("perspective", "White")
    opponent = "Black" if perspective == "White" else "White"
    is_fen = game.get("input_type") == "fen"

    cards_html = ""
    report_title = "FEN position analysis" if is_fen else f"{game['white']} vs {game['black']}"
    hero_meta = (
        f"""
            <p><strong>Side to move:</strong> {escape(game.get("side_to_move", "Unknown"))}</p>
            <p><strong>Input:</strong> FEN position</p>
            <p><strong>Perspective:</strong> {escape(perspective)}</p>
        """
        if is_fen
        else f"""
            <p><strong>Event:</strong> {escape(game["event"])}</p>
            <p><strong>Result:</strong> {escape(game["result"])}</p>
            <p><strong>Perspective:</strong> {escape(perspective)}</p>
        """
    )
    summary_copy = (
        """
            This report analyzes only the current FEN position. The green arrow is
            Stockfish's preferred move for the side to move.
        """
        if is_fen
        else """
            Each card shows the board after the played move. The blue arrow is the actual move.
            The green arrow is Stockfish's preferred move from the same position.
        """
    )
    legend_html = (
        '<p><span class="line green"></span>Green arrow = engine best move</p>'
        if is_fen
        else """
            <p><span class="line blue"></span>Blue arrow = played move</p>
            <p><span class="line green"></span>Green arrow = engine best move</p>
        """
    )

    for move in moves:
        move_kicker = "FEN position" if is_fen else f"Move {move['index']}"
        summary_label = f"Best for {game.get('side_to_move', 'side to move')}" if is_fen else "Engine best"
        details_summary = "Input FEN" if is_fen else "FEN after move"

        if is_fen:
            table_html = f"""
                        <tr>
                            <th>Side to move</th>
                            <td><code>{escape(move["played_san"])}</code></td>
                        </tr>
                        <tr>
                            <th>Engine best</th>
                            <td><code>{escape(move["best_san"])}</code></td>
                        </tr>
                        <tr>
                            <th>Current eval</th>
                            <td>{escape(move["eval_before"])}</td>
                        </tr>
                        <tr>
                            <th>After best</th>
                            <td>{escape(move["eval_after"])}</td>
                        </tr>
            """
        else:
            table_html = f"""
                        <tr>
                            <th>Played move</th>
                            <td><code>{escape(move["played_san"])}</code></td>
                        </tr>
                        <tr>
                            <th>Engine best</th>
                            <td><code>{escape(move["best_san"])}</code></td>
                        </tr>
                        <tr>
                            <th>Eval before</th>
                            <td>{escape(move["eval_before"])}</td>
                        </tr>
                        <tr>
                            <th>Eval after</th>
                            <td>{escape(move["eval_after"])}</td>
                        </tr>
            """

        cards_html += f"""
        <article class="analysis-card {move["label_class"]}">
            <div class="card-header">
                <div>
                    <p class="move-kicker">{escape(move_kicker)}</p>
                    <h2>{escape(move["move_title"])}</h2>
                    <p class="subtle">{escape(summary_label)}: <strong>{escape(move["best_san"])}</strong></p>
                </div>
                <span class="badge {move["label_class"]}">{escape(move["label"])}</span>
            </div>

            <div class="card-body">
                <div class="board-frame">
                    <div class="board-wrap">
                        {move["board_svg"]}
                    </div>
                </div>

                <div class="details">
                    <table>
                        {table_html}
                    </table>

                    <div class="explanation">
                        <h3>Coach explanation</h3>
                        <p>{move["explanation"]}</p>
                    </div>

                    <details>
                        <summary>{escape(details_summary)}</summary>
                        <code class="fen">{escape(move["fen_after"])}</code>
                    </details>
                </div>
            </div>
        </article>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<style>
    :root {{
        --bg: #f3eee4;
        --paper: #fffaf1;
        --paper-2: #f8eddd;
        --ink: #1f2933;
        --muted: #6b6258;
        --wood: #9a673d;
        --wood-dark: #4b2f1d;
        --green: #2f7d46;
        --green-dark: #1f5c35;
        --line: #dccbb5;
        --shadow: rgba(76, 52, 31, 0.18);
        --blue: #2563eb;
    }}

    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        padding: 0;
        background:
            linear-gradient(45deg, rgba(154, 103, 61, 0.045) 25%, transparent 25%),
            linear-gradient(-45deg, rgba(154, 103, 61, 0.045) 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, rgba(154, 103, 61, 0.045) 75%),
            linear-gradient(-45deg, transparent 75%, rgba(154, 103, 61, 0.045) 75%),
            linear-gradient(180deg, #fbf7ef 0%, var(--bg) 100%);
        background-size: 72px 72px, 72px 72px, 72px 72px, 72px 72px, auto;
        background-position: 0 0, 0 36px, 36px -36px, -36px 0, 0 0;
        color: var(--ink);
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    .analysis-root {{
        max-width: 1280px;
        margin: 0 auto;
        padding: 10px 12px 80px;
        overflow-x: hidden;
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 82% 16%, rgba(248, 215, 154, 0.18), transparent 20rem),
            linear-gradient(135deg, #2b1b12 0%, #163321 58%, #0f1f17 100%);
        color: #fffaf1;
        border: 1px solid rgba(255, 250, 241, 0.16);
        border-radius: 28px;
        padding: 34px 38px 42px;
        margin-bottom: 24px;
        box-shadow: 0 26px 64px var(--shadow);
    }}

    .hero::after {{
        content: "";
        position: absolute;
        inset: auto 0 0 0;
        height: 8px;
        background: linear-gradient(90deg, var(--wood), #d7a15f, var(--green));
    }}

    .hero .eyebrow {{
        display: inline-flex;
        align-items: center;
        min-height: 30px;
        padding: 0 12px;
        border-radius: 999px;
        background: rgba(255, 250, 241, 0.12);
        border: 1px solid rgba(255, 250, 241, 0.20);
        color: #f8d79a;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .hero h1 {{
        margin: 16px 0 14px;
        color: #fffaf1;
        font-size: 42px;
        line-height: 1.05;
        letter-spacing: 0;
    }}

    .hero-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px 16px;
    }}

    .hero p {{
        margin: 0;
        color: #eadfcf;
        font-size: 15px;
        font-weight: 700;
    }}

    .hero strong {{
        color: #fffaf1;
    }}

    .summary {{
        background: rgba(255, 250, 241, 0.94);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 24px 26px;
        margin-bottom: 24px;
        box-shadow: 0 18px 44px var(--shadow);
    }}

    .summary h2 {{
        margin: 0 0 10px;
        color: var(--ink);
        font-size: 24px;
    }}

    .summary p {{
        margin: 10px 0;
        line-height: 1.65;
        color: var(--muted);
        font-weight: 650;
    }}

    .legend {{
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        background: #f8eddd;
        border: 1px solid #ead8be;
        border-radius: 18px;
        padding: 13px 16px;
        margin-top: 16px;
    }}

    .legend p {{
        margin: 0;
        color: var(--ink);
    }}

    .line {{
        display: inline-block;
        width: 38px;
        height: 6px;
        border-radius: 999px;
        margin-right: 9px;
        vertical-align: middle;
    }}

    .blue {{
        background: var(--blue);
    }}

    .green {{
        background: var(--green);
    }}

    .analysis-card {{
        background: rgba(255, 250, 241, 0.96);
        border-radius: 26px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 24px 60px var(--shadow);
        border: 1px solid var(--line);
        border-left: 10px solid #9ca3af;
    }}

    .analysis-card.ok {{
        border-left-color: #22c55e;
    }}

    .analysis-card.inaccuracy {{
        border-left-color: #eab308;
    }}

    .analysis-card.mistake {{
        border-left-color: #f97316;
    }}

    .analysis-card.blunder {{
        border-left-color: #ef4444;
    }}

    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
        margin-bottom: 18px;
    }}

    .move-kicker {{
        margin: 0 0 4px;
        color: var(--green-dark);
        font-size: 12px;
        font-weight: 950;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .card-header h2 {{
        margin: 0 0 5px;
        color: var(--ink);
        font-size: 28px;
        line-height: 1.1;
    }}

    .subtle {{
        margin: 0;
        color: var(--muted);
        font-weight: 650;
    }}

    .badge {{
        border-radius: 999px;
        padding: 9px 15px;
        font-weight: 950;
        background: #f8eddd;
        color: var(--wood-dark);
        white-space: nowrap;
    }}

    .badge.ok {{
        background: #dcfce7;
        color: #166534;
    }}

    .badge.inaccuracy {{
        background: #fef3c7;
        color: #92400e;
    }}

    .badge.mistake {{
        background: #ffedd5;
        color: #9a3412;
    }}

    .badge.blunder {{
        background: #fee2e2;
        color: #991b1b;
    }}

    .card-body {{
        display: grid;
        grid-template-columns: 500px 1fr;
        gap: 30px;
        align-items: start;
    }}

    .board-frame {{
        max-width: 500px;
        width: 100%;
        padding: 14px;
        border-radius: 24px;
        background:
            linear-gradient(180deg, #4b2f1d 0%, #2b1b12 100%);
        box-shadow: inset 0 1px 0 rgba(255, 250, 241, 0.15);
    }}

    .board-wrap {{
        border-radius: 16px;
        overflow: hidden;
        background: #2b1b12;
    }}

    .board-wrap svg {{
        display: block;
        width: 100%;
        height: auto;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 18px;
        overflow: hidden;
        border-radius: 18px;
        background: #fffdf8;
        border: 1px solid #ead8be;
    }}

    th, td {{
        text-align: left;
        padding: 13px 14px;
        border-bottom: 1px solid #ead8be;
    }}

    tr:last-child th,
    tr:last-child td {{
        border-bottom: 0;
    }}

    th {{
        width: 155px;
        background: #f8eddd;
        color: var(--wood-dark);
        font-weight: 950;
    }}

    td {{
        color: var(--ink);
        font-weight: 700;
    }}

    code {{
        background: #f2eadf;
        color: var(--ink);
        padding: 3px 7px;
        border-radius: 7px;
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: 13px;
    }}

    .explanation {{
        background: linear-gradient(180deg, #f8eddd 0%, #fffaf1 100%);
        border: 1px solid #ead8be;
        border-radius: 18px;
        padding: 17px 18px;
        margin-bottom: 16px;
    }}

    .explanation h3 {{
        margin: 0 0 8px;
        color: var(--ink);
        font-size: 19px;
    }}

    .explanation p {{
        margin: 0;
        line-height: 1.65;
        color: var(--muted);
        font-weight: 650;
    }}

    details {{
        color: var(--muted);
        font-weight: 700;
    }}

    .fen {{
        display: block;
        margin-top: 10px;
        word-break: break-all;
    }}

    @media (max-width: 900px) {{
        .analysis-root {{
            padding: 6px 6px 44px;
        }}

        .hero {{
            padding: 24px 20px 32px;
            border-radius: 22px;
            margin-bottom: 16px;
        }}

        .hero h1 {{
            font-size: 28px;
        }}

        .hero-grid {{
            display: grid;
            gap: 7px;
        }}

        .summary {{
            padding: 18px 16px;
            border-radius: 20px;
            margin-bottom: 18px;
        }}

        .summary h2 {{
            font-size: 21px;
        }}

        .summary p {{
            font-size: 14px;
            line-height: 1.55;
        }}

        .legend {{
            gap: 10px;
            padding: 12px;
        }}

        .card-body {{
            grid-template-columns: 1fr;
            gap: 18px;
        }}

        .analysis-card {{
            padding: 18px 14px;
            border-radius: 22px;
            margin-bottom: 18px;
            border-left-width: 7px;
        }}

        .card-header {{
            gap: 12px;
            margin-bottom: 14px;
        }}

        .card-header h2 {{
            font-size: 23px;
        }}

        .badge {{
            padding: 7px 11px;
            font-size: 13px;
        }}

        .board-frame {{
            max-width: 100%;
            padding: 8px;
            border-radius: 18px;
        }}

        .board-wrap {{
            border-radius: 12px;
        }}

        th, td {{
            display: block;
            width: 100%;
            padding: 10px 12px;
        }}

        th {{
            border-bottom: 0;
        }}

        td {{
            padding-top: 0;
        }}

        .explanation {{
            padding: 14px;
            border-radius: 15px;
        }}

        .explanation h3 {{
            font-size: 17px;
        }}

        .explanation p {{
            font-size: 14px;
            line-height: 1.55;
        }}
    }}

    @media (min-width: 901px) and (max-width: 1180px) {{
        .card-body {{
            grid-template-columns: minmax(360px, 460px) 1fr;
            gap: 24px;
        }}
    }}
</style>
</head>
<body>
<div class="analysis-root">
    <section class="hero">
        <span class="eyebrow">Analysis report</span>
        <h1>{escape(report_title)}</h1>
        <div class="hero-grid">
            {hero_meta}
        </div>
    </section>

    <section class="summary">
        <h2>How to read this analysis</h2>
        <p>
            {summary_copy}
        </p>
        <p>
            Evaluations are from {escape(perspective)}'s perspective.
            <code>+1.00</code> means {escape(perspective)} is about one pawn better.
            <code>-1.00</code> means {escape(opponent)} is about one pawn better.
        </p>
        <div class="legend">
            {legend_html}
        </div>
    </section>

    {cards_html}
</div>
</body>
</html>
"""
