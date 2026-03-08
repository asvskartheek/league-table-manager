# Reddit Posts — League Table Manager
> Ready-to-paste posts for manual submission. Post one per subreddit, spaced 3–5 days apart.

---

## Post 1 — r/selfhosted

**Timing:** Tuesday–Thursday, 9am–12pm EST
**Flair:** Show and Tell
**Screenshots to attach:** `standings_screen.png` + `h2h_screen.png` (attach both as images to the post)

**Title:**
```
I built a self-hosted football league tracker for my friend group — standings, H2H stats, and records [Show and Tell]
```

**Body:**
```
My friends and I have been playing football together for years. After 200+ matches we had no idea who was actually dominating the table — spreadsheets got messy, arguments about "who's really the best" never got settled. So I built something.

**What it does:**
- Live standings table sorted by win percentage, with gold/silver/bronze highlights for top 3
- Head-to-Head comparison for any two players: win bar, form guide (last 5 games as coloured dots), full stat breakdown
- Records page: highest-scoring game, biggest winning margin, win streaks, first to 100 goals
- Add/edit/delete matches in seconds with a live score preview

**Self-hosting:**
It runs as a Hugging Face Space — you can duplicate my Space in about 2 minutes, add your Supabase credentials as secrets, and have your own private instance immediately. No Docker, no VPS needed. Or run it locally with `uv run app.py`.

**Stack:** Python + Gradio + Supabase (PostgreSQL). MIT licensed.

- 🔗 GitHub: https://github.com/asvskartheek/league-table-manager
- 🚀 Live demo: https://huggingface.co/spaces/asvs/league-table-manager
- 📖 Self-host guide (in README): https://github.com/asvskartheek/league-table-manager

The self-hosting guide in the README is written for non-technical users — Supabase table SQL is copy-pasteable, and the HF Space duplicate path requires zero coding.

Happy to answer questions about the setup or the stack.
```

---

## Post 2 — r/learnpython

**Timing:** 3–5 days after Post 1, Tuesday–Thursday, 9am–12pm EST
**Flair:** Project (or no flair — check current flair options)
**Screenshots to attach:** `standings_screen.png` + `records_screen.png`

**Title:**
```
I built a full Gradio + Supabase app to settle who's the real champion in my football friend group — here's what I learned
```

**Body:**
```
My friends and I play football every week. After 200+ games we still argued about who was actually the best, so I built a league tracker to end the debate once and for all.

It turned into a proper learning project. Here's what I picked up:

---

**The stack:**
- **Gradio** for the UI — it's underrated for building data apps quickly in pure Python. No HTML/CSS/JS needed.
- **Supabase** as the backend — free PostgreSQL with a Python client that feels like Postgres but with zero server management.
- **Hugging Face Spaces** for hosting — free, no Docker needed, deploys from a git push.

---

**The trickiest part — module-level state in Python:**

I have a `data.py` that holds a global `matches` list (in-memory cache of all match records). The bug I hit: if any other module does `from data import matches`, they get a reference to the *original* list object. When `load_matches()` reassigns `matches = [...]`, those modules still point at the old list.

The fix: every other module does `import data` and then accesses `data.matches`. When the list gets reassigned, all modules see the fresh one because they're going through the module reference, not holding a copy of the object.

Small thing, but it took me a while to debug why my UI was showing stale data after a refresh.

---

**What the app does:**
- League standings sorted by win rate
- Head-to-Head stats for any two players with form guide
- Records page (win streaks, top scorer, highest-scoring games)
- Add/edit/delete matches

---

The code is MIT licensed if anyone wants to use it as a Gradio + Supabase starter:

🔗 https://github.com/asvskartheek/league-table-manager

Happy to explain any part of the architecture in the comments.
```

---

## Post 3 — r/sideprojects

**Timing:** 3–5 days after Post 2, Tuesday–Thursday, 9am–12pm EST
**Flair:** None needed
**Screenshots to attach:** ALL FOUR — `standings_screen.png`, `h2h_screen.png`, `records_screen.png`, `add_match_screen.png` (Reddit allows up to 20 images in a gallery post — use gallery format if possible, otherwise attach all 4)

**Title:**
```
Made a football league manager for my friend group — 200+ matches later, here's the table
```

**Body:**
```
My friends and I have been playing football together for years. We kept arguing about who was actually the best, so I built this to settle it.

It tracks every result and shows:
- A live standings table sorted by win rate (with gold/silver/bronze for top 3)
- Head-to-Head comparison for any two players, with a win bar and form guide
- A Records page — longest win streak, highest-scoring match, biggest margin, goal milestones
- Match history with edit/delete

The whole thing is free to self-host. You duplicate a Hugging Face Space, add two Supabase keys, and you're done. No server setup needed.

Built with Python, Gradio, and Supabase. MIT licensed.

🔗 GitHub + setup guide: https://github.com/asvskartheek/league-table-manager
🚀 Live demo: https://huggingface.co/spaces/asvs/league-table-manager

If your friend group plays any regular sport and you're tired of arguing about who's winning — this is for you.
```

---

## Post 4 — r/socceranalytics

**Timing:** 3–5 days after Post 3, Tuesday–Thursday, 9am–12pm EST
**Flair:** Tool / Project (check current flair options)
**Screenshots to attach:** `h2h_screen.png` + `records_screen.png` (analytics-focused audience cares about data depth, not the add-match form)

**Title:**
```
Built a stat tracker for my 5-a-side group — 200+ matches of data, here's what the numbers look like
```

**Body:**
```
My friends have been playing 5-a-side football for a few years. We recently passed 200 matches logged and I wanted to share what the data looks like — and the tool I built to track it.

**Some numbers from our league:**
- 200+ matches played across multiple seasons
- Win rates range from ~30% to ~77% across players
- Head-to-head records between some pairs are wildly unbalanced despite close overall records
- Form guide (last 5 results) often predicts upcoming match outcomes better than overall win rate

**What the tracker shows:**
- Standings sorted by win percentage
- H2H breakdown for any two players: total record, goal difference, last 5 meetings as a form strip, side-by-side stat cards
- Records: highest-scoring game, biggest winning margin, current and all-time win streaks, first player to reach goal milestones (50, 100, 200...)

I built it as a self-hostable web app so other groups can use it for their own leagues. It's free — runs on Hugging Face Spaces with Supabase as the database. MIT licensed.

🔗 GitHub: https://github.com/asvskartheek/league-table-manager
🚀 Live demo: https://huggingface.co/spaces/asvs/league-table-manager

If your group plays regularly and wants proper stats tracking (beyond a WhatsApp message or a spreadsheet), give it a try. Happy to talk about the data model or the stat calculations in the comments.
```

---

## Posting Checklist

| # | Subreddit | Flair | Screenshots | Status |
|---|---|---|---|---|
| 1 | r/selfhosted | Show and Tell | standings + h2h | ⬜ |
| 2 | r/learnpython | Project | standings + records | ⬜ |
| 3 | r/sideprojects | None | All 4 (gallery) | ⬜ |
| 4 | r/socceranalytics | Tool/Project | h2h + records | ⬜ |

## Rules to follow
- Space posts **3–5 days apart** — same-day cross-posting looks like spam
- Reply to **every comment within 2 hours** of posting — Reddit rewards engagement
- Don't edit the post body after posting (it looks suspicious to mods)
- If a post gets removed, check the subreddit rules and DM the mod before reposting
