# Self-Hosting Guide — League Table Manager

Get your own private league tracker running on the internet in under 10 minutes — **no coding experience needed.**

---

## What You'll End Up With

A personal web app hosted for free on Hugging Face Spaces that:
- Tracks football match results for your group of friends
- Shows a live standings table, head-to-head stats, and records
- Is accessible from any phone or browser

---

## Overview of Steps

| Step | What you'll do | Time |
|---|---|---|
| 1 | Create a free Supabase account (the database) | ~3 min |
| 2 | Fork this repo on GitHub | ~1 min |
| 3 | Create a free Hugging Face account & Space | ~3 min |
| 4 | Connect them with two secrets | ~2 min |
| 5 | Push → app is live! | automatic |

---

## Step 1 — Set Up Your Database (Supabase)

Supabase is a free database service. This is where all your match data will live.

### 1.1 — Create an account

1. Go to **https://supabase.com** and click **Start your project**.
2. Sign up with GitHub or email.

### 1.2 — Create a new project

1. Click **New project**.
2. Give it any name (e.g. `my-league`).
3. Set a **Database Password** — write it down somewhere safe, you'll need it if you ever need direct DB access.
4. Choose the region closest to you.
5. Click **Create new project** and wait ~1 minute for it to spin up.

### 1.3 — Create the matches table

1. In your project, click **SQL Editor** in the left sidebar.
2. Click **New query**.
3. Paste the following SQL and click **Run** (the green ▶ button):

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

You should see "Success. No rows returned." — that means it worked.

### 1.4 — Copy your credentials

1. In the left sidebar, click **Project Settings** (the gear icon at the bottom).
2. Click **API** in the settings menu.
3. You'll see two things you need — copy them somewhere (a text file is fine):
   - **Project URL** — looks like `https://abcdefghijkl.supabase.co`
   - **anon public** key (under "Project API Keys") — a long string starting with `eyJ...`

> **Note:** The `anon` key is safe to use here. It only has access to your `matches` table and cannot harm your database.

---

## Step 2 — Fork the Repository on GitHub

1. Go to this repository on GitHub.
2. Click the **Fork** button in the top-right corner.
3. Keep all defaults and click **Create fork**.

You now have your own copy of the code at `https://github.com/YOUR_USERNAME/league-table-manager`.

---

## Step 3 — Create a Hugging Face Space

Hugging Face Spaces is a free hosting platform for Gradio apps.

### 3.1 — Create an account

1. Go to **https://huggingface.co** and click **Sign Up**.
2. Verify your email.

### 3.2 — Create a new Space

1. Click your profile picture → **New Space**.
2. Fill in:
   - **Space name**: anything you like (e.g. `my-league-tracker`)
   - **License**: MIT
   - **SDK**: Select **Gradio**
   - **Space hardware**: CPU Basic (free)
   - **Visibility**: **Private** (so only you can see it)
3. Click **Create Space**.

> You'll land on an empty space page — that's fine, you'll push code to it shortly.

### 3.3 — Create a Hugging Face token

You need a token so GitHub can push to your Space automatically.

1. Click your profile picture → **Settings**.
2. Click **Access Tokens** in the left sidebar.
3. Click **New token**.
4. Give it a name (e.g. `github-deploy`) and set Role to **Write**.
5. Click **Generate a token**.
6. **Copy the token now** — you won't be able to see it again. It starts with `hf_...`.

---

## Step 4 — Connect Everything with Secrets

You need to give GitHub three pieces of information so it can deploy your app to HF Spaces, and you need to give your Space the Supabase credentials.

### 4.1 — Add secrets to your GitHub fork

1. Go to your forked repo on GitHub (`github.com/YOUR_USERNAME/league-table-manager`).
2. Click **Settings** → **Secrets and variables** → **Actions**.
3. Click **New repository secret** for each of the following:

| Secret Name | Value |
|---|---|
| `HF_TOKEN` | Your Hugging Face token (starts with `hf_...`) |
| `HF_USERNAME` | Your Hugging Face username |
| `HF_SPACE_NAME` | The name you gave your Space in Step 3.2 |

### 4.2 — Add secrets to your Hugging Face Space

1. Go to your Space on Hugging Face (`huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_NAME`).
2. Click **Settings** tab.
3. Scroll down to **Repository secrets**.
4. Click **New secret** for each:

| Secret Name | Value |
|---|---|
| `SUPABASE_URL` | Your Supabase Project URL from Step 1.4 |
| `SUPABASE_KEY` | Your Supabase anon key from Step 1.4 |

---

## Step 5 — Deploy!

### Option A — Automatic (via GitHub Actions) ✅ Recommended

Every time you push to the `main` branch of your GitHub fork, GitHub Actions will automatically sync the code to your Hugging Face Space.

To trigger the first deploy:

1. Go to your GitHub fork → **Actions** tab.
2. Click **Deploy to Hugging Face Spaces** in the left sidebar.
3. Click **Run workflow** → **Run workflow**.

Wait ~1 minute. Then go to your Space URL:
```
https://huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_NAME
```

Your app is live!

### Option B — Manual (direct push to HF Space)

If you prefer not to use GitHub Actions, you can push directly:

```bash
git clone https://github.com/YOUR_USERNAME/league-table-manager
cd league-table-manager

# Add your HF Space as a remote
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_NAME

# Push
git push space main
```

When prompted for a password, use your Hugging Face token (`hf_...`).

---

## Using the App

Once the app is live:

1. Open your Space URL in any browser.
2. Go to **Add Match** and enter a match result (team names + score).
3. The **Standings** tab will update automatically.
4. Use **Head to Head** to compare any two players/teams.
5. **Records** shows league milestones.

> **Tip:** Bookmark the Space URL on your phone — it works great on mobile.

---

## Updating the App

If you want to pull in new features from the original repository:

```bash
# In your local clone
git remote add upstream https://github.com/ORIGINAL_OWNER/league-table-manager
git fetch upstream
git merge upstream/main
git push origin main
```

GitHub Actions will automatically redeploy to your Space.

---

## Troubleshooting

### The Space shows "Building..." for a long time

- This is normal on first deploy — it can take 2–3 minutes while it installs dependencies.
- If it stays red/failed, click **Logs** in your Space to see the error.

### "Error connecting to database" in the app

- Double-check that `SUPABASE_URL` and `SUPABASE_KEY` are set correctly in the Space secrets (Step 4.2).
- Make sure you ran the SQL to create the `matches` table (Step 1.3).

### GitHub Actions fails with "Authentication error"

- Check that `HF_TOKEN`, `HF_USERNAME`, and `HF_SPACE_NAME` are all correct in GitHub Secrets (Step 4.1).
- Make sure the token has **Write** access.

### I forgot my Space URL

It's always: `https://huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_NAME`

---

## FAQ

**Is this really free?**
Yes. Supabase free tier gives you 500 MB of database storage and unlimited reads/writes for a small project. Hugging Face free CPU Spaces have no time limits. GitHub Actions free tier gives you 2,000 minutes/month (a deploy takes ~30 seconds).

**Can other people add matches?**
By default yes — anyone with the URL can add/edit matches. If you set your Space to **Private**, only you (and people you invite) can access it.

**Can I rename the teams?**
Team names are whatever you type in the "Add Match" form. They're stored as plain text — just be consistent with spelling.

**What happens to my data if I delete the Space?**
Your data lives in Supabase, not the Space. You can recreate the Space anytime and reconnect the same Supabase credentials — your match history will still be there.

**Can I run this on my own computer instead?**
Yes. See the [README](README.md) for local setup instructions using `uv`.
