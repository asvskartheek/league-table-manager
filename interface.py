"""Gradio UI: builds the full multi-tab interface."""
import gradio as gr

import data
from data import load_matches, get_teams_from_matches
from renderers import (
    render_league_table_html,
    render_match_history_html,
    render_stat_cards,
    render_h2h_stats_html,
    get_h2h_match_history_html,
    make_status,
    update_score_preview,
)
from crud import add_match, delete_match_by_id, update_match


def build_interface():
    """Build and return the Gradio Blocks demo."""
    load_matches()
    initial_teams = get_teams_from_matches()

    with gr.Blocks(title="League Table Manager") as demo:

        # ── App header ──────────────────────────────────
        gr.HTML("""
        <div style="padding:20px 0 8px; font-family:Inter,sans-serif;">
            <h1 style="font-size:1.9rem; font-weight:900; color:#f1f5f9; letter-spacing:-0.03em; margin:0;">
                ⚽ League Table Manager
            </h1>
            <p style="color:#64748b; margin:4px 0 0; font-size:0.85rem;">Track matches, standings, and head-to-head records</p>
        </div>
        """)

        with gr.Tabs():

            # ── Tab 1: Standings ─────────────────────────
            with gr.Tab("Standings"):
                gr.HTML("<h2 style='color:#f1f5f9; font-size:1.1rem; font-weight:700; margin:8px 0 4px; font-family:Inter,sans-serif;'>Current Standings</h2>")
                standings_html = gr.HTML(value=render_league_table_html(data.matches))

                with gr.Accordion("Column Guide", open=False):
                    gr.Markdown("""
| Column | Meaning |
|--------|---------|
| Win Rate | Win percentage (wins / games played) |
| P | Matches played |
| W | Wins |
| D | Draws |
| L | Losses |
| GF | Goals scored (Goals For) |
| GA | Goals conceded (Goals Against) |
| GD | Goal difference (GF − GA) |
| Pts | League points (W=3, D=1, L=0) |
| G/GM | Goals scored per match |
| WW | Whitewash wins (opponent scored 0) |
| 5G | Matches where you scored 5 or more |
                    """)

            # ── Tab 2: Add Match ─────────────────────────
            with gr.Tab("Add Match"):
                with gr.Row():
                    # Left: Add Match form
                    with gr.Column(scale=1, min_width=280):
                        gr.HTML("<h2 style='color:#f1f5f9; font-size:1rem; font-weight:700; margin:4px 0 12px; font-family:Inter,sans-serif;'>Add Match</h2>")

                        score_preview = gr.HTML(value="""
                        <div style="text-align:center; padding:16px; background:#0f172a; border-radius:12px;
                                    border:1px solid #334155; color:#64748b; font-style:italic; font-family:Inter,sans-serif; font-size:0.85rem;">
                            Select teams and enter goals to preview
                        </div>
                        """)

                        home_team = gr.Dropdown(
                            choices=initial_teams,
                            label="Home Team",
                            value=initial_teams[0] if initial_teams else None,
                            allow_custom_value=True
                        )
                        away_team = gr.Dropdown(
                            choices=initial_teams,
                            label="Away Team",
                            value=initial_teams[1] if len(initial_teams) > 1 else None,
                            allow_custom_value=True
                        )

                        with gr.Row():
                            home_goals = gr.Number(label="Home Goals", value=0, minimum=0, precision=0)
                            away_goals = gr.Number(label="Away Goals", value=0, minimum=0, precision=0)

                        submit_btn = gr.Button("Add Match", variant="primary")
                        status_html = gr.HTML(value="")

                    # Right: Match history
                    with gr.Column(scale=2):
                        gr.HTML("<h2 style='color:#f1f5f9; font-size:1rem; font-weight:700; margin:4px 0 12px; font-family:Inter,sans-serif;'>Match History</h2>")
                        matches_html = gr.HTML(value=render_match_history_html(data.matches))

                        # Delete accordion
                        with gr.Accordion("Delete a Match", open=False):
                            gr.Markdown("Enter the row number from the history above, or click a row to auto-fill.")
                            delete_preview_html = gr.HTML(value="")
                            with gr.Row():
                                delete_row_input = gr.Number(
                                    label="Row # to Delete",
                                    value=None,
                                    minimum=1,
                                    precision=0,
                                    scale=2
                                )
                                stage_delete_btn = gr.Button("Preview Delete", variant="secondary", scale=1)
                            confirm_delete_btn = gr.Button("Confirm Delete", variant="stop", visible=False)
                            pending_match_id = gr.State(None)

                        # Edit accordion
                        with gr.Accordion("Edit a Match", open=False):
                            gr.Markdown("Enter the row number to edit, fill in the new values, then click Save.")
                            update_row_input = gr.Number(label="Row # to Edit", value=None, minimum=1, precision=0)
                            with gr.Row():
                                update_home_team = gr.Dropdown(
                                    choices=initial_teams,
                                    label="New Home Team",
                                    allow_custom_value=True
                                )
                                update_away_team = gr.Dropdown(
                                    choices=initial_teams,
                                    label="New Away Team",
                                    allow_custom_value=True
                                )
                            with gr.Row():
                                update_home_goals = gr.Number(label="Home Goals", value=0, minimum=0, precision=0)
                                update_away_goals = gr.Number(label="Away Goals", value=0, minimum=0, precision=0)
                            update_btn = gr.Button("Save Changes", variant="secondary")
                            update_status_html = gr.HTML(value="")

                # ── Score preview events ──
                for component in [home_team, away_team, home_goals, away_goals]:
                    component.change(
                        fn=update_score_preview,
                        inputs=[home_team, away_team, home_goals, away_goals],
                        outputs=[score_preview]
                    )

                # ── Add Match ──
                def add_match_full(home, away, hg, ag):
                    status = add_match(home, away, hg, ag)
                    teams = get_teams_from_matches()
                    return (
                        render_league_table_html(data.matches),
                        render_match_history_html(data.matches),
                        make_status(status),
                        gr.Number(value=0),
                        gr.Number(value=0),
                        gr.Dropdown(choices=teams),
                        gr.Dropdown(choices=teams),
                        gr.Dropdown(choices=teams),
                        gr.Dropdown(choices=teams),
                    )

                submit_btn.click(
                    fn=add_match_full,
                    inputs=[home_team, away_team, home_goals, away_goals],
                    outputs=[standings_html, matches_html, status_html,
                             home_goals, away_goals,
                             home_team, away_team,
                             update_home_team, update_away_team],
                    show_progress="minimal"
                )

                # ── Two-step Delete ──
                def stage_delete(row_number):
                    if row_number is None or row_number < 1:
                        return (
                            '<div style="padding:10px; background:#fee2e2; border-left:4px solid #dc2626; border-radius:6px; color:#991b1b; font-family:Inter,sans-serif;">✗ Invalid row number</div>',
                            None,
                            gr.update(visible=False)
                        )
                    sorted_m = sorted(data.matches, key=lambda x: x[5], reverse=True)
                    row_idx = int(row_number) - 1
                    if row_idx < 0 or row_idx >= len(sorted_m):
                        return (
                            f'<div style="padding:10px; background:#fee2e2; border-left:4px solid #dc2626; border-radius:6px; color:#991b1b; font-family:Inter,sans-serif;">✗ Row {int(row_number)} does not exist</div>',
                            None,
                            gr.update(visible=False)
                        )
                    m = sorted_m[row_idx]
                    preview = f"""
                    <div style="padding:12px; background:#7f1d1d20; border:1px solid #dc2626; border-radius:8px; color:#fca5a5; font-family:Inter,sans-serif;">
                        About to delete row <strong>{int(row_number)}</strong>:
                        <strong>{m[1]} {m[3]} – {m[4]} {m[2]}</strong><br>
                        <small style="color:#94a3b8;">Click <em>Confirm Delete</em> to proceed.</small>
                    </div>
                    """
                    return preview, m[0], gr.update(visible=True)

                stage_delete_btn.click(
                    fn=stage_delete,
                    inputs=[delete_row_input],
                    outputs=[delete_preview_html, pending_match_id, confirm_delete_btn]
                )

                def execute_delete(match_id):
                    if match_id is None:
                        return (
                            render_league_table_html(data.matches),
                            render_match_history_html(data.matches),
                            make_status("Error: No match staged for deletion"),
                            "",
                            None,
                            gr.update(visible=False)
                        )
                    ok = delete_match_by_id(match_id)
                    status = "Match deleted successfully" if ok else "Error: Failed to delete match"
                    return (
                        render_league_table_html(data.matches),
                        render_match_history_html(data.matches),
                        make_status(status),
                        "",
                        None,
                        gr.update(visible=False)
                    )

                confirm_delete_btn.click(
                    fn=execute_delete,
                    inputs=[pending_match_id],
                    outputs=[standings_html, matches_html, status_html,
                             delete_preview_html, pending_match_id, confirm_delete_btn],
                    show_progress="minimal"
                )

                # ── Edit Match ──
                def update_match_full(row_number, new_home, new_away, new_home_goals, new_away_goals):
                    status = update_match(row_number, new_home, new_away, new_home_goals, new_away_goals)
                    teams = get_teams_from_matches()
                    return (
                        render_league_table_html(data.matches),
                        render_match_history_html(data.matches),
                        make_status(status),
                        gr.Dropdown(choices=teams),
                        gr.Dropdown(choices=teams),
                        gr.Dropdown(choices=teams),
                        gr.Dropdown(choices=teams),
                    )

                update_btn.click(
                    fn=update_match_full,
                    inputs=[update_row_input, update_home_team, update_away_team,
                            update_home_goals, update_away_goals],
                    outputs=[standings_html, matches_html, update_status_html,
                             home_team, away_team,
                             update_home_team, update_away_team],
                    show_progress="minimal"
                )

            # ── Tab 3: Head to Head ──────────────────────
            with gr.Tab("Head to Head"):
                gr.HTML("<h2 style='color:#f1f5f9; font-size:1.1rem; font-weight:700; margin:8px 0 16px; font-family:Inter,sans-serif;'>Head-to-Head Comparison</h2>")

                with gr.Row():
                    h2h_team1 = gr.Dropdown(
                        choices=initial_teams,
                        label="Team 1",
                        value=initial_teams[0] if initial_teams else None,
                        allow_custom_value=True,
                        scale=1
                    )
                    h2h_team2 = gr.Dropdown(
                        choices=initial_teams,
                        label="Team 2",
                        value=initial_teams[1] if len(initial_teams) > 1 else None,
                        allow_custom_value=True,
                        scale=1
                    )

                h2h_stats_html = gr.HTML(
                    value=render_h2h_stats_html(
                        initial_teams[0] if initial_teams else None,
                        initial_teams[1] if len(initial_teams) > 1 else None,
                        data.matches
                    )
                )

                gr.HTML("<h3 style='color:#94a3b8; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin:20px 0 8px; font-family:Inter,sans-serif;'>Match History</h3>")

                h2h_history_html = gr.HTML(
                    value=get_h2h_match_history_html(
                        initial_teams[0] if initial_teams else None,
                        initial_teams[1] if len(initial_teams) > 1 else None,
                        data.matches
                    )
                )

                def update_h2h(t1, t2):
                    return (
                        render_h2h_stats_html(t1, t2, data.matches),
                        get_h2h_match_history_html(t1, t2, data.matches)
                    )

                h2h_team1.change(fn=update_h2h, inputs=[h2h_team1, h2h_team2], outputs=[h2h_stats_html, h2h_history_html])
                h2h_team2.change(fn=update_h2h, inputs=[h2h_team1, h2h_team2], outputs=[h2h_stats_html, h2h_history_html])

            # ── Tab 4: Records ───────────────────────────
            with gr.Tab("Records"):
                gr.HTML("<h2 style='color:#f1f5f9; font-size:1.1rem; font-weight:700; margin:8px 0 16px; font-family:Inter,sans-serif;'>League Records</h2>")
                records_html = gr.HTML(value=render_stat_cards(data.matches))

        # ── Page load refresh ──
        def refresh_all():
            load_matches()
            teams = get_teams_from_matches()
            t1 = teams[0] if teams else None
            t2 = teams[1] if len(teams) > 1 else None
            return (
                render_league_table_html(data.matches),
                render_match_history_html(data.matches),
                render_h2h_stats_html(t1, t2, data.matches),
                get_h2h_match_history_html(t1, t2, data.matches),
                render_stat_cards(data.matches),
                gr.Dropdown(choices=teams),
                gr.Dropdown(choices=teams),
                gr.Dropdown(choices=teams),
                gr.Dropdown(choices=teams),
                gr.Dropdown(choices=teams),
                gr.Dropdown(choices=teams),
            )

        demo.load(
            fn=refresh_all,
            inputs=[],
            outputs=[
                standings_html, matches_html,
                h2h_stats_html, h2h_history_html,
                records_html,
                home_team, away_team,
                update_home_team, update_away_team,
                h2h_team1, h2h_team2,
            ]
        )

    return demo
