"""HTML rendering functions for each UI section of the League Table Manager."""
from data import calculate_table, format_datetime


# ─────────────────────────────────────────────
# League Table (Standings)
# ─────────────────────────────────────────────

def render_league_table_html(matches_list):
    """Render the league standings as a styled HTML table with medal highlights."""
    if not matches_list:
        return '<div style="padding:24px; text-align:center; color:#64748b;">No matches yet. Add some matches to see the standings.</div>'

    df = calculate_table(matches_list)
    df = df.reset_index(drop=True)

    def _rank_map(series, ascending=False):
        vals = sorted(set(series.tolist()), reverse=not ascending)
        return {v: (vals.index(v) + 1) for v in vals}

    def _medal_style(rank, fallback="#94a3b8", big=False):
        size = "1.1rem" if big else "1.0rem"
        small = "1.1rem" if big else "0.82rem"
        if rank == 1:
            return f"font-weight:900; font-size:{size}; color:#f59e0b; text-shadow:0 0 10px #f59e0baa, 0 0 3px #fbbf24;"
        elif rank == 2:
            return f"font-weight:800; font-size:{size}; color:#b0b8c4;"
        elif rank == 3:
            return f"font-weight:800; font-size:{size}; color:#cd7f32;"
        else:
            return f"font-size:{small}; color:{fallback};"

    wp_rm  = _rank_map(df['WP'])
    p_rm   = _rank_map(df['P'])
    gf_rm  = _rank_map(df['GF'])
    gpm_rm = _rank_map(df['GPM'])
    gam_rm = _rank_map(df['GAM'], ascending=True)  # lowest GAM is best
    gdm_rm = _rank_map(df['GDM'])
    w_rm   = _rank_map(df['W'])
    ww_rm  = _rank_map(df['#WW'])
    fg_rm  = _rank_map(df['#5GM'])

    rows_html = ""
    for i, row in df.iterrows():
        rank = i + 1
        wp = row["WP"]
        gdm = row["GDM"]

        if wp >= 60:
            row_style = "background:rgba(34,197,94,0.07); border-left:3px solid #22c55e;"
        elif wp >= 40:
            row_style = "background:rgba(234,179,8,0.07); border-left:3px solid #eab308;"
        else:
            row_style = "background:rgba(239,68,68,0.07); border-left:3px solid #ef4444;"

        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"<span style='color:#64748b'>#{rank}</span>")

        gdm_fallback = '#22c55e' if gdm > 0 else ('#ef4444' if gdm < 0 else '#94a3b8')

        wp_sty  = _medal_style(wp_rm[wp])
        p_sty   = _medal_style(p_rm[row['P']])
        gf_sty  = _medal_style(gf_rm[row['GF']], big=True)
        gpm_sty = _medal_style(gpm_rm[row['GPM']])
        gam_sty = _medal_style(gam_rm[row['GAM']])
        gdm_sty = _medal_style(gdm_rm[gdm], fallback=gdm_fallback)
        w_sty   = _medal_style(w_rm[row['W']], fallback='#22c55e')
        ww_sty  = _medal_style(ww_rm[row['#WW']])
        fg_sty  = _medal_style(fg_rm[row['#5GM']])

        rows_html += f"""
        <tr style="{row_style}" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
            <td style="padding:10px 8px; font-weight:700; text-align:center;">{medal}</td>
            <td style="padding:10px 8px; font-weight:600; color:#f1f5f9; white-space:nowrap;">{row['Team']}</td>
            <td style="padding:10px 8px; text-align:center; {wp_sty}">{wp}%</td>
            <td style="padding:10px 8px; text-align:center; {p_sty}">{row['P']}</td>
            <td style="padding:10px 8px; text-align:center; {gf_sty}">{row['GF']}</td>
            <td style="padding:10px 8px; text-align:center; {gpm_sty}">{row['GPM']}</td>
            <td style="padding:10px 8px; text-align:center; {gam_sty}">{row['GAM']}</td>
            <td style="padding:10px 8px; text-align:center; {gdm_sty}">{row['GDM']}</td>
            <td style="padding:10px 8px; text-align:center; {w_sty}font-weight:600;">{row['W']}</td>
            <td style="padding:10px 8px; text-align:center; color:#94a3b8;">{row['D']}</td>
            <td style="padding:10px 8px; text-align:center; color:#ef4444; font-weight:600;">{row['L']}</td>
            <td style="padding:10px 8px; text-align:center; {ww_sty}">{row['#WW']}</td>
            <td style="padding:10px 8px; text-align:center; {fg_sty}">{row['#5GM']}</td>
        </tr>
        """

    def th(label, color="#94a3b8", align="center"):
        return f'<th style="padding:10px 8px; text-align:{align}; color:{color}; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; white-space:nowrap;">{label}</th>'

    return f"""
    <div style="overflow-x:auto; border-radius:12px; border:1px solid #334155; font-family:Inter,ui-sans-serif,sans-serif;">
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr style="background:#0f172a; border-bottom:2px solid #22c55e;">
                    {th('#', '#22c55e')}
                    {th('Team', '#22c55e', 'left')}
                    {th('WR%')}
                    {th('P')}
                    {th('Goals', '#f59e0b')}
                    {th('GPM')}
                    {th('GAM')}
                    {th('GDM')}
                    {th('W', '#22c55e')}
                    {th('D')}
                    {th('L', '#ef4444')}
                    {th('WW')}
                    {th('5G')}
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """


# ─────────────────────────────────────────────
# Match History
# ─────────────────────────────────────────────

def render_match_history_html(matches_list):
    """Render all match results as a color-coded scrollable HTML table."""
    if not matches_list:
        return '<div style="padding:24px; text-align:center; color:#64748b; font-family:Inter,sans-serif;">No matches yet.</div>'

    sorted_matches = sorted(matches_list, key=lambda x: x[5], reverse=True)

    rows = ""
    for i, match in enumerate(sorted_matches, 1):
        match_id, h, a, gh, ga, dt = match
        formatted_dt = format_datetime(dt)

        if gh > ga:
            h_color, a_color = "#22c55e", "#ef4444"
            result_label = f"{h} WIN"
            result_color = "#22c55e"
        elif ga > gh:
            h_color, a_color = "#ef4444", "#22c55e"
            result_label = f"{a} WIN"
            result_color = "#22c55e"
        else:
            h_color = a_color = "#eab308"
            result_label = "DRAW"
            result_color = "#eab308"

        rows += f"""
        <tr style="border-bottom:1px solid #334155;">
            <td style="padding:8px 10px; color:#64748b; font-size:0.78rem; text-align:center;">{i}</td>
            <td style="padding:8px 10px; color:#64748b; font-size:0.73rem; white-space:nowrap;">{formatted_dt}</td>
            <td style="padding:8px 10px; font-weight:600; color:#f1f5f9; text-align:right; white-space:nowrap;">{h}</td>
            <td style="padding:8px 12px; text-align:center; white-space:nowrap;">
                <span style="color:{h_color}; font-weight:800; font-size:1rem;">{gh}</span>
                <span style="color:#475569; margin:0 4px;">–</span>
                <span style="color:{a_color}; font-weight:800; font-size:1rem;">{ga}</span>
            </td>
            <td style="padding:8px 10px; font-weight:600; color:#f1f5f9; white-space:nowrap;">{a}</td>
            <td style="padding:8px 10px; text-align:center;">
                <span style="font-size:0.65rem; font-weight:700; color:{result_color}; background:{result_color}18;
                             padding:2px 6px; border-radius:4px; text-transform:uppercase; letter-spacing:0.05em;">{result_label}</span>
            </td>
        </tr>
        """

    return f"""
    <div style="overflow-x:auto; border-radius:12px; border:1px solid #334155; font-family:Inter,ui-sans-serif,sans-serif;">
        <div style="overflow-y:auto; max-height:450px;">
            <table style="width:100%; border-collapse:collapse;">
                <thead style="position:sticky; top:0; z-index:1;">
                    <tr style="background:#0f172a; border-bottom:2px solid #22c55e;">
                        <th style="padding:8px 10px; color:#94a3b8; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; text-align:center;">#</th>
                        <th style="padding:8px 10px; color:#94a3b8; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; text-align:left;">Date</th>
                        <th style="padding:8px 10px; color:#22c55e; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; text-align:right;">Home</th>
                        <th style="padding:8px 10px; color:#22c55e; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; text-align:center;">Score</th>
                        <th style="padding:8px 10px; color:#22c55e; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em;">Away</th>
                        <th style="padding:8px 10px; color:#94a3b8; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; text-align:center;">Result</th>
                    </tr>
                </thead>
                <tbody style="background:#1e293b;">
                    {rows}
                </tbody>
            </table>
        </div>
    </div>
    """


# ─────────────────────────────────────────────
# Records / Stat Cards
# ─────────────────────────────────────────────

def render_stat_cards(matches_list):
    """Render league-wide records as a grid of styled stat cards."""
    if not matches_list:
        return '<div style="padding:24px; text-align:center; color:#64748b; font-family:Inter,sans-serif;">No matches yet.</div>'

    highest_aggregate = 0
    highest_aggregate_match = None
    biggest_margin = 0
    biggest_margin_match = None
    most_goals_one_side = 0
    most_goals_one_side_match = None
    most_goals_one_side_team = None
    total_goals = 0
    total_matches = len(matches_list)

    sorted_matches = sorted(matches_list, key=lambda x: x[5])

    cumulative_goals = {}
    first_to_100 = None
    first_to_500 = None

    team_results = {}

    for match in matches_list:
        match_id, h, a, gh, ga, dt = match[0], match[1], match[2], match[3], match[4], match[5]
        total_goals += gh + ga
        aggregate = gh + ga
        if aggregate > highest_aggregate:
            highest_aggregate = aggregate
            highest_aggregate_match = match

        margin = abs(gh - ga)
        if margin > biggest_margin:
            biggest_margin = margin
            biggest_margin_match = match

        if gh > most_goals_one_side:
            most_goals_one_side = gh
            most_goals_one_side_match = match
            most_goals_one_side_team = h
        if ga > most_goals_one_side:
            most_goals_one_side = ga
            most_goals_one_side_match = match
            most_goals_one_side_team = a

    for match in sorted_matches:
        match_id, h, a, gh, ga = match[0], match[1], match[2], match[3], match[4]

        cumulative_goals[h] = cumulative_goals.get(h, 0) + gh
        cumulative_goals[a] = cumulative_goals.get(a, 0) + ga

        if first_to_100 is None:
            if cumulative_goals[h] >= 100:
                first_to_100 = h
            elif cumulative_goals[a] >= 100:
                first_to_100 = a

        if first_to_500 is None:
            if cumulative_goals[h] >= 500:
                first_to_500 = h
            elif cumulative_goals[a] >= 500:
                first_to_500 = a

        team_results.setdefault(h, [])
        team_results.setdefault(a, [])
        if gh > ga:
            team_results[h].append('W')
            team_results[a].append('L')
        elif ga > gh:
            team_results[a].append('W')
            team_results[h].append('L')
        else:
            team_results[h].append('D')
            team_results[a].append('D')

    longest_streak = 0
    longest_streak_team = None
    for team, results in team_results.items():
        current = 0
        for r in results:
            if r == 'W':
                current += 1
                if current > longest_streak:
                    longest_streak = current
                    longest_streak_team = team
            else:
                current = 0

    def fmt(m):
        if m is None:
            return "—"
        return f"{m[1]} {m[3]}–{m[4]} {m[2]}"

    avg_goals = round(total_goals / total_matches, 1) if total_matches > 0 else 0

    def card(icon, label, value, sub, color, vsize="2.2rem"):
        return f"""
    <div style="background:#1e293b; border-radius:12px; padding:20px 16px; border:1px solid #334155; text-align:center; font-family:Inter,sans-serif;">
        <div style="font-size:1.6rem; margin-bottom:4px;">{icon}</div>
        <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">{label}</div>
        <div style="color:{color}; font-size:{vsize}; font-weight:800; margin-bottom:6px; line-height:1.1;">{value}</div>
        <div style="color:#cbd5e1; font-size:0.8rem;">{sub}</div>
    </div>
    """

    return f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:16px; padding:4px 0; font-family:Inter,sans-serif;">
        {card('⚽', 'Total Matches', total_matches, f'{total_goals} total goals', '#22c55e')}
        {card('📊', 'Avg Goals / Match', avg_goals, 'goals per game', '#a78bfa')}
        {card('🔥', 'Highest Scoring', highest_aggregate, fmt(highest_aggregate_match), '#fbbf24')}
        {card('💥', 'Biggest Margin', biggest_margin, fmt(biggest_margin_match), '#22c55e')}
        {card('🎯', 'Most Goals by One Side', most_goals_one_side, f'{most_goals_one_side_team} — {fmt(most_goals_one_side_match)}', '#f97316')}
        {card('🥅', 'First to 100 Goals', first_to_100 or '—', '100 goals milestone', '#22c55e', '1.6rem')}
        {card('🏆', 'First to 500 Goals', first_to_500 or '—', '500 goals milestone', '#f59e0b', '1.6rem')}
        {card('⚡', 'Longest Win Streak', longest_streak, longest_streak_team or '—', '#a78bfa')}
    </div>
    """


# ─────────────────────────────────────────────
# Head-to-Head
# ─────────────────────────────────────────────

def render_h2h_stats_html(team1, team2, matches_list):
    """Render head-to-head stats as a styled hero card with bar chart and stats table."""
    if not team1 or not team2 or team1 == team2:
        return '<div style="padding:24px; text-align:center; color:#64748b; font-family:Inter,sans-serif;">Select two different teams to compare.</div>'

    stats = {
        team1: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0},
        team2: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0},
    }

    h2h_matches = []
    for match in matches_list:
        h, a, gh, ga = match[1], match[2], match[3], match[4]
        if (h == team1 and a == team2) or (h == team2 and a == team1):
            h2h_matches.append(match)
            stats[h]["P"] += 1
            stats[h]["GF"] += gh
            stats[h]["GA"] += ga
            stats[a]["P"] += 1
            stats[a]["GF"] += ga
            stats[a]["GA"] += gh

            if gh > ga:
                stats[h]["W"] += 1
                stats[a]["L"] += 1
            elif gh < ga:
                stats[a]["W"] += 1
                stats[h]["L"] += 1
            else:
                stats[h]["D"] += 1
                stats[a]["D"] += 1

    total_played = stats[team1]["P"]
    if total_played == 0:
        return f'<div style="padding:24px; text-align:center; color:#64748b; font-family:Inter,sans-serif;">No matches between {team1} and {team2} yet.</div>'

    w1 = stats[team1]['W']
    w2 = stats[team2]['W']
    draws = stats[team1]['D']

    # Tri-color bar segments
    p1 = round(w1 / total_played * 100)
    pd_ = round(draws / total_played * 100)
    p2 = 100 - p1 - pd_

    # Form guide: last 5 H2H results (team1 perspective)
    last5 = sorted(h2h_matches, key=lambda x: x[5], reverse=True)[:5]
    form_dots = ""
    for m in reversed(last5):
        mh, ma, mgh, mga = m[1], m[2], m[3], m[4]
        if mgh == mga:
            dot_color, dot_label = "#eab308", "D"
        elif (mh == team1 and mgh > mga) or (ma == team1 and mga > mgh):
            dot_color, dot_label = "#3b82f6", "W"
        else:
            dot_color, dot_label = "#ef4444", "L"
        form_dots += f'<span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:{dot_color};margin:0 3px;" title="{dot_label}"></span>'

    # H2H records
    if h2h_matches:
        best_agg = max(h2h_matches, key=lambda x: x[3] + x[4])
        best_margin_m = max(h2h_matches, key=lambda x: abs(x[3] - x[4]))
        last_m = sorted(h2h_matches, key=lambda x: x[5])[-1]
        best_agg_str = f"{best_agg[1]} {best_agg[3]}–{best_agg[4]} {best_agg[2]}"
        margin_val = abs(best_margin_m[3] - best_margin_m[4])
        margin_str = f"{best_margin_m[1]} {best_margin_m[3]}–{best_margin_m[4]} {best_margin_m[2]}"
        last_mh, last_ma, last_mgh, last_mga = last_m[1], last_m[2], last_m[3], last_m[4]
        if last_mgh > last_mga:
            last_winner = last_mh
        elif last_mga > last_mgh:
            last_winner = last_ma
        else:
            last_winner = "Draw"
        last_str = f"{last_mh} {last_mgh}–{last_mga} {last_ma}"
    else:
        best_agg_str = margin_str = last_str = "—"
        margin_val = 0
        last_winner = "—"
        best_agg = None

    def mini_card(icon, label, val, sub):
        return f"""
    <div style="background:#0f172a; border-radius:10px; padding:14px 12px; border:1px solid #334155; text-align:center; flex:1; min-width:130px;">
        <div style="font-size:1.3rem; margin-bottom:4px;">{icon}</div>
        <div style="color:#64748b; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">{label}</div>
        <div style="color:#f1f5f9; font-size:1.3rem; font-weight:800; line-height:1;">{val}</div>
        <div style="color:#94a3b8; font-size:0.72rem; margin-top:4px;">{sub}</div>
    </div>"""

    def wp(t):
        p = stats[t]["P"]
        return round((stats[t]["W"] / p) * 100, 1) if p > 0 else 0.0

    wp1, wp2 = wp(team1), wp(team2)

    def stat_row(label, v1, v2, lower_better=False):
        if isinstance(v1, float) or isinstance(v2, float):
            v1s, v2s = f"{v1}%", f"{v2}%"
        else:
            v1s, v2s = str(v1), str(v2)
        if lower_better:
            better1 = v1 < v2
            better2 = v2 < v1
        else:
            better1 = v1 > v2
            better2 = v2 > v1
        c1 = "#3b82f6" if better1 else ("#94a3b8" if v1 == v2 else "#64748b")
        c2 = "#ef4444" if better2 else ("#94a3b8" if v1 == v2 else "#64748b")
        fw1 = "800" if better1 else "500"
        fw2 = "800" if better2 else "500"
        return f"""
        <tr style="border-bottom:1px solid #1e293b;">
            <td style="padding:10px 16px; color:{c1}; font-weight:{fw1}; text-align:right; font-size:1rem; width:35%;">{v1s}</td>
            <td style="padding:10px 8px; text-align:center; color:#475569; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em;">{label}</td>
            <td style="padding:10px 16px; color:{c2}; font-weight:{fw2}; font-size:1rem; width:35%;">{v2s}</td>
        </tr>"""

    if w1 > w2:
        leader_txt = f"<span style='color:#3b82f6;font-weight:800;'>{team1}</span> leads"
    elif w2 > w1:
        leader_txt = f"<span style='color:#ef4444;font-weight:800;'>{team2}</span> leads"
    else:
        leader_txt = "<span style='color:#eab308;font-weight:700;'>All Square</span>"

    return f"""
    <div style="font-family:Inter,ui-sans-serif,sans-serif; border-radius:14px; border:1px solid #334155; overflow:hidden; background:#1e293b;">

        <!-- Hero Header -->
        <div style="background:linear-gradient(135deg,#0f1f3d 0%,#0f172a 50%,#1f0f0f 100%); padding:24px 28px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <div style="text-align:left; flex:1;">
                    <div style="color:#3b82f6; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:4px;">Team 1</div>
                    <div style="color:#f1f5f9; font-size:1.5rem; font-weight:800;">{team1}</div>
                    <div style="color:#3b82f6; font-size:2.5rem; font-weight:900; line-height:1;">{w1}</div>
                    <div style="color:#64748b; font-size:0.7rem;">wins</div>
                </div>
                <div style="text-align:center; padding:0 20px;">
                    <div style="color:#475569; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px;">vs</div>
                    <div style="color:#eab308; font-size:1.6rem; font-weight:800;">{draws}</div>
                    <div style="color:#64748b; font-size:0.7rem;">draws</div>
                    <div style="margin-top:10px; font-size:0.72rem;">{leader_txt}</div>
                </div>
                <div style="text-align:right; flex:1;">
                    <div style="color:#ef4444; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:4px;">Team 2</div>
                    <div style="color:#f1f5f9; font-size:1.5rem; font-weight:800;">{team2}</div>
                    <div style="color:#ef4444; font-size:2.5rem; font-weight:900; line-height:1;">{w2}</div>
                    <div style="color:#64748b; font-size:0.7rem;">wins</div>
                </div>
            </div>

            <!-- Tri-color bar -->
            <div style="border-radius:8px; overflow:hidden; height:14px; display:flex; margin-bottom:6px;">
                <div style="width:{p1}%; background:#3b82f6; transition:width 0.3s;"></div>
                <div style="width:{pd_}%; background:#eab308;"></div>
                <div style="width:{p2}%; background:#ef4444;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.68rem; color:#64748b;">
                <span style="color:#3b82f6;">{p1}% ({w1}W)</span>
                <span style="color:#eab308;">{pd_}% ({draws}D) · {total_played} played</span>
                <span style="color:#ef4444;">({w2}W) {p2}%</span>
            </div>
        </div>

        <!-- Form Guide -->
        <div style="background:#0f172a; padding:12px 20px; display:flex; align-items:center; gap:10px; border-top:1px solid #1e293b;">
            <span style="color:#475569; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; white-space:nowrap;">Last {len(last5)}</span>
            <div style="display:flex; align-items:center;">{form_dots}</div>
            <span style="color:#475569; font-size:0.68rem; margin-left:4px;">← most recent</span>
        </div>

        <!-- H2H Records -->
        <div style="padding:16px 16px 8px; display:flex; gap:10px; flex-wrap:wrap;">
            {mini_card('🔥', 'Highest Scoring', best_agg[3]+best_agg[4] if h2h_matches else 0, best_agg_str)}
            {mini_card('💥', 'Biggest Margin', margin_val, margin_str)}
            {mini_card('📅', 'Last Match', last_winner, last_str)}
        </div>

        <!-- Stats Table -->
        <div style="padding:8px 16px 16px;">
            <table style="width:100%; border-collapse:collapse; background:#0f172a; border-radius:10px; overflow:hidden;">
                <thead>
                    <tr style="background:#0a1020;">
                        <th style="padding:8px 16px; text-align:right; color:#3b82f6; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; width:35%;">{team1}</th>
                        <th style="padding:8px; text-align:center; color:#475569; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.06em;"></th>
                        <th style="padding:8px 16px; text-align:left; color:#ef4444; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.08em; width:35%;">{team2}</th>
                    </tr>
                </thead>
                <tbody>
                    {stat_row('Won', w1, w2)}
                    {stat_row('Drawn', draws, draws)}
                    {stat_row('Lost', stats[team1]['L'], stats[team2]['L'], lower_better=True)}
                    {stat_row('Win %', wp1, wp2)}
                    {stat_row('Goals For', stats[team1]['GF'], stats[team2]['GF'])}
                    {stat_row('Goals Against', stats[team1]['GA'], stats[team2]['GA'], lower_better=True)}
                    {stat_row('GPM', round(stats[team1]['GF']/total_played,2), round(stats[team2]['GF']/total_played,2))}
                </tbody>
            </table>
        </div>
    </div>
    """


def get_h2h_match_history_html(team1, team2, matches_list):
    """Render the head-to-head match history with blue/yellow/red color scheme."""
    if not team1 or not team2 or team1 == team2:
        return ""
    h2h = sorted(
        [m for m in matches_list if
         (m[1] == team1 and m[2] == team2) or (m[1] == team2 and m[2] == team1)],
        key=lambda x: x[5], reverse=True
    )
    if not h2h:
        return '<div style="padding:24px; text-align:center; color:#64748b; font-family:Inter,sans-serif;">No matches yet.</div>'

    rows = ""
    for i, match in enumerate(h2h, 1):
        match_id, mh, ma, mgh, mga, dt = match[0], match[1], match[2], match[3], match[4], match[5]
        formatted_dt = format_datetime(dt)

        if mgh == mga:
            h_score_color = a_score_color = "#eab308"
            result_label = "DRAW"
            result_color = "#eab308"
        elif (mh == team1 and mgh > mga) or (ma == team1 and mga > mgh):
            h_score_color = "#3b82f6" if mh == team1 else "#ef4444"
            a_score_color = "#ef4444" if ma == team2 else "#3b82f6"
            result_label = f"{team1} WIN"
            result_color = "#3b82f6"
        else:
            h_score_color = "#ef4444" if mh == team1 else "#3b82f6"
            a_score_color = "#3b82f6" if ma == team2 else "#ef4444"
            result_label = f"{team2} WIN"
            result_color = "#ef4444"

        rows += f"""
        <tr style="border-bottom:1px solid #334155;">
            <td style="padding:8px 10px; color:#64748b; font-size:0.78rem; text-align:center;">{i}</td>
            <td style="padding:8px 10px; color:#64748b; font-size:0.73rem; white-space:nowrap;">{formatted_dt}</td>
            <td style="padding:8px 10px; font-weight:600; color:#f1f5f9; text-align:right; white-space:nowrap;">{mh}</td>
            <td style="padding:8px 12px; text-align:center; white-space:nowrap;">
                <span style="color:{h_score_color}; font-weight:800; font-size:1rem;">{mgh}</span>
                <span style="color:#475569; margin:0 4px;">–</span>
                <span style="color:{a_score_color}; font-weight:800; font-size:1rem;">{mga}</span>
            </td>
            <td style="padding:8px 10px; font-weight:600; color:#f1f5f9; white-space:nowrap;">{ma}</td>
            <td style="padding:8px 10px; text-align:center;">
                <span style="font-size:0.65rem; font-weight:700; color:{result_color}; background:{result_color}18;
                             padding:2px 8px; border-radius:4px; text-transform:uppercase; letter-spacing:0.05em;">{result_label}</span>
            </td>
        </tr>"""

    def th(label, align="center"):
        return f'<th style="padding:8px 10px; text-align:{align}; color:#22c55e; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.1em; white-space:nowrap;">{label}</th>'

    return f"""
    <div style="overflow-x:auto; border-radius:12px; border:1px solid #334155; font-family:Inter,ui-sans-serif,sans-serif;">
        <div style="overflow-y:auto; max-height:450px;">
            <table style="width:100%; border-collapse:collapse;">
                <thead style="position:sticky; top:0; z-index:1;">
                    <tr style="background:#0f172a; border-bottom:2px solid #22c55e;">
                        {th('#')}
                        {th('Date', 'left')}
                        {th('Home', 'right')}
                        {th('Score')}
                        {th('Away', 'left')}
                        {th('Result')}
                    </tr>
                </thead>
                <tbody style="background:#1e293b;">
                    {rows}
                </tbody>
            </table>
        </div>
    </div>"""


# ─────────────────────────────────────────────
# Utility renderers
# ─────────────────────────────────────────────

def make_status(msg):
    """Render a success or error status banner as HTML."""
    if not msg:
        return ""
    is_error = msg.lower().startswith("error")
    bg = "#fee2e2" if is_error else "#dcfce7"
    border = "#dc2626" if is_error else "#16a34a"
    color = "#991b1b" if is_error else "#166534"
    icon = "✗" if is_error else "✓"
    return f'<div style="padding:10px 14px; background:{bg}; border-left:4px solid {border}; border-radius:6px; color:{color}; font-weight:500; font-family:Inter,sans-serif;">{icon} {msg}</div>'


def update_score_preview(home, away, hg, ag):
    """Render a live score preview card based on form inputs."""
    h = home or "Home"
    a = away or "Away"
    hg = int(hg or 0)
    ag = int(ag or 0)
    h_color = "#22c55e" if hg > ag else ("#ef4444" if hg < ag else "#eab308")
    a_color = "#22c55e" if ag > hg else ("#ef4444" if ag < hg else "#eab308")
    result = "DRAW" if hg == ag else (f"{h} WIN" if hg > ag else f"{a} WIN")
    return f"""
    <div style="text-align:center; padding:16px; background:#0f172a; border-radius:12px; border:1px solid #334155; font-family:Inter,sans-serif;">
        <div style="font-size:0.68rem; color:#64748b; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:8px;">{result}</div>
        <div style="font-size:1.4rem; font-weight:800;">
            <span style="color:#f1f5f9;">{h}</span>
            <span style="color:{h_color}; margin:0 14px;">{hg}</span>
            <span style="color:#475569;">—</span>
            <span style="color:{a_color}; margin:0 14px;">{ag}</span>
            <span style="color:#f1f5f9;">{a}</span>
        </div>
    </div>
    """
