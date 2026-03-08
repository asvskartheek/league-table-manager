# Contributing to League Table Manager

Thanks for your interest in contributing! This document covers everything you need to run the project locally and understand the codebase.

---

## Running Locally

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- A [Supabase](https://supabase.com) project with the `matches` table (see schema below)

### Setup

```bash
# Clone the repo
git clone https://github.com/asvskartheek/league-table-manager.git
cd league-table-manager

# Copy and fill in credentials
cp .env.example .env.local
# Edit .env.local — set SUPABASE_URL and SUPABASE_KEY

# Install dependencies and run
./local_run_space.sh
```

The app will be available at `http://localhost:7860`.

### Environment Variables

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon/service key |

---

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

---

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

Full technical documentation is in [DOCS.md](DOCS.md).

---

## Architecture

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

### Key pattern — shared in-memory cache

`data.matches` is a module-level list. All other modules must do:

```python
import data
data.matches  # always the live list
```

**Not** `from data import matches` — that captures a reference at import time and won't reflect updates after `load_matches()` reassigns the list.

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI framework | [Gradio](https://gradio.app) |
| Database | [Supabase](https://supabase.com) (PostgreSQL) |
| Hosting | [Hugging Face Spaces](https://huggingface.co/spaces) |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Language | Python 3.12 |

---

## Deployment

The app is designed to run as a Hugging Face Space. Push to the `origin` remote (HuggingFace) and set `SUPABASE_URL` and `SUPABASE_KEY` as Space secrets.

There is also a GitHub mirror at `github` remote for discoverability:

```bash
git push origin main        # deploy to Hugging Face
git push github main        # update GitHub mirror
```
