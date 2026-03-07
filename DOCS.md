# Developer Documentation — League Table Manager

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Module Reference](#2-module-reference)
3. [Data Model](#3-data-model)
4. [Database Setup](#4-database-setup)
5. [Running Locally](#5-running-locally)
6. [Deployment (Hugging Face Spaces)](#6-deployment-hugging-face-spaces)
7. [Adding New Features](#7-adding-new-features)
8. [UI / Styling Guide](#8-ui--styling-guide)

---

## 1. Architecture Overview

The app is a Gradio web interface backed by a Supabase (PostgreSQL) database. It follows a simple layered structure:

```
Browser  <-->  Gradio (interface.py)
                    |
             renderers.py   (HTML output)
             crud.py        (writes to DB + cache)
             data.py        (reads from DB, holds cache)
                    |
             config.py      (Supabase client, env vars)
                    |
             Supabase DB    (persistent storage)
```

**In-memory cache:** `data.matches` is a module-level list that acts as a read-through cache. It is populated on startup by `load_matches()` and kept in sync by the CRUD functions. Every UI callback reads from `data.matches` — it never queries Supabase on every render.

**No background threads / queues.** All operations are synchronous. Gradio handles concurrency at the request level; the shared `data.matches` list is only safe here because Gradio's default queue serialises event handlers in a single process.

---

## 2. Module Reference

### `app.py`
Entry point. Calls `build_interface()` and launches the Gradio app with the custom theme and CSS.

```python
from interface import build_interface
from theme import LeagueTheme, CSS

demo = build_interface()
demo.launch(theme=LeagueTheme(), css=CSS)
```

---

### `config.py`
Sets up shared infrastructure that every other module imports.

| Symbol | Type | Purpose |
|---|---|---|
| `logger` | `logging.Logger` | App-wide logger |
| `IST` | `datetime.timezone` | UTC+5:30, used for timestamping matches |
| `SUPABASE_URL` | `str` | Read from `SUPABASE_URL` env var |
| `SUPABASE_KEY` | `str` | Read from `SUPABASE_KEY` env var |
| `supabase` | `supabase.Client` | Initialized Supabase client |

---

### `data.py`
Owns the in-memory match cache and all read/compute operations.

| Symbol | Purpose |
|---|---|
| `matches` | Module-level list. Each entry: `[id, home, away, home_goals, away_goals, datetime_str]` |
| `load_matches()` | Fetches all rows from Supabase `matches` table, rebuilds `data.matches` |
| `get_teams_from_matches()` | Returns sorted list of unique team names from `data.matches` |
| `calculate_table(matches_list)` | Returns a pandas DataFrame with all league stats (P, W, D, L, GF, GA, GD, Pts, GPM, GAM, GDM, WP, #WW, #5GM) |
| `_parse_datetime(dt)` | Parses ISO datetime strings with variable microsecond precision |
| `format_datetime(dt)` | Converts a UTC datetime string to a human-readable IST string |

**Important:** Other modules must access the cache as `data.matches` (not `from data import matches`) so that the reference stays live after `load_matches()` replaces the list object.

---

### `theme.py`
Contains the visual design system.

| Symbol | Purpose |
|---|---|
| `LeagueTheme` | Gradio `Base` subclass — dark slate/green color scheme using Inter font |
| `CSS` | Global CSS string injected into the Gradio app for table headers, buttons, inputs, etc. |

---

### `renderers.py`
Pure functions that take data and return HTML strings. No side effects, no Supabase calls.

| Function | Output |
|---|---|
| `render_league_table_html(matches_list)` | Full standings table with medal/color highlights |
| `render_match_history_html(matches_list)` | Scrollable chronological match list |
| `render_stat_cards(matches_list)` | Grid of record cards (highest scoring, streaks, milestones, etc.) |
| `render_h2h_stats_html(team1, team2, matches_list)` | Hero card with tri-color bar, form dots, mini records, and stats table |
| `get_h2h_match_history_html(team1, team2, matches_list)` | Filtered match history for H2H pair |
| `make_status(msg)` | Green success / red error banner HTML |
| `update_score_preview(home, away, hg, ag)` | Live score preview card HTML |

---

### `crud.py`
Handles all writes to Supabase and keeps `data.matches` in sync.

| Function | Description |
|---|---|
| `add_match(home, away, home_goals, away_goals)` | Validates inputs, inserts into Supabase, appends to `data.matches`. Returns status string. |
| `delete_match_by_id(match_id)` | Deletes from Supabase, removes from `data.matches`. Returns `True`/`False`. |
| `update_match(row_number, new_home, new_away, new_home_goals, new_away_goals)` | Updates Supabase row and mutates the entry in `data.matches`. `row_number` is the 1-based display row from match history (sorted newest-first). Returns status string. |

---

### `interface.py`
Builds the Gradio `Blocks` layout. All UI event handlers (`.click`, `.change`, `demo.load`) are defined here as closures inside `build_interface()`.

**Tabs:**
1. **Standings** — Displays `render_league_table_html` + collapsible column guide
2. **Add Match** — Split layout: add form (left) + match history with delete/edit accordions (right)
3. **Head to Head** — Team dropdowns → H2H stats card + filtered match history
4. **Records** — `render_stat_cards` grid

**Page load refresh:** `demo.load` calls `load_matches()` then re-renders all HTML components and refreshes all dropdown choices. This ensures the UI is always up to date on each browser load.

---

## 3. Data Model

### Match record (in-memory)

```python
[id, home, away, home_goals, away_goals, datetime_str]
# index: 0    1     2         3           4            5
```

All indices are used directly throughout the codebase — no named fields. The datetime string is an ISO 8601 string stored in UTC by Supabase.

### League table columns

| Column | Formula |
|---|---|
| WP (Win Rate %) | `W / P * 100` |
| GPM (Goals Per Match) | `GF / P` |
| GAM (Goals Against per Match) | `GA / P` |
| GDM (Goal Difference per Match) | `(GF - GA) / P` |
| #WW (Whitewash Wins) | Wins where opponent scored 0 |
| #5GM (5-Goal Matches) | Matches where this team scored >= 5 |

Standings are sorted by `WP` descending.

---

## 4. Database Setup

You need a Supabase project with the following table:

```sql
create table matches (
  id          bigint primary key generated always as identity,
  home        text not null,
  away        text not null,
  home_goals  integer not null default 0,
  away_goals  integer not null default 0,
  datetime    timestamptz not null default now(),
  updated_at  timestamptz
);
```

Enable Row Level Security as appropriate for your use case. The anon key is sufficient for read/write if RLS is disabled or permissive policies are set.

Credentials go in `.env.local` (local) or Space secrets (HF deployment):

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

---

## 5. Running Locally

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync

# Set credentials
cp .env.example .env.local
# Edit .env.local

# Run
./local_run_space.sh
# or directly:
uv run app.py
```

The app starts on `http://localhost:7860` by default.

---

## 6. Deployment (Hugging Face Spaces)

1. Create a new Gradio Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Set `app_file: app.py` in the Space metadata (already set in README.md header)
3. Add `SUPABASE_URL` and `SUPABASE_KEY` as Space secrets (Settings → Repository secrets)
4. Push the repo — HF will install from `pyproject.toml` and run `app.py`

The `requirements.txt` file is kept for compatibility; primary dependency management is via `pyproject.toml` + `uv.lock`.

---

## 7. Adding New Features

### Adding a new stat to the standings table

1. In `data.py` → `calculate_table()`: add the new key to the `table` dict initializer, compute its value in the loops, and include it in the `df` column list.
2. In `renderers.py` → `render_league_table_html()`: add a `_rank_map` call for the new column, compute its style via `_medal_style`, add a `<td>` to the row template, and a `<th>` to the header.

### Adding a new tab

1. In `interface.py` → `build_interface()`: add a new `with gr.Tab("Name"):` block inside the `with gr.Tabs():` context.
2. Add the relevant `gr.HTML` component and wire up event handlers.
3. If the tab needs to refresh on page load, add its output component to the `demo.load` outputs list and return its rendered value from `refresh_all()`.

### Adding a new renderer

Add a new function to `renderers.py`. It should:
- Accept `matches_list` (or a subset) as its primary input
- Return an HTML string
- Have no side effects (no Supabase calls, no mutations to `data.matches`)

---

## 8. UI / Styling Guide

### Color palette

| Token | Hex | Usage |
|---|---|---|
| Background | `#0f172a` | Page and input backgrounds |
| Surface | `#1e293b` | Cards, table rows |
| Border | `#334155` | All borders |
| Text primary | `#f1f5f9` | Main text |
| Text secondary | `#94a3b8` | Labels, metadata |
| Text muted | `#64748b` | Empty states, placeholders |
| Green | `#22c55e` | Wins, positive values, accent |
| Red | `#ef4444` | Losses, errors |
| Yellow | `#eab308` | Draws, warnings |
| Blue | `#3b82f6` | Team 1 in H2H |
| Gold | `#f59e0b` | Rank 1 medal |
| Silver | `#b0b8c4` | Rank 2 medal |
| Bronze | `#cd7f32` | Rank 3 medal |

### Fonts

The app uses `Inter` (via Google Fonts) with fallbacks to `ui-sans-serif`, `system-ui`, `sans-serif`. All inline styles reference `font-family:Inter,ui-sans-serif,sans-serif` or `font-family:Inter,sans-serif`.

### Row highlights (standings)

- WP >= 60%: green left border (`#22c55e`)
- WP >= 40%: yellow left border (`#eab308`)
- WP < 40%: red left border (`#ef4444`)
