---
title: League Table Manager
emoji: ⚽
colorFrom: green
colorTo: slate
sdk: gradio
sdk_version: 6.2.0
app_file: app.py
pinned: false
license: mit
---

# League Table Manager

A Gradio web app for tracking football matches, standings, and head-to-head statistics. Data is persisted in a Supabase PostgreSQL database.

## Features

- **Standings** — Live league table sorted by win rate, with gold/silver/bronze highlights for top performers across key stats
- **Add Match** — Add, edit, and delete matches with a live score preview; match history shown alongside the form
- **Head to Head** — Side-by-side comparison of any two teams: win bar, form guide dots, records, and a full stats table
- **Records** — League-wide milestones: highest-scoring game, biggest margin, first to 100/500 goals, longest win streak

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- A [Supabase](https://supabase.com) project with a `matches` table (see [DOCS.md](DOCS.md))

### Setup

```bash
# Clone the repo
git clone <repo-url>
cd league-table-manager

# Copy and fill in credentials
cp .env.example .env.local
# Edit .env.local with your SUPABASE_URL and SUPABASE_KEY

# Install dependencies
uv sync

# Run locally
./local_run_space.sh
```

The app will be available at `http://localhost:7860`.

## Environment Variables

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon/service key |

## Deployment

This app is designed to run as a [Hugging Face Space](https://huggingface.co/spaces). Push to the Space repo and set `SUPABASE_URL` and `SUPABASE_KEY` as Space secrets.

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
