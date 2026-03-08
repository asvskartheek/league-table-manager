# How to Market League Table Manager

> A complete, practical guide for getting real users to discover and use this project.
> Written as a learning document — covers strategy, platform specifics, and exact scripts/content to create.

---

## Table of Contents

1. [Understanding the Product & Target Audiences](#1-understanding-the-product--target-audiences)
2. [The Central Asset: The Self-Hosting Guide](#2-the-central-asset-the-self-hosting-guide)
3. [GitHub Repository SEO](#3-github-repository-seo)
4. [awesome-selfhosted Listing](#4-awesome-selfhosted-listing)
5. [Reddit Strategy](#5-reddit-strategy)
6. [Hacker News — Show HN](#6-hacker-news--show-hn)
7. [Product Hunt Launch](#7-product-hunt-launch)
8. [Dev.to / Hashnode / Medium Articles](#8-devto--hashnode--medium-articles)
9. [Hugging Face Spaces Promotion](#9-hugging-face-spaces-promotion)
10. [Twitter / X Strategy](#10-twitter--x-strategy)
11. [Screen Recording Guide](#11-screen-recording-guide)
12. [Priority Order & Realistic Timeline](#12-priority-order--realistic-timeline)

---

## 1. Understanding the Product & Target Audiences

### What is it?
A free, self-hostable web app to track football league matches between a group of friends or colleagues. Features:
- Live standings table sorted by win rate, with medal highlights
- Add/edit/delete matches with live score preview
- Head-to-Head stats with form guide and win bar
- Records page (milestone cards, win streaks, highest scores)
- Built on Gradio + Supabase, deployable as a Hugging Face Space in minutes

### Who would use this?

| Audience | Where they live online |
|---|---|
| **Friend groups** who play regular 5-a-side / FIFA / foosball | Reddit: r/Foosball, r/FifaCareers, r/sportsand general social media |
| **Office workers** running an internal league | LinkedIn, Slack communities, r/cscareerquestions |
| **Self-hosters / home lab enthusiasts** | r/selfhosted, r/homelab, awesome-selfhosted |
| **Python / Gradio developers** looking for real-world Gradio examples | r/learnpython, Dev.to, HN |
| **Supabase users** looking for starter projects | Supabase Discord, r/Supabase |

### The honest pitch (use this everywhere)
> "My friends and I play football regularly. We had no way to track who was winning across 200+ games, so I built this. It's free, runs on Hugging Face Spaces with one click, and stores data in Supabase. Self-host it for your own group."

This story is **real**, **relatable**, and **not salesy**. It will work on every platform.

---

## 2. The Central Asset: The Self-Hosting Guide

The self-hosting guide is the key marketing asset. Before posting anywhere, make sure it is:

- [ ] Clear on what the app looks like (screenshots already in `product_sc/` — embed them)
- [ ] Shows the **one-click Hugging Face Duplicate Space** path first (lowest friction)
- [ ] Shows the local dev setup path second
- [ ] Has a working demo link (the HF Space at `asvs/league-table-manager`)
- [ ] Lists all environment variables with clear explanations
- [ ] Has a Supabase table creation SQL snippet someone can paste directly

**Why this matters:** Every Reddit post, tweet, or HN comment will link here. If someone opens it and gets confused in 30 seconds, they leave. The guide is your landing page.

---

## 3. GitHub Repository SEO

GitHub has its own internal search engine, and repositories also rank on Google. Both matter.

### Improvements to make right now

**Repository description (About section — top right on GitHub):**
```
Self-hostable football league tracker — standings, H2H stats, and records. Built with Gradio + Supabase.
```
Keep it under 15 words. Start with the main use case.

**GitHub Topics to add (the tag badges):**
```
football, sports, league-table, self-hosted, gradio, supabase, python, statistics, open-source, standings
```
Topics are indexed by GitHub search AND Google. Add at least 8.

**README improvements:**
- Add a GIF or screenshot at the very top — before any text. GitHub renders images inline. First impressions matter.
- Add a "Live Demo" badge/link right at the top pointing to your HF Space
- Add a "Deploy to HF Spaces" button (HF provides this — see their docs)

**Star count matters:** Every time you share anywhere, people who find it interesting will star it. Even 50 stars makes it look credible. Ask friends to star it.

---

## 4. awesome-selfhosted Listing

`awesome-selfhosted` is a GitHub repository with 220k+ stars. It's basically a curated directory of self-hosted apps. Getting listed here is one of the highest-value SEO moves because:
- It is linked from thousands of blog posts and reddit comments
- It shows up in Google searches for "self-hosted X"
- It gives your project a permanent backlink from a trusted source

### Is it eligible?
The app needs to be self-hosted (not just cloud SaaS). Since users can run it locally or on their own HF account — **yes, it qualifies**.

### Where to list it
The closest category is likely: **Sports & Entertainment** or possibly **Personal Dashboards**. Check their categories file first.

### How to submit

1. Fork `awesome-selfhosted/awesome-selfhosted` on GitHub
2. Find the right alphabetical position in the right category
3. Add one line in this exact format:
   ```
   - [League Table Manager](https://github.com/asvs/league-table-manager) - Football league tracker with standings, H2H stats, and match history. Built with Gradio and Supabase. `MIT` `Python`
   ```
   - Description must be **under 250 characters**
   - Must end with license and language tags
   - No trailing period
4. Open a Pull Request titled: `Add League Table Manager to Sports & Entertainment`
5. In the PR description, confirm: actively maintained, MIT license, self-hosted (not SaaS), has a live demo

**Important rules:**
- Only one item per PR
- Software must be actively maintained
- License must be listed on the project

---

## 5. Reddit Strategy

### The golden rule of Reddit marketing

Reddit users hate obvious self-promotion. The trick is to **tell a real story** about why you built it, share it in communities where it's genuinely useful, and be present to answer questions. Don't post and disappear.

Each subreddit has different rules. Read them before posting. Breaking rules gets your post removed and can get you banned.

---

### Subreddit 1: r/selfhosted (~2.4M members)
**Best fit.** This community is exactly for this type of app.

**Rules:** You can share your own projects if they're genuinely self-hosted. No sales pitches. Be helpful in comments.

**Post title:**
```
I built a self-hosted football league tracker for my friends – standings, H2H, and records [GitHub]
```

**Post body template:**
```
My group of friends has been playing football together for years. We had 200+ matches and no way to see who was actually dominating the table, so I built this.

It's a Gradio + Supabase app. You can deploy it to your own Hugging Face Space in about 2 minutes (just duplicate the Space and add your Supabase keys). Or run it locally with uv.

Features:
- League standings sorted by win rate, with gold/silver/bronze highlights
- Add, edit, delete matches
- Head-to-Head comparison for any two teams with form guide and a win bar
- Records page: highest-scoring game, biggest margin, win streaks, goal milestones

It's MIT licensed and free. Would love feedback from anyone who runs their own sports tracker.

GitHub: [link]
Live demo: [HF Space link]
Self-hosting guide: [link]
```

**Post type:** Text post with images attached (use your screenshots from `product_sc/`)

---

### Subreddit 2: r/ProgrammerHumor / r/learnpython (context post)
**Strategy:** Write a relatable story post, not a promo.

**Post idea for r/learnpython:**
```
Title: I built a full Gradio + Supabase app just to settle who's the real champion in my football friend group

...tell the story, share what you learned, link the GitHub at the end as "here's the code if anyone finds it useful"
```

This works because it's educational AND promotional.

---

### Subreddit 3: r/Foosball or r/FIFA or r/socceranalytics
**Strategy:** Post as a user sharing a tool, not as a developer.

```
Title: Anyone else keeping stats on their games? I made a free tracker — here's how ours looks after 238 matches
```
Share the standings screenshot and the records screenshot. Let the visuals do the talking.

---

### Subreddit 4: r/sideprojects
**Strategy:** "I made a thing" posts are native here.

```
Title: Made a football league manager for my friend group — 238 matches later, here's the table
```
Casual, story-driven, include all 4 screenshots.

---

### General Reddit tips
- Post on **Tuesday–Thursday, 9am–12pm EST** — highest engagement windows
- Reply to **every comment** within the first 2 hours
- Don't post the same thing to multiple subreddits on the same day (looks like spam)
- Space posts across subreddits by at least 3–5 days
- Check the subreddit's karma/account age requirements — some require older accounts

---

## 6. Hacker News — Show HN

HN's Show HN section is for things people can actually try. Your HF Space demo qualifies perfectly.

### The rules
- Title must start with "Show HN:"
- Must be something people can use/run
- No superlatives (no "best", "fastest", "first")
- Modest language reads stronger
- Don't ask for upvotes — ask people to try it

### Post title:
```
Show HN: League Table Manager – self-hosted football standings tracker (Gradio + Supabase)
```

### Post body (keep it short — HN readers skim):
```
My friends play football regularly and we had no good way to track standings across hundreds of games.
Built this: live table sorted by win rate, head-to-head comparison with form guide, match records.

Stack: Python, Gradio, Supabase. Runs as a Hugging Face Space (one-click deploy) or locally with uv.
MIT licensed.

Demo: [HF Space URL]
GitHub: [URL]
Self-hosting guide: [URL]
```

### Timing
- Post between **7am–9am EST on a weekday** (ideally Tuesday or Wednesday)
- Be ready to respond to comments for the entire day — HN rewards engagement

### What to expect
- If it gets traction: 50–200 upvotes, comments from developers trying it, potential GitHub stars
- If it doesn't take off immediately: normal, HN is hit or miss. Try again in 6 months with a new angle (e.g., after adding a new feature)

---

## 7. Product Hunt Launch

Product Hunt is a daily leaderboard of new products. Free and open source tools do well here.

### Before launching
- [ ] Create a Product Hunt account and engage with the community for 2–4 weeks first (upvote other products, comment). This builds credibility.
- [ ] Prepare all visual assets: screenshots (you have these), a short GIF/demo video (see Screen Recording section), a tagline, and a description

### Product details to prepare

**Name:** League Table Manager

**Tagline (under 60 chars):**
```
Self-hosted football league tracker for your friend group
```

**Description:**
```
Track matches, standings, and head-to-head stats for your private football league.
Free, open source (MIT), deploys to Hugging Face Spaces in minutes.
Built with Gradio and Supabase — no complex setup needed.
```

**Topics/tags to choose:** `Developer Tools`, `Open Source`, `Sports`, `Self-Hosted`

### Launch day tips
- Post at **12:01am PST** to get a full day of votes
- Share the link on all your social channels at launch
- Ask friends/colleagues to visit and **comment** (not just upvote — PH explicitly says don't ask for upvotes)
- Reply to every comment on launch day
- Consider asking someone with a following to hunt it for you (the "hunter" gets notified to their followers)

---

## 8. Dev.to / Hashnode / Medium Articles

Writing articles is the highest long-term SEO value. These articles rank on Google and bring organic traffic for years.

### Article idea 1 — Technical story (best for Dev.to)

**Title:** `I built a football league tracker with Gradio and Supabase — here's what I learned`

**Content outline:**
1. The problem: 238 matches, no good tracker
2. Why Gradio (fast, Python-native, deploys to HF Spaces for free)
3. Why Supabase (free tier, real Postgres, easy Python client)
4. Architecture walkthrough (the module structure: data.py, crud.py, renderers.py, etc.)
5. One specific technical challenge and how you solved it (e.g., the `data.matches` import pattern)
6. How to self-host it yourself (link to the guide)
7. Screenshots of the final result

**Why this works:** Targets "Gradio tutorial", "Supabase Python", "self-hosted sports tracker" search terms. Ends with a genuine project people can use.

---

### Article idea 2 — Non-technical story (best for Medium)

**Title:** `How I turned 200+ football games with friends into actual data`

**Content outline:**
1. The ritual: the friend group, the matches, the arguments about who was really best
2. The moment you decided to build something instead of using a spreadsheet
3. What the app shows now (include screenshots)
4. How anyone can set it up for free
5. A few fun stats from your own data (e.g., Kane's 77% win rate, Kartheek's 540 goals)

**Why this works:** Human story, no technical jargon, shareable outside developer circles. The "actual data from real matches" angle is compelling.

---

### Platform notes

| Platform | Audience | Best for |
|---|---|---|
| Dev.to | Developers, free, good SEO | Technical article |
| Hashnode | Developers, you own the domain | Technical article (can be your own blog) |
| Medium | General tech readers | Story-driven article |

Cross-posting to multiple platforms is fine — add a "Originally published at..." note at the bottom.

---

## 9. Hugging Face Spaces Promotion

Your app already lives on HF Spaces. HF has a discovery system — Spaces can appear in trending lists and topic searches.

### Optimizations on the Space itself

**Space title:** Make sure it says "League Table Manager" clearly

**README at the top of the Space** (the card people see before opening it):
- Add screenshots embedded in the README (HF renders them)
- Add a clear "What is this?" one-paragraph description
- Add a "Who is this for?" section
- Add a "How to self-host your own" link

**Tags on the Space:** Add tags like `gradio`, `sports`, `statistics`, `self-hosted`. HF Spaces can be filtered by tag.

**Likes:** Ask your network to like the Space on HF. More likes = higher in trending.

### HF Community posts
Hugging Face has a community discussion section. You can write a post introducing your Space to the HF community. It's low-traffic but permanent, and HF users are technically savvy.

---

## 10. Twitter / X Strategy

Twitter is most effective for **ongoing engagement** rather than one-time announcements. Think of it as building an audience over time, not a single launch spike.

### Account setup
If you don't have a developer-focused Twitter presence, start tweeting about what you're building (build in public). Even a small audience of 100–200 engaged followers is more valuable than 0.

### Tweet 1 — Launch tweet (with screenshots)

```
I built a football league tracker for my friends.

238 matches. 1587 goals. One undisputed champion.

It's free, open source, and you can deploy it to @huggingface Spaces in 2 minutes.

[Screenshot of standings]
[Screenshot of H2H]

→ GitHub: [link]
→ Self-host guide: [link]

#buildinpublic #opensource #python #gradio #football
```

**Key:** Attach 2 screenshots. Tweets with images get 2x more engagement.

---

### Tweet 2 — Stats angle (a few days later)

```
Fun thing about having a football league tracker:

After 238 games you can see things like:
• Kane is at 77.27% win rate
• Kartheek has 540 goals (most by any player)
• Longest win streak: 11 games
• Biggest margin ever: 10 goals

Built with Gradio + Supabase.
Free to self-host for your group 👇
[link]
```

---

### Tweet 3 — Technical angle (for developer audience)

```
How I structured a Gradio app that stays fast with 200+ matches:

• data.py holds an in-memory cache (the full matches list)
• All other modules do `import data; data.matches` — NOT `from data import matches`
• This means when load_matches() runs, all modules see the fresh list

Tiny detail, huge difference when you're building something stateful.

Full code: [GitHub link]
```

---

### Hashtags to use
For developer audience: `#buildinpublic #opensource #python #gradio #supabase #selfhosted`
For sports audience: `#football #soccer #sportsanalytics #footballstats`
For general: `#indiehacker #sideproject`

**Rule of thumb:** No more than 3–4 hashtags per tweet. More looks spammy.

### Who to tag / reply to
- Tag `@gradio` and `@supabase` in tweets about the tech stack — they often retweet projects built with their tools
- Tag `@huggingface` when sharing the Space link
- Engage with `#buildinpublic` posts from other developers — this builds reciprocal relationships

---

## 11. Screen Recording Guide

A short demo video (60–90 seconds) is the single most powerful asset for every platform. Here's exactly what to record.

### What you need
- Screen recording software: **OBS** (free, open source) or macOS built-in (Cmd+Shift+5)
- Your HF Space running live in browser
- Optional: a microphone for voiceover

### The 90-second demo script

**Scene 1 (0–10s): Hook — the problem**
> Navigate to the app. Start on the Standings tab.
> Say: "My friends and I play football every week. After 200+ games, we had no idea who was actually the best. So I built this."

**Scene 2 (10–30s): Standings**
> Slowly scroll down the standings table. Point out the gold/silver/bronze medals.
> Say: "Live standings table — sorted by win percentage. Gold, silver, bronze for top 3 in each category. Every match you add updates this in real time."

**Scene 3 (30–50s): Head to Head**
> Click the "Head to Head" tab. Select two teams from the dropdowns.
> Say: "Pick any two players — you get the win bar, their last 5 games as colored dots, full stats side by side, and the complete match history between them."

**Scene 4 (50–65s): Records**
> Click "Records".
> Say: "And the Records tab tracks milestones automatically — highest-scoring game, biggest margin, longest win streak, first to 100 goals."

**Scene 5 (65–90s): Add match + call to action**
> Click "Add Match", quickly show the form.
> Say: "Adding a match takes 5 seconds. The whole thing is free — you can deploy your own copy to Hugging Face Spaces in about 2 minutes. Link in the description."

### Recording tips
- Use a clean browser tab — no bookmarks bar, no other tabs visible
- Record at 1920x1080 minimum
- Keep mouse movements slow and deliberate
- If no voiceover: add captions as text overlays in a free editor like CapCut or DaVinci Resolve

### Where to use the video
- Twitter/X as an embedded video (performs better than just screenshots)
- Product Hunt launch (GIF or MP4 as the thumbnail/demo)
- Dev.to article embedded via Loom or YouTube
- Hugging Face Space README (link to a YouTube/Loom video)
- LinkedIn if you post there

---

## 12. Priority Order & Realistic Timeline

Don't try to do everything at once. Here's a phased approach:

### Phase 1 — Fix the foundation (do this first, before any promotion)
1. Update GitHub repo: description, topics/tags, README with screenshot at top
2. Add live demo link to README
3. Polish the self-hosting guide (screenshots embedded, copy-pasteable SQL for Supabase setup)

**Why first:** Every link you share will point here. If it's rough, the rest doesn't matter.

---

### Phase 2 — Submit to directories (passive, long-term traffic)
1. Submit PR to `awesome-selfhosted`
2. Add better tags/description to HF Space

**Why second:** These take time to process but generate permanent backlinks and organic traffic. Start them early.

---

### Phase 3 — First Reddit post
1. Post to r/selfhosted with screenshots and your story
2. Be present for 24 hours to reply to comments

**Why third:** Reddit can generate a spike of 100–500 GitHub visitors in a day. But you need the foundation ready first.

---

### Phase 4 — Content creation
1. Record the 90-second screen recording
2. Write the technical Dev.to article
3. Write the story-driven Medium post

**Why fourth:** Evergreen content that keeps working after the initial launch.

---

### Phase 5 — Launch platforms
1. Post on Hacker News (Show HN)
2. Launch on Product Hunt (after 2–4 weeks of community engagement there)

**Why last:** These are high-visibility but require preparation and the right moment. Do them after you've practiced the pitch on Reddit.

---

### Phase 6 — Ongoing (Twitter, sustained Reddit)
1. Tweet the launch, then 2–3 more tweets over the following weeks
2. Post to r/sideprojects, r/learnpython as follow-up with new angles
3. Engage with replies and feedback, iterate on the app

---

## Key Principles (Summary)

1. **Tell the real story.** You built this for a real problem with real friends. That story sells itself.
2. **Screenshots first.** People don't read — they scan visuals. Lead with the standings screenshot and the H2H screen.
3. **Low friction for users.** The HF Space one-click deploy is your best pitch. Always mention it.
4. **Be present.** Post, then respond to every comment for 24 hours. Communities reward engagement.
5. **Don't over-promote.** 2–3 posts across platforms over 2 weeks looks organic. 10 posts in 2 days looks like spam.
6. **Tag the tools you used.** @gradio, @supabase, @huggingface all have audiences who care about what people build with their tools.

---

## Resources Referenced

- [awesome-selfhosted](https://awesome-selfhosted.net/) — directory to submit to
- [Show HN Guidelines](https://news.ycombinator.com/showhn.html) — official HN rules
- [Product Hunt Launch Guide](https://www.producthunt.com/launch) — official launch docs
- [How to promote your open-source project](https://m4xshen.dev/posts/promote-open-source-project) — good overview
- [GitHub SEO Guide 2025](https://www.gitdevtool.com/blog/github-seo) — repo optimization
- [Reddit Marketing Tips (Hootsuite)](https://blog.hootsuite.com/reddit-marketing/) — Reddit dos and don'ts
- [Dev.to — Supporting open source on Product Hunt](https://dev.to/crowddotdev/supporting-open-source-projects-on-product-hunt-52pb)
