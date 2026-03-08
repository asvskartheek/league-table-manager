# How to Deliver Better UX for the Gradio League Table Manager

A thorough guide covering UX design principles, Gradio's customization capabilities, and concrete recommendations for improving the League Table Manager app.

---

## Table of Contents

1. [What's Wrong Right Now — Honest Audit](#1-whats-wrong-right-now--honest-audit)
2. [UX Design Principles That Apply Here](#2-ux-design-principles-that-apply-here)
3. [What Gradio Actually Lets You Control](#3-what-gradio-actually-lets-you-control)
4. [Concrete Recommendations by Area](#4-concrete-recommendations-by-area)
5. [Custom CSS — The Most Powerful Lever](#5-custom-css--the-most-powerful-lever)
6. [Theming — The Structured Lever](#6-theming--the-structured-lever)
7. [Layout Restructuring](#7-layout-restructuring)
8. [Data Display Improvements](#8-data-display-improvements)
9. [Interaction Feedback & State](#9-interaction-feedback--state)
10. [Typography & Visual Hierarchy](#10-typography--visual-hierarchy)
11. [What Gradio Cannot Do (and Workarounds)](#11-what-gradio-cannot-do-and-workarounds)
12. [Implementation Roadmap](#12-implementation-roadmap)
13. [Complete Reference Code Snippets](#13-complete-reference-code-snippets)

---

## 1. What's Wrong Right Now — Honest Audit

Looking at the screenshot, here is a plain-language breakdown of the problems:

### 1.1 Layout Problems

**The two-column split is unbalanced and cramped.**
The left column has a form (Home Team, Away Team, Goals, Add Match button, Status). The right column has the league table, match history, delete controls, AND update controls — all stacked vertically with no visual separation. The right column becomes a very long scroll while the left column is short. This creates visual asymmetry and makes the right column overwhelming.

**The "Update Match" section is buried.**
It lives at the very bottom of the right column — a destructive/critical action (editing existing records) is hidden below a long table of data. Users have to scroll past the entire match history to find it. This is bad information architecture.

**CRUD controls are mixed with data display.**
Delete and Update controls live inside the same column as the league table and match history. These are conceptually different things — viewing data vs. modifying data — but they're presented as if they're at the same level.

### 1.2 Data Density Problems

**The league table has 15 columns.**
WP, GPM, GAM, GDM, P, W, D, L, GF, GA, GD, Pts, #WW, #5GM — this is a lot of information for 8 rows. The columns are narrow and hard to scan. Users need to horizontally scroll to see all columns, which is a terrible experience.

**The match history table has no visual distinction between rows.**
Row numbers, timestamps, and scores are all presented identically. The most important thing — who won — is not visually highlighted.

**Column headers are cryptic abbreviations.**
GPM, GAM, GDM, #WW, #5GM — these mean nothing to a first-time viewer. There are no tooltips or explanations.

### 1.3 Interaction Problems

**The status message is invisible.**
After adding/deleting a match, the status appears in a small, unstyled textbox labeled "Status". Success and failure look identical — same font, same color, same size. There is no visual difference between "Match added successfully" and "Error: team names cannot be empty".

**Dropdown choices don't update after adding a new team.**
If you type a custom team name in the Home Team dropdown and add a match, that new team won't appear in the Away Team dropdown (or the Team vs Team dropdowns) until the page is refreshed. The UI state gets stale.

**The Number inputs for goals require clicking arrows.**
The default `gr.Number` renders with increment/decrement arrows. For entering goals (0-15 typically), this is fine — but the visual design of these inputs is inconsistent with the dropdowns above them (different heights, different borders).

### 1.4 Visual Design Problems

**No visual identity for a sports/league context.**
The UI looks like a generic data entry form. There is nothing that evokes a league, competition, or scoreboard. A dark sports-dashboard aesthetic (think football scoreboard apps) would be far more appropriate and engaging.

**The orange button is jarring.**
Gradio's default `variant="primary"` orange works for ML demos but looks out of place here. It also clashes with the green tabs.

**No color coding for standings.**
In every real league table — Premier League, La Liga, Serie A — the top positions are highlighted green (Champions League spots) and the bottom positions red (relegation). This is a universally understood visual language that this app ignores completely.

**No responsive design.**
On mobile or a narrow window, the two-column layout collapses and everything becomes a single stacked column with no adaptation — the tables overflow horizontally.

---

## 2. UX Design Principles That Apply Here

These are established, widely-cited UX principles and how each applies to this app:

### 2.1 Fitts's Law — Make Important Actions Big and Close

Fitts's Law states that the time to click a target is a function of distance and target size. The "Add Match" button is the most frequently used action in this app and it's appropriately prominent. But the "Delete Row" and "Update Match" actions are small and buried. Solution: make actions proportional to their frequency, and destructive actions (delete) require confirmation (see 2.5).

### 2.2 Hick's Law — Reduce Decision Complexity

Hick's Law: the more choices a user has, the longer decisions take. The League Manager tab presents the user with 7 form fields, 3 buttons, and 2 tables all at once. The cognitive load is high. Solution: separate the "Add Match" primary task from the "Edit/Delete" secondary tasks, either by tabbing them or collapsing the edit section.

### 2.3 Miller's Law — 7 ± 2 Chunks

Humans can hold about 7 items in working memory. The league table has 15 columns. This isn't wrong per se — a league table genuinely has many stats — but the way information is grouped matters. Solution: visually group related columns (e.g., "Attack" for GF/GPM, "Defense" for GA/GAM, "Results" for W/D/L/Pts).

### 2.4 The Principle of Least Surprise

Users should not be surprised by the result of an action. Currently, after you add a match, the dropdowns still show the same teams — the table updates but the form doesn't reset. Should the goal inputs reset to 0? Probably yes. Should a success message appear prominently? Yes. Solution: after a successful add, reset goal inputs to 0 and show a clear green confirmation.

### 2.5 Prevent Errors (Error Prevention > Error Recovery)

Nielsen's 10 Usability Heuristics include "Error Prevention" as higher priority than good error messages. Currently, there is no confirmation dialog before deleting a match. You enter a row number and click "Delete Row" and the match is gone. Solution: at minimum, show a preview of what will be deleted ("Row 3: Kartheek 4-2 Shiva") before the delete action executes.

### 2.6 Recognition vs. Recall

Users should recognize options rather than having to recall them. The "Row # to Delete" input requires the user to look at the match history table, find the row number, mentally note it, then type it into the input. This is a recall task. Solution: make rows in the match history table selectable (Gradio's `gr.Dataframe` supports `row_count` and selection) and automatically populate the delete/edit inputs from the selected row.

### 2.7 Feedback — Show System Status

Nielsen's #1 heuristic: "Visibility of system status". The app currently has one status textbox for all messages — success, failure, loading. There is no loading state while a match is being written to Supabase. Solution: use `gr.Progress` or update a status component with clear visual states (green text for success, red for error).

### 2.8 Visual Hierarchy with the F-Pattern

Eye-tracking studies show users read web pages in an F-pattern: strong attention to the top horizontal band, then a secondary sweep lower, then vertical scanning of the left side. The current layout puts the most frequently viewed data (league table) in the right column — which gets secondary attention — while the form (less important for reading) is in the left column, which gets primary attention. This is backwards for read-heavy usage.

### 2.9 Affordance — Make Interactive Things Look Interactive

The delete and update row number inputs look the same as the goal inputs. There's no visual affordance that these are the "dangerous" inputs (they affect existing records). Solution: style the delete section with a red/warning border, and the update section with a blue/caution border.

### 2.10 Proximity — Group Related Things Together

The Gestalt principle of proximity: elements close to each other appear related. Currently the "Update Match" fields (row number, new home team, new away team, new goals) are just placed vertically without clear visual grouping. They blend with the league table above them. Solution: use a visually distinct `gr.Group` or `gr.Accordion` container with a clear header.

---

## 3. What Gradio Actually Lets You Control

Gradio (as of v4+) exposes several layers of customization, in increasing order of power and complexity:

### 3.1 Built-in Themes

Gradio ships with: `gr.themes.Base()`, `gr.themes.Default()`, `gr.themes.Soft()`, `gr.themes.Monochrome()`, `gr.themes.Glass()`.

You apply them in `gr.Blocks(theme=...)`. Each theme changes the entire color palette, typography, border radius, and spacing globally.

```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    ...
```

**What you can control via themes:**
- Primary hue (the accent color — buttons, highlights, active tabs)
- Secondary hue (used for some accents)
- Neutral hue (backgrounds, borders, text)
- Font family (supports Google Fonts via `gr.themes.GoogleFont()`)
- Border radius (sharp corners vs. rounded)
- Spacing (compact vs. spacious)
- Text size

### 3.2 Custom Theme Classes (Subclassing `gr.themes.Base`)

You can subclass `gr.themes.Base` and call `super().set(...)` to override specific CSS variables. Gradio exposes hundreds of CSS variables for individual component parts (button hover state, block shadow, input focus ring, etc.). This gives fine-grained control without writing raw CSS.

```python
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class SportsTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.green,
            neutral_hue=colors.slate,
            font=fonts.GoogleFont("Inter"),
        )
        super().set(
            body_background_fill="#0f172a",       # dark navy
            block_background_fill="#1e293b",       # slightly lighter
            button_primary_background_fill="#16a34a",
            button_primary_text_color="white",
            block_border_width="1px",
            block_border_color="#334155",
        )
```

### 3.3 Raw CSS via `css=` Parameter in `gr.Blocks`

You can pass a raw CSS string to `gr.Blocks(css=...)`. This lets you target any element with standard CSS selectors. You can also target Gradio components by assigning them `elem_id` or `elem_classes` attributes.

```python
with gr.Blocks(css="""
    #league-table .cell-wrap { font-weight: bold; }
    .status-success { color: #16a34a !important; }
""") as demo:
    table = gr.Dataframe(elem_id="league-table")
```

**Important:** Gradio renders all tables as HTML tables internally, so you can target them with CSS selectors. However, Gradio uses Shadow DOM in some components, which limits CSS penetration. Use `!important` where needed.

### 3.4 CSS from External Files

Instead of an inline string, you can load CSS from a file:

```python
demo.launch(css_paths=["styles.css"])
```

This is better for maintainability when CSS grows large.

### 3.5 `gr.HTML` — Inject Arbitrary HTML

`gr.HTML(value="<div>...</div>")` lets you inject any HTML into the layout. This is the escape hatch for anything Gradio's component system can't do. You can use it for:
- Custom stat cards (styled divs instead of dataframes for key metrics)
- Progress bars
- Color-coded text/badges
- Custom score displays
- Header banners with logos

```python
def render_standings_card(team, pts, wp):
    color = "#16a34a" if wp > 60 else "#dc2626" if wp < 30 else "#d97706"
    return f"""
    <div style="background:{color}20; border-left:4px solid {color}; padding:12px; border-radius:8px; margin:4px 0;">
        <strong>{team}</strong> — {pts} pts ({wp}% WR)
    </div>
    """
```

### 3.6 `gr.Dataframe` Styling

`gr.Dataframe` supports a `datatype` parameter that changes how cells are rendered. You can use `"markdown"` as a datatype for columns, which means cells can contain HTML/Markdown, enabling colored badges, bold text, etc.

```python
gr.Dataframe(
    datatype=["str", "markdown", "number", ...],
    ...
)
```

Then in your DataFrame, format values as Markdown strings:
```python
df["WP"] = df["WP"].apply(lambda x: f"**{x}%**" if x > 60 else f"{x}%")
```

### 3.7 `gr.Accordion` — Collapsible Sections

`gr.Accordion(label="Update Match", open=False)` wraps content in a collapsible panel. This is perfect for hiding secondary actions (delete, update) until the user explicitly needs them.

```python
with gr.Accordion("Edit / Delete Match", open=False):
    # delete and update controls here
```

### 3.8 `gr.Group` and `gr.Column` with `variant`

`gr.Group()` draws a visual boundary (rounded box) around its contents. Useful for making the add-match form feel like a distinct card.

```python
with gr.Group():
    home_team = gr.Dropdown(...)
    away_team = gr.Dropdown(...)
```

### 3.9 Component-Level Styling

Every Gradio component accepts:
- `elem_id` — unique CSS id
- `elem_classes` — list of CSS classes
- `scale` — relative width in a row
- `min_width` — minimum pixel width
- `visible` — show/hide

### 3.10 `gr.Progress` and Loading States

Gradio supports a `gr.Progress` context manager for long-running operations, and also a `show_progress` flag on event handlers. This is important for Supabase operations that might take 500ms-2s.

```python
submit_btn.click(
    fn=add_match,
    inputs=[...],
    outputs=[...],
    show_progress="minimal"   # or "full"
)
```

---

## 4. Concrete Recommendations by Area

### 4.1 Tab Structure — Split Into Better Sections

**Current:** 3 tabs: League Manager, Team vs Team Stats, League Stats

**Recommended:** 4 tabs with better naming:
- **Standings** — The league table only, full-width, prominent
- **Match Log** — Match history + Add Match form side by side
- **Head to Head** — Team vs Team (renamed for clarity)
- **Records** — League Stats (renamed for clarity)

Rationale: The league table is the most-viewed thing. Give it its own tab so it can be full-width and readable. The "League Manager" tab is trying to do too many things (view table + view history + add + delete + update).

### 4.2 Rename Cryptic Columns

These column names need plain-English tooltips or at least full-form labels:

| Current | Suggested Label | Meaning |
|---------|----------------|---------|
| WP | Win % | Win percentage |
| GPM | Goals/Game | Goals scored per match |
| GAM | Conceded/Game | Goals conceded per match |
| GDM | GD/Game | Goal difference per match |
| P | Played | Matches played |
| GF | Goals For | Total goals scored |
| GA | Goals Against | Total goals conceded |
| GD | Goal Diff | Goal difference |
| Pts | Points | League points |
| #WW | Whitewashes | Clean-sheet wins |
| #5GM | 5-Goal Games | Matches where scored 5+ |

Since Gradio DataFrames don't support column tooltips natively, you can add a `gr.Markdown` key/legend below the table.

### 4.3 Color-Code the League Table

This is the single biggest readability improvement. Use `gr.HTML` to render a custom HTML table instead of `gr.Dataframe` for the league table. This gives full CSS control:

- Top 3 positions: left border in gold/silver/bronze
- Win % > 60%: green row tint
- Win % < 30%: red row tint
- Bold points column
- Rank number in a styled circle

### 4.4 Redesign Status Feedback

Replace the plain `gr.Textbox` status with `gr.HTML` that renders styled alerts:

```python
def styled_status(msg, success=True):
    color = "#16a34a" if success else "#dc2626"
    bg = "#f0fdf4" if success else "#fef2f2"
    icon = "✓" if success else "✗"
    return f"""
    <div style="padding:12px 16px; background:{bg}; border-radius:8px;
                border-left:4px solid {color}; color:{color}; font-weight:500;">
        {icon} {msg}
    </div>
    """
```

### 4.5 Add a Score Display for Add Match

Instead of raw number inputs, show a live score preview as the user fills in the form:

```python
score_preview = gr.HTML(value="<div class='score'>? - ?</div>")

def update_preview(home, away, hg, ag):
    h = home or "Home"
    a = away or "Away"
    return f"""<div style="text-align:center; font-size:1.5rem; font-weight:700;
                           padding:12px; background:#1e293b; border-radius:8px; color:white;">
        {h} <span style="color:#16a34a">{int(hg)}</span>
        —
        <span style="color:#dc2626">{int(ag)}</span> {a}
    </div>"""

home_team.change(fn=update_preview, inputs=[home_team, away_team, home_goals, away_goals], outputs=[score_preview])
away_team.change(fn=update_preview, inputs=[home_team, away_team, home_goals, away_goals], outputs=[score_preview])
home_goals.change(fn=update_preview, inputs=[home_team, away_team, home_goals, away_goals], outputs=[score_preview])
away_goals.change(fn=update_preview, inputs=[home_team, away_team, home_goals, away_goals], outputs=[score_preview])
```

### 4.6 Collapse Edit/Delete Controls

Wrap delete and update in `gr.Accordion` components, closed by default. This reduces cognitive overload on first load.

```python
with gr.Accordion("Delete a Match", open=False):
    ...

with gr.Accordion("Edit a Match", open=False):
    ...
```

### 4.7 Update Dropdowns After Adding a Match

Currently, if a new team is entered as custom value, the dropdowns don't update. After every add/delete/update, refresh the dropdown choices:

```python
def add_match_and_refresh(home, away, hg, ag):
    result = add_match(home, away, hg, ag)  # returns table, history, status
    teams = get_teams_from_matches()
    team_update = gr.Dropdown(choices=teams)
    return (*result, team_update, team_update, team_update, team_update)
```

---

## 5. Custom CSS — The Most Powerful Lever

Here is a complete CSS block you can pass to `gr.Blocks(css=...)` to transform the look without changing layout logic:

```css
/* ===== Global Dark Sports Theme ===== */

/* Body background */
body, .gradio-container {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}

/* Tab bar */
.tab-nav button {
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #94a3b8 !important;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.tab-nav button.selected {
    color: #22c55e !important;
    border-bottom: 2px solid #22c55e !important;
    background: transparent !important;
}

/* Blocks / Cards */
.block {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

/* Labels */
label span {
    color: #94a3b8 !important;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Input fields */
input[type="text"],
input[type="number"],
.gr-textbox textarea {
    background-color: #0f172a !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

input:focus, textarea:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1) !important;
}

/* Dropdown */
.gr-dropdown {
    background-color: #0f172a !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
}

/* Primary button - green instead of orange */
button.primary {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3) !important;
    transition: all 0.2s !important;
}

button.primary:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    box-shadow: 0 6px 16px rgba(34, 197, 94, 0.4) !important;
    transform: translateY(-1px);
}

/* Danger/stop button */
button.stop {
    background: #7f1d1d !important;
    color: #fca5a5 !important;
    border: 1px solid #dc2626 !important;
}

/* Dataframe table */
.gr-dataframe table {
    border-collapse: collapse;
    width: 100%;
}

.gr-dataframe th {
    background-color: #0f172a !important;
    color: #22c55e !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    padding: 10px 8px !important;
    border-bottom: 2px solid #22c55e !important;
}

.gr-dataframe td {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    padding: 8px !important;
    border-bottom: 1px solid #334155 !important;
    font-size: 0.85rem;
}

.gr-dataframe tr:hover td {
    background-color: #263548 !important;
}

/* Accordion */
.gr-accordion {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* Title/Heading */
h1 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: white !important;
}
```

**How to apply it:**

```python
with open("styles.css") as f:
    css = f.read()

with gr.Blocks(title="League Table Manager", css=css) as demo:
    ...
```

Or inline:

```python
CSS = """... (paste above) ..."""
with gr.Blocks(css=CSS) as demo:
    ...
```

---

## 6. Theming — The Structured Lever

For a clean football/sports aesthetic, here is a complete custom theme class to replace the default:

```python
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class LeagueTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.green,
            secondary_hue=colors.emerald,
            neutral_hue=colors.slate,
            spacing_size=sizes.spacing_md,
            radius_size=sizes.radius_lg,
            text_size=sizes.text_md,
            font=(
                fonts.GoogleFont("Inter"),
                "ui-sans-serif",
                "system-ui",
                "sans-serif",
            ),
            font_mono=(
                fonts.GoogleFont("JetBrains Mono"),
                "ui-monospace",
                "monospace",
            ),
        )
        super().set(
            # Body
            body_background_fill="#0f172a",
            body_background_fill_dark="#0f172a",
            # Blocks/Cards
            block_background_fill="#1e293b",
            block_background_fill_dark="#1e293b",
            block_border_color="#334155",
            block_border_color_dark="#334155",
            block_border_width="1px",
            block_radius="12px",
            block_shadow="0 4px 24px rgba(0,0,0,0.4)",
            # Text
            body_text_color="#e2e8f0",
            body_text_color_dark="#e2e8f0",
            block_label_text_color="#94a3b8",
            block_label_text_weight="600",
            # Inputs
            input_background_fill="#0f172a",
            input_background_fill_dark="#0f172a",
            input_border_color="#334155",
            input_border_color_dark="#334155",
            input_border_color_focus="*primary_500",
            # Buttons
            button_primary_background_fill="*primary_600",
            button_primary_background_fill_hover="*primary_500",
            button_primary_text_color="white",
            button_primary_border_color="transparent",
            button_secondary_background_fill="#334155",
            button_secondary_background_fill_hover="#475569",
            button_secondary_text_color="#e2e8f0",
            # Tabs
            border_color_primary="*primary_600",
        )

theme = LeagueTheme()

with gr.Blocks(title="League Table Manager", theme=theme) as demo:
    ...
```

---

## 7. Layout Restructuring

### 7.1 The Core Problem: Information Architecture

Current information architecture:

```
Tab: League Manager
  Row:
    Column (left, scale=1):
      - Home Team dropdown
      - Away Team dropdown
      - Home Goals + Away Goals
      - Add Match button
      - Status textbox
    Column (right, scale=2):
      - League Table (dataframe)
      - Match History (dataframe)
      - Delete controls
      - --- separator ---
      - Update Match section
```

Problems: Add/Edit/Delete + View all in one tab, too much content in right column.

Proposed information architecture:

```
Tab: Standings
  - Full-width League Table (colored HTML)
  - Summary stats row: Total Matches | Top Scorer | Most Wins

Tab: Matches
  Row:
    Column (left, scale=1):
      - Score Preview (gr.HTML live-updating)
      - Home Team dropdown
      - Away Team dropdown
      - Home Goals + Away Goals
      - Add Match button
      - Status (gr.HTML colored alert)
    Column (right, scale=2):
      - Match History (dataframe, full-width)
      - Accordion: "Edit a Match" (closed by default)
        - Row # input
        - Team/Goals inputs
        - Update button
      - Accordion: "Delete a Match" (closed by default)
        - Row # input + preview text
        - Delete button (with confirmation via JS or 2-step)

Tab: Head to Head
  - Team 1 + Team 2 dropdowns
  - H2H stats cards (side by side, styled HTML)
  - Match history between teams

Tab: League Records
  - League-level stats (best styled as gr.HTML cards, not a dataframe)
```

### 7.2 Making Full-Width Tables

Gradio's default layout adds padding to columns. To make a table truly full-width, wrap it in a Row with no columns:

```python
with gr.Row():
    league_table = gr.Dataframe(
        label="League Table",
        value=calculate_table(matches),
        interactive=False,
    )
```

Or, for maximum control, render the entire table as HTML:

```python
league_table_html = gr.HTML(value=render_league_table_html(matches))
```

### 7.3 Sticky Form + Scrollable Table

Gradio does not natively support CSS `position: sticky` layouts — the two-column layout will scroll together. However, you can keep the form compact and the table auto-height:

```python
with gr.Column(scale=1, min_width=280):
    # Keep form as compact as possible — fewer elements, less height
    ...
with gr.Column(scale=3):
    # Table takes remaining space
    gr.Dataframe(height=500)  # fixed height with scrolling inside
```

The `height` parameter on `gr.Dataframe` creates an internally scrolling table with a fixed outer height.

---

## 8. Data Display Improvements

### 8.1 Replace League Table Dataframe with HTML

The biggest win. Instead of `gr.Dataframe`, render the league table as a styled HTML table using `gr.HTML`. This lets you:
- Color entire rows based on rank/win-rate
- Add rank medals (gold/silver/bronze icons)
- Bold the points column
- Show win% as a visual bar

```python
def render_league_table_html(df):
    rows_html = ""
    for i, row in df.iterrows():
        rank = i + 1
        wp = row["WP"]

        # Row color based on win rate
        if wp >= 60:
            row_style = "background: rgba(34,197,94,0.08); border-left: 3px solid #22c55e;"
        elif wp >= 40:
            row_style = "background: rgba(234,179,8,0.08); border-left: 3px solid #eab308;"
        else:
            row_style = "background: rgba(239,68,68,0.08); border-left: 3px solid #ef4444;"

        # Rank medal
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")

        # Win% bar
        bar = f"""
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="flex:1; background:#334155; border-radius:4px; height:6px;">
                <div style="width:{wp}%; background:#22c55e; border-radius:4px; height:6px;"></div>
            </div>
            <span style="font-size:0.75rem; color:#94a3b8; min-width:42px;">{wp}%</span>
        </div>
        """

        rows_html += f"""
        <tr style="{row_style}">
            <td style="padding:10px 8px; font-weight:700;">{medal}</td>
            <td style="padding:10px 8px; font-weight:600; color:#f1f5f9;">{row['Team']}</td>
            <td style="padding:10px 8px;">{bar}</td>
            <td style="padding:10px 8px; text-align:center;">{row['P']}</td>
            <td style="padding:10px 8px; text-align:center; color:#22c55e; font-weight:600;">{row['W']}</td>
            <td style="padding:10px 8px; text-align:center; color:#94a3b8;">{row['D']}</td>
            <td style="padding:10px 8px; text-align:center; color:#ef4444; font-weight:600;">{row['L']}</td>
            <td style="padding:10px 8px; text-align:center;">{row['GF']}</td>
            <td style="padding:10px 8px; text-align:center;">{row['GA']}</td>
            <td style="padding:10px 8px; text-align:center;">{int(row['GD']):+d}</td>
            <td style="padding:10px 8px; text-align:center; font-weight:800; font-size:1.1rem; color:#fbbf24;">{row['Pts']}</td>
            <td style="padding:10px 8px; text-align:center; font-size:0.8rem;">{row['GPM']}</td>
            <td style="padding:10px 8px; text-align:center; font-size:0.8rem;">{row['#WW']}</td>
            <td style="padding:10px 8px; text-align:center; font-size:0.8rem;">{row['#5GM']}</td>
        </tr>
        """

    table_html = f"""
    <div style="overflow-x:auto; border-radius:12px; border:1px solid #334155;">
        <table style="width:100%; border-collapse:collapse; font-family:Inter,sans-serif;">
            <thead>
                <tr style="background:#0f172a; border-bottom:2px solid #22c55e;">
                    <th style="padding:10px 8px; text-align:left; color:#22c55e; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em;">#</th>
                    <th style="padding:10px 8px; text-align:left; color:#22c55e; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em;">Team</th>
                    <th style="padding:10px 8px; text-align:left; color:#22c55e; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em;">Win Rate</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">P</th>
                    <th style="padding:10px 8px; text-align:center; color:#22c55e; font-size:0.7rem; text-transform:uppercase;">W</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">D</th>
                    <th style="padding:10px 8px; text-align:center; color:#ef4444; font-size:0.7rem; text-transform:uppercase;">L</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">GF</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">GA</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">GD</th>
                    <th style="padding:10px 8px; text-align:center; color:#fbbf24; font-size:0.7rem; text-transform:uppercase;">Pts</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">G/GM</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">WW</th>
                    <th style="padding:10px 8px; text-align:center; color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">5G</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    return table_html
```

### 8.2 Match History with Score Highlighting

Color the score in match history to show the winner at a glance:

```python
def render_match_history_html(matches_list):
    rows = ""
    for i, match in enumerate(sorted_matches, 1):
        _, h, a, gh, ga, dt = match

        # Determine winner
        if gh > ga:
            h_color, a_color = "#22c55e", "#ef4444"
        elif ga > gh:
            h_color, a_color = "#ef4444", "#22c55e"
        else:
            h_color, a_color = "#eab308", "#eab308"

        rows += f"""
        <tr style="border-bottom:1px solid #334155;">
            <td style="padding:8px; color:#64748b; font-size:0.8rem;">{i}</td>
            <td style="padding:8px; color:#94a3b8; font-size:0.75rem;">{formatted_dt}</td>
            <td style="padding:8px; font-weight:600; color:#f1f5f9; text-align:right;">{h}</td>
            <td style="padding:8px; text-align:center; font-weight:800; font-size:1rem;">
                <span style="color:{h_color}">{gh}</span>
                <span style="color:#475569; margin:0 4px;">-</span>
                <span style="color:{a_color}">{ga}</span>
            </td>
            <td style="padding:8px; font-weight:600; color:#f1f5f9;">{a}</td>
        </tr>
        """
    return f'<div style="overflow-y:auto; max-height:400px; border-radius:12px; border:1px solid #334155;"><table style="width:100%; border-collapse:collapse;">{rows}</table></div>'
```

### 8.3 Stats Cards for Key Metrics

Instead of a dataframe for League Records, use stat cards:

```python
def render_stat_cards(matches_list):
    # ... compute stats ...
    return f"""
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:16px;">
        <div style="background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; text-align:center;">
            <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">
                Highest Scoring Match
            </div>
            <div style="color:#fbbf24; font-size:2rem; font-weight:800; margin-bottom:4px;">{highest_agg}</div>
            <div style="color:#e2e8f0; font-size:0.85rem;">{best_match_str}</div>
        </div>
        <div style="background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; text-align:center;">
            <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">
                Biggest Win Margin
            </div>
            <div style="color:#22c55e; font-size:2rem; font-weight:800; margin-bottom:4px;">{biggest_margin}</div>
            <div style="color:#e2e8f0; font-size:0.85rem;">{margin_match_str}</div>
        </div>
        <div style="background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; text-align:center;">
            <div style="color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">
                Most Goals in a Game
            </div>
            <div style="color:#a78bfa; font-size:2rem; font-weight:800; margin-bottom:4px;">{most_goals}</div>
            <div style="color:#e2e8f0; font-size:0.85rem;">{most_goals_str}</div>
        </div>
    </div>
    """
```

---

## 9. Interaction Feedback & State

### 9.1 Two-Step Delete Confirmation

Pure Python approach — no JavaScript needed:

```python
pending_delete = gr.State(None)   # stores match info for pending delete

def stage_delete(row_number):
    """First click — show what will be deleted."""
    sorted_matches = sorted(matches, key=lambda x: x[5], reverse=True)
    row_idx = int(row_number) - 1
    if row_idx < 0 or row_idx >= len(sorted_matches):
        return gr.HTML("<div style='color:red'>Invalid row number</div>"), None, gr.update(visible=False)
    match = sorted_matches[row_idx]
    h, a, gh, ga = match[1], match[2], match[3], match[4]
    preview = f"""
    <div style="padding:12px; background:#7f1d1d20; border:1px solid #dc2626; border-radius:8px; color:#fca5a5;">
        About to delete: <strong>{h} {gh} - {ga} {a}</strong><br>
        <small>Click 'Confirm Delete' to proceed, or change the row number to cancel.</small>
    </div>
    """
    return gr.HTML(preview), match[0], gr.update(visible=True)

confirm_delete_btn = gr.Button("Confirm Delete", variant="stop", visible=False)
delete_preview = gr.HTML()
pending_match_id = gr.State(None)

delete_row_input.change(fn=stage_delete, inputs=[delete_row_input],
                        outputs=[delete_preview, pending_match_id, confirm_delete_btn])
confirm_delete_btn.click(fn=execute_delete, inputs=[pending_match_id],
                         outputs=[league_table, matches_table, status_msg])
```

### 9.2 Auto-Reset Goals After Adding Match

```python
def add_match_and_reset(home, away, hg, ag):
    table, history, status = add_match(home, away, hg, ag)
    teams = get_teams_from_matches()
    return (
        table, history, status,
        gr.Number(value=0),   # reset home goals
        gr.Number(value=0),   # reset away goals
        gr.Dropdown(choices=teams),  # refresh home dropdown
        gr.Dropdown(choices=teams),  # refresh away dropdown
    )
```

### 9.3 Colored Status Alerts

```python
def make_status_html(msg):
    if msg.startswith("Error"):
        return f'<div style="padding:10px 14px; background:#fee2e2; border-left:4px solid #dc2626; border-radius:6px; color:#991b1b; font-weight:500;">✗ {msg}</div>'
    return f'<div style="padding:10px 14px; background:#dcfce7; border-left:4px solid #16a34a; border-radius:6px; color:#166534; font-weight:500;">✓ {msg}</div>'

status_html = gr.HTML(value="")
```

---

## 10. Typography & Visual Hierarchy

### 10.1 Font Choice

Use **Inter** — it is the industry standard for dashboards and data-heavy UIs. It has excellent tabular number support (all numbers have equal width), which is critical for aligning columns in a league table.

```python
from gradio.themes.utils import fonts
font=fonts.GoogleFont("Inter")
```

For mono/number-heavy columns, **JetBrains Mono** or **IBM Plex Mono** gives numbers a monospaced alignment.

### 10.2 Heading Hierarchy

The current app uses `gr.Markdown("# League Table Manager")` and `gr.Markdown("### Head-to-Head Statistics")` etc., but with inconsistent levels. Establish a clear hierarchy:

```
H1 (one per page): App name in the page header only
H2 (one per tab): Tab-level section name
H3 (within a tab): Subsection names
```

### 10.3 Numeric Display

In the league table, numbers should be:
- Right-aligned within columns
- Tabular lining figures (all same width) — Inter handles this
- Consistent decimal places (GPM: always 2 decimal places)
- Signed for goal difference (+161, -87)

```python
df["GD"] = df["GD"].apply(lambda x: f"+{x}" if x > 0 else str(x))
```

---

## 11. What Gradio Cannot Do (and Workarounds)

Understanding Gradio's limitations is as important as knowing its capabilities.

### 11.1 Cannot: Truly Sticky/Fixed Sidebar

Gradio does not support `position:fixed` or `position:sticky` layouts natively. The CSS property doesn't apply because Gradio wraps everything in a scrollable container. **Workaround:** Keep the form minimal and compact (as described in 7.3). Use `height` on tables to make the table scroll internally, keeping the form visible above.

### 11.2 Cannot: Real-Time Table Refresh Without User Action

Gradio does not push data to the client automatically. If two people are using the app simultaneously, user A won't see user B's added matches until they interact or refresh. **Workaround:** Add a `gr.Button("Refresh", variant="secondary")` that calls `refresh_data()`. Alternatively, use `every=N` on `demo.load()` for polling, though this adds server load.

```python
# Poll every 30 seconds automatically
demo.load(fn=refresh_data, outputs=[league_table, matches_table], every=30)
```

### 11.3 Cannot: Sortable Table Columns (Click Header to Sort)

`gr.Dataframe` does not support clicking column headers to re-sort. **Workaround:** Add `gr.Radio` or `gr.Dropdown` for "Sort by" selection, then re-compute the sorted DataFrame in Python.

```python
sort_by = gr.Dropdown(choices=["Win %", "Points", "Goals For", "Goals Against"], value="Win %", label="Sort Table By")
sort_by.change(fn=lambda col: calculate_table_sorted(matches, col), inputs=[sort_by], outputs=[league_table])
```

### 11.4 Cannot: Inline Row Editing in Dataframe

Clicking a row in the Dataframe to populate edit fields is not directly supported. `gr.Dataframe` has `select` event (fires when a cell is selected), but the API is limited. **Workaround:** Use `gr.Dataframe.select()` event to capture the row index and auto-populate edit fields.

```python
def on_row_select(evt: gr.SelectData):
    row_number = evt.index[0] + 1  # 1-indexed
    return row_number

matches_table.select(fn=on_row_select, outputs=[delete_row_input])
```

### 11.5 Cannot: Tooltips on Dataframe Column Headers

Gradio's Dataframe component does not support `title` attributes or hover tooltips on column headers. **Workaround:** Put a legend below the table as a collapsible `gr.Accordion`:

```python
with gr.Accordion("Column Guide", open=False):
    gr.Markdown("""
    | Col | Meaning |
    |-----|---------|
    | WP | Win Percentage |
    | GPM | Goals Per Match |
    | GAM | Goals Against Per Match |
    | GDM | Goal Difference Per Match |
    | #WW | Whitewash wins (opponent scored 0) |
    | #5GM | Matches where you scored 5 or more |
    """)
```

### 11.6 Cannot: Native Animations or Transitions

Gradio does not support animated transitions between states (e.g., counter incrementing from old to new value). **Workaround:** Accept static updates. If animations are critical, render the component as `gr.HTML` and include CSS animations:

```css
@keyframes pulse {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
}
.updating { animation: pulse 1s infinite; }
```

### 11.7 Cannot: Confirmation Dialogs (Native Browser `confirm()`)

`window.confirm()` is not accessible from Python. **Workaround:** Use the two-step pattern described in section 9.1 — first click stages the action with a preview, second click confirms it.

### 11.8 Cannot: Context Menus or Right-Click Actions

No way to intercept right-click on Gradio components. **Workaround:** Provide explicit action buttons — not a limitation worth fighting.

---

## 12. Implementation Roadmap

A prioritized list of changes, from highest impact / lowest effort to lowest impact / highest effort:

### Phase 1 — Quick Wins (1-2 hours)

1. Apply `gr.themes.Soft()` or `gr.themes.Monochrome()` as a starter theme
2. Add `gr.Accordion` around delete and update sections (closed by default)
3. Replace status `gr.Textbox` with `gr.HTML` + colored alert function
4. Add `height=400` to both DataFrames to prevent page-length explosions
5. Add column guide accordion below league table

### Phase 2 — Layout Restructuring (2-4 hours)

6. Separate league table into its own tab ("Standings")
7. Rename tabs: League Manager → "Matches", Team vs Team Stats → "Head to Head", League Stats → "Records"
8. Move match add form to left column of Matches tab, history to right
9. Add score preview `gr.HTML` above the form
10. Refresh dropdown choices after every mutation (add/delete/update)

### Phase 3 — Custom Theme and CSS (2-3 hours)

11. Implement `LeagueTheme` class (section 6)
12. Apply custom CSS for dataframe headers, row hover, and tab styling
13. Apply Inter font
14. Style buttons: green primary, red delete, neutral secondary

### Phase 4 — HTML-Rendered Tables (3-5 hours)

15. Replace league table Dataframe with `render_league_table_html()` function
16. Add win-rate progress bars to each team row
17. Add medal icons for top 3
18. Color the match history score cells by winner
19. Replace League Stats dataframe with 3-card HTML grid

### Phase 5 — Advanced Interactions (3-5 hours)

20. Add row selection → auto-populate edit fields
21. Implement two-step delete confirmation
22. Add auto-reset of goals to 0 after successful add
23. Add sort-by dropdown for league table
24. Add `every=30` auto-refresh on demo.load for live multi-user use

---

## 13. Complete Reference Code Snippets

### 13.1 Minimal Theme Application

```python
with gr.Blocks(
    title="League Table Manager",
    theme=gr.themes.Soft(
        primary_hue="green",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter"),
    )
) as demo:
    ...
```

### 13.2 Passing CSS

```python
CSS = """
/* paste custom CSS block from section 5 */
"""

with gr.Blocks(title="League Table Manager", css=CSS) as demo:
    ...
```

### 13.3 Colored Status

```python
def make_status(msg):
    if not msg:
        return ""
    is_error = msg.lower().startswith("error")
    bg = "#fee2e2" if is_error else "#dcfce7"
    border = "#dc2626" if is_error else "#16a34a"
    color = "#991b1b" if is_error else "#166534"
    icon = "✗" if is_error else "✓"
    return f'<div style="padding:10px 14px;background:{bg};border-left:4px solid {border};border-radius:6px;color:{color};font-weight:500;">{icon} {msg}</div>'

status_html = gr.HTML(value="")
# In event handler output:
outputs=[league_table, matches_table, status_html]
# And wrap the add_match return:
league_table, history, status_text = add_match(...)
return league_table, history, make_status(status_text)
```

### 13.4 Collapsible Edit/Delete

```python
with gr.Accordion("Delete a Match", open=False):
    with gr.Row():
        delete_row_input = gr.Number(label="Row # to Delete", minimum=1, precision=0, scale=2)
        delete_btn = gr.Button("Delete Row", variant="stop", scale=1)
    delete_preview = gr.HTML()

with gr.Accordion("Edit a Match", open=False):
    update_row_input = gr.Number(label="Row # to Edit", minimum=1, precision=0)
    with gr.Row():
        update_home_team = gr.Dropdown(choices=initial_teams, label="New Home Team", allow_custom_value=True)
        update_away_team = gr.Dropdown(choices=initial_teams, label="New Away Team", allow_custom_value=True)
    with gr.Row():
        update_home_goals = gr.Number(label="Home Goals", value=0, minimum=0, precision=0)
        update_away_goals = gr.Number(label="Away Goals", value=0, minimum=0, precision=0)
    update_btn = gr.Button("Save Changes", variant="secondary")
```

### 13.5 Score Preview Component

```python
score_preview = gr.HTML(value="""
<div style="text-align:center;padding:16px;background:#1e293b;border-radius:12px;
            border:1px solid #334155;color:#64748b;font-style:italic;">
    Select teams and enter goals to preview the score
</div>
""")

def update_score_preview(home, away, hg, ag):
    h = home or "Home"
    a = away or "Away"
    hg = int(hg or 0)
    ag = int(ag or 0)
    h_color = "#22c55e" if hg > ag else ("#ef4444" if hg < ag else "#eab308")
    a_color = "#22c55e" if ag > hg else ("#ef4444" if ag < hg else "#eab308")
    result = "DRAW" if hg == ag else (f"{h} WIN" if hg > ag else f"{a} WIN")
    return f"""
    <div style="text-align:center;padding:16px;background:#1e293b;border-radius:12px;border:1px solid #334155;">
        <div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">{result}</div>
        <div style="font-size:1.4rem;font-weight:800;font-family:Inter,sans-serif;">
            <span style="color:#f1f5f9;">{h}</span>
            <span style="color:{h_color};margin:0 12px;">{hg}</span>
            <span style="color:#475569;">—</span>
            <span style="color:{a_color};margin:0 12px;">{ag}</span>
            <span style="color:#f1f5f9;">{a}</span>
        </div>
    </div>
    """

for component in [home_team, away_team, home_goals, away_goals]:
    component.change(
        fn=update_score_preview,
        inputs=[home_team, away_team, home_goals, away_goals],
        outputs=[score_preview]
    )
```

### 13.6 Auto-Refresh Dropdowns After Mutation

```python
def add_match_full(home, away, hg, ag):
    table, history, status = add_match(home, away, hg, ag)
    teams = get_teams_from_matches()
    return (
        table,
        history,
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
    outputs=[
        league_table, matches_table, status_html,
        home_goals, away_goals,
        home_team, away_team,
        update_home_team, update_away_team
    ]
)
```

### 13.7 Row Selection to Auto-Populate Delete Input

```python
def on_match_row_select(evt: gr.SelectData):
    return evt.index[0] + 1  # convert 0-indexed to 1-indexed row number

matches_table.select(
    fn=on_match_row_select,
    outputs=[delete_row_input]
)
```

---

## Key Takeaways

1. **Gradio's biggest UX lever is custom CSS + gr.HTML.** Themes give you structure; raw HTML gives you full creative control. The league table especially benefits from switching from `gr.Dataframe` to `gr.HTML`.

2. **Information architecture matters more than styling.** Separating "view data" from "modify data" into cleaner tab structures reduces cognitive load even before a single CSS change.

3. **Visual feedback is the cheapest UX win.** Colored success/error statuses, win-rate bars in the table, and score color coding cost little code but dramatically improve readability.

4. **Know Gradio's hard limits.** No real-time push, no sticky layouts, no column-header sorting out of the box. Work with these constraints rather than fighting them.

5. **Font matters for a data-heavy app.** Inter with tabular lining numbers makes the league table significantly easier to scan.
