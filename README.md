---
title: League Table Manager
emoji: ⚽
colorFrom: green
colorTo: gray
sdk: gradio
sdk_version: 6.2.0
app_file: app.py
pinned: false
license: mit
---

# League Table Manager

> Self-hostable football league tracker — standings, H2H stats, and records. Built with Gradio + Supabase.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face%20Spaces-orange?logo=huggingface)](https://huggingface.co/spaces/asvs/league-table-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

[![Duplicate this Space](https://huggingface.co/datasets/huggingface/badges/resolve/main/duplicate-this-space-md.svg)](https://huggingface.co/spaces/asvs/league-table-manager?duplicate=true)

---

![Standings](product_sc/standings_screen.png)

---

## Features

- **Standings** — Live league table sorted by win rate, with gold/silver/bronze highlights for top performers across key stats
- **Add Match** — Add, edit, and delete matches with a live score preview; match history shown alongside the form
- **Head to Head** — Side-by-side comparison of any two teams: win bar, form guide dots, records, and a full stats table
- **Records** — League-wide milestones: highest-scoring game, biggest margin, first to 100/500 goals, longest win streak

| Standings | Head to Head |
|---|---|
| ![Standings](product_sc/standings_screen.png) | ![H2H](product_sc/h2h_screen.png) |

| Records | Add Match |
|---|---|
| ![Records](product_sc/records_screen.png) | ![Add Match](product_sc/add_match_screen.png) |

---

## Self-Host in 2 Minutes

The fastest way is to duplicate the Hugging Face Space — no coding needed:

**[→ Read the Self-Hosting Guide](SELF_HOSTING.md)**

Or click the badge above to go directly to the duplicate flow.

---

## Local Development

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- A [Supabase](https://supabase.com) project with a `matches` table (see [SELF_HOSTING.md](SELF_HOSTING.md))

### Setup

```bash
# Clone the repo
git clone https://github.com/asvskartheek/league-table-manager.git
cd league-table-manager

# Copy and fill in credentials
cp .env.example .env.local
# Edit .env.local with your SUPABASE_URL and SUPABASE_KEY

# Install dependencies and run
./local_run_space.sh
```

The app will be available at `http://localhost:7860`.

## Environment Variables

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon/service key |

## Database Schema

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

## Project Structure

```
app.py          Entry point — launches the Gradio app
config.py       Environment variables, Supabase client, logging, IST timezone
data.py         In-memory match cache, Supabase loading, table calculations
theme.py        Gradio theme (LeagueTheme) and global CSS
renderers.py    HTML rendering functions for each UI section
crud.py         Add / update / delete match operations
interface.py    Gradio Blocks UI builder
```

See [DOCS.md](DOCS.md) for full technical documentation.

## Tech Stack

- [Gradio](https://gradio.app) — Python web UI framework
- [Supabase](https://supabase.com) — Postgres database with a Python client
- [Hugging Face Spaces](https://huggingface.co/spaces) — free hosting

## License

MIT — see [LICENSE](LICENSE)
