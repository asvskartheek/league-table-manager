# Self-Hosting Guide — League Table Manager

Get your own private league tracker running on the internet in under 10 minutes — **no coding experience needed.**

You only need to do two things:
1. **Set up a free database** (Supabase) — where your match data lives
2. **Duplicate this Space** on Hugging Face — one click and you're hosted

---

## Step 1 — Set Up Your Database (Supabase)

Supabase is a free database service. All your match results are stored here.

### 1.1 — Create an account

Go to **https://supabase.com** and click **Start your project**. Sign up with GitHub or email.

### 1.2 — Create a new project

1. Click **New project**.
2. Give it any name (e.g. `my-league`).
3. Set a **Database Password** — anything strong, you won't need it again unless you want direct DB access.
4. Choose the region closest to you.
5. Click **Create new project** and wait about a minute.

### 1.3 — Create the matches table

1. Click **SQL Editor** in the left sidebar.
2. Click **New query**.
3. Paste this SQL and click **Run** (the green ▶ button):

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

You should see **"Success. No rows returned."** — that means it worked.

### 1.4 — Copy your credentials

1. Click **Project Settings** (gear icon, bottom of left sidebar).
2. Click **API**.
3. Copy these two values — paste them into a text file for now:
   - **Project URL** — looks like `https://abcdefgh.supabase.co`
   - **anon public** key — a long string starting with `eyJ...`

> The anon key only has access to your matches table. It's safe to use here.

---

## Step 2 — Duplicate This Space

1. Go to the original Space on Hugging Face (the one you're reading this from).
2. Click the **three-dot menu (⋮)** in the top-right corner of the Space.
3. Click **Duplicate this Space**.
4. You'll be prompted to:
   - Sign in or create a free Hugging Face account if you haven't already
   - Choose a name for your copy (e.g. `my-league-tracker`)
   - Set visibility to **Private** (so only you can access it)
5. Before clicking **Duplicate Space**, you'll see a section called **Variables and secrets**. Add both of these:

   | Name | Value |
   |---|---|
   | `SUPABASE_URL` | Your Project URL from Step 1.4 |
   | `SUPABASE_KEY` | Your anon key from Step 1.4 |

6. Click **Duplicate Space**.

Hugging Face will copy all the code and start building your app. After about 1–2 minutes it'll be live at:

```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

That's it — you're done!

---

## Using the App

1. Open your Space URL in any browser (works great on mobile too).
2. Go to **Add Match** and enter a result — type any team names you like.
3. **Standings** updates automatically.
4. **Head to Head** — compare any two players/teams.
5. **Records** — league milestones and streaks.

> Bookmark the URL on your phone for quick access.

---

## Troubleshooting

**The Space is stuck on "Building..."**
Normal for the first deploy — it installs dependencies. Give it 2–3 minutes. If it goes red, click **Logs** to see what went wrong.

**"Error connecting to database" in the app**
Your Supabase credentials aren't set correctly. Go to your Space → **Settings** → **Repository secrets** and double-check `SUPABASE_URL` and `SUPABASE_KEY`.

**I forgot to add the secrets before duplicating**
Go to your Space → **Settings** → **Repository secrets** → add them there, then click **Restart Space** (Factory reboot).

---

## FAQ

**Is this really free?**
Yes. Supabase free tier: 500 MB storage, unlimited reads/writes for a small project. Hugging Face free CPU Spaces: no time limits.

**Can other people add matches?**
If your Space is **Private**, only you and people you explicitly invite can see it. If **Public**, anyone with the URL can add/edit matches.

**What if I delete the Space by accident?**
Your data is safe in Supabase. Just duplicate the Space again and re-enter the same credentials — your entire match history will still be there.

**Can I rename teams?**
Team names are whatever you type in the Add Match form. Just be consistent with spelling across matches.

**I want to run it on my computer instead**
See the [README](README.md) for local setup instructions.
