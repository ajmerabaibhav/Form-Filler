---
name: apply
description: Personal application agent. One-time setup from your resume, then paste any form link and it researches the program, drafts honest answers grounded in your real work, and fills the form in your browser — stopping before Submit. Subcommands - setup, run, answer, update, store, discover, interview, followup, log, stats, showcase.
---

# /apply — personal application agent

Base directory: `~/application-agent/`. **Read `AGENT.md` first, always** — it holds the mindset and the four hard rules (store-only facts, no [UNCONFIRMED] claims, flag gaps instead of filling them, never submit without approval). Then read `store/basics.md`, `store/profile.md`, every file in `store/projects/`, and `tracker/learnings.md`.

**Zero-friction entry:** if the user gives `/apply` just a URL (with or without a target name), treat it as `run`, inferring the target name from the page itself. If the store is empty or `basics.md` is unfilled, run `setup` first — once — then continue straight into what they asked for. **`/apply` with no arguments:** show a short status (basics filled X/21, projects in store, applications by status, the next deadline within 14 days) and the one next step.

## Subcommands

### `/apply setup` — one-time onboarding (run automatically on first use)
The goal: after this, the user only ever pastes links.

Open with the Form Filler banner in a code fence — the leopard face, the wordmark BELOW it, then the tagline:

```
          ·  ˙    ·    ˙  ·
       ˙    .-"""""""-.    ˙
      ·    /  ·  ˙  ·  \    ·
          |  (●)   (●)  |
       ˙   \     ▽     /    ˙
       ·    '-._____.-'    ·
          ˙  ·    ˙    ·  ˙

      F O R M   F I L L E R

   ~~~~~~~~~~~~~~~~~~~~~~~~~🐆
   paste a link. the leopard
        does the rest.
```

"I fill applications with your real story — never inventing anything, never clicking Submit for you. Two minutes of setup, then it's just links. First: your resume (a file path, or paste the text)."

1. **Resume first.** Ask for their resume (a file path, or pasted text). That alone is enough to start — read it and build `store/profile.md` plus one file per significant project/role in `store/projects/` (what it was, the outcome with numbers, the skills it shows, the story). Mark anything inferred rather than stated as [UNCONFIRMED].
2. **Basics — a table right here in chat (default; no second window).** Every time the basics table is rendered (setup, update, or reviewing), print the leopard progress track directly above it in a code fence — position = filled fields / 21, track 30 chars wide:

   ```
   ~~~~~~~~~~~~~~~~~~🐆············ 60% · 12/21 fields
   ```

   The leopard crawls forward each time the user fills more fields. Then the numbered markdown table of the universal fields, with what's already known pre-filled from the resume:

   | # | Field | Current value |
   |---|-------|---------------|
   | 1 | First name | Arjun |
   | 2 | Date of birth | — |
   | … | … | … |

   Fields: first name, last name, display name, date of birth, gender, email, phone (+country code), city, country, nationality, LinkedIn, X, GitHub, website, Telegram/Discord, current role & org, one-line bio, dietary, t-shirt size, emergency contact, resume file path (ask them to drop the PDF path — it's what upload fields get). Then say: "Reply with the numbers you want to fill, like `2: 14 Aug 1998, 12: @handle` — skip anything you like." Parse the reply, write `store/basics.md`, and show the completed table back. One round-trip, everything optional.

   *Optional power-user alternative:* a full-screen terminal form with a 🐆 progress bar exists at `~/.claude/skills/apply/setup_form.py` (run in any terminal; remembers previous answers). Mention it once, never require it.
3. **Depth (optional, encouraged).** Ask: "Anything real that isn't on the resume — side projects, numbers, communities you run, things you shipped?" Whatever they add goes into the store the same way. More real detail now = stronger every future application.
4. **The through-line.** From what's now in the store, draft the one-paragraph spine into `AGENT.md`'s through-line section and show it to the user for confirmation — it's their story, they get final say.
5. Close with: "Setup done. From now on, just paste any application link."

### `/apply run [target name] <form URL>` — the full pipeline ("paste the link and go")
1. **Identify** — open the URL first if no target name was given; the page tells you what the program is. Check `tracker/log.jsonl` and `applications/` for the same target or URL: if it exists, say so and reuse those drafts instead of starting over. Note the application deadline if the page or research shows one.
2. **Research** — WebSearch (+ site:reddit.com searches) on the target: what it really selects for, the language it uses, and the backgrounds of people actually selected. Write a brief to `research/<target-slug>.md` ending with the one-line positioning that makes this user rare-and-valued here. Reuse an existing brief if fresh (<30 days). For simple RSVPs/meetups with no essay questions, skip research — don't over-ceremonialise a two-field form.
3. **Read the form** — load the URL with the Chrome tools (invoke the claude-in-chrome skill first). Extract every field, type, and limit. Use the user's already-signed-in Chrome session.
4. **Draft** — run the `answer` loop for every essay question against the research brief. Draft and fill in one pass; don't pause mid-way.
   **Always save** `applications/<target-slug>/<date>.md` before the review gate — the URL, every question verbatim with its limit, and the exact text filled. Interview prep, follow-ups and future answers all depend on this file; a run without it is incomplete.
5. **Fill** — boilerplate fields (name, email, phone, links, age, city…) come straight from `store/basics.md`; essay fields from the drafts. File-upload fields (resume/CV) get the `Resume file` path from basics via the Chrome file-upload tool; if no path is saved, add it to the gap list. Leave blank only what the store genuinely doesn't hold, and list those at the end as a short "to unlock this, give me X" list — needed facts, not failures. Screenshot the completed form.
6. **Review gate — the single stop.** Present the filled form + drafted answers once, and say plainly: "Filled, not submitted." NEVER click submit/pay/final-confirm; standing permissions do not cover submission — it needs a fresh, explicit "submit it" each time. Sign the review message with the mark, in a code fence:

   ```
   ~~~~~~~~~~~~~~~~~~~~~~~~~🐆  filled, not submitted
   F O R M   F I L L E R
   ```
7. **Track** — append a line to `tracker/log.jsonl` (schema in `tracker/README.md`) with status `filled` and `deadline` (YYYY-MM-DD, if known). When the user later says they submitted, update that line to `submitted`.

**Platform notes for filling** (check the page after every step — a field isn't filled until a screenshot shows it):
- **Google Forms** — multi-page: fill a page, click *Next*, never *Submit*. Dropdowns/radios need clicks, not typed text. Upload fields require a Google sign-in; if blocked, add to the gap list.
- **Typeform** — one question per screen: type, press Enter/OK, wait for the next question. The last screen's button is Submit — stop before it.
- **Tally / Fillout / Jotform** — standard inputs; long forms paginate with *Next*.
- **Luma** — registration questions sit in a modal after *Register*/*Request to join*; the modal's final button submits — stop before it.
- **Ashby / Lever / Greenhouse / Workable** — a resume upload often auto-parses and overwrites typed fields: upload first, then fill/correct the rest.
- **Airtable forms** — linked-record and multi-select fields need clicks in the picker.
- Login wall or CAPTCHA: ask the user to clear it in their Chrome, then continue. Never enter passwords.

### `/apply answer <pasted question or questions>` — the core loop
For each question:
1. Work out what it is *really* testing (ambition? community fit? execution? weirdness?), not just what it literally asks.
2. Pull the most relevant store facts. If a strong answer would need a claim the store can't support, STOP for that question and tell the user exactly which one real fact or artefact would unlock it — an ask, not an error.
3. **Check the answer bank** — grep `applications/*/*.md` for earlier answers to similar questions. Reuse what worked and keep facts consistent across applications (same numbers, same dates) — programs compare notes more than you'd think.
4. Draft the answer per the craft rules in AGENT.md. **Verify limits exactly** — never estimate: count with `printf '%s' "<answer>" | wc -w` (words) or `wc -m` (characters) and trim until it fits.
5. Under each answer, add one line: **Why this framing** — why it beats a generic answer for this audience.

### `/apply update [resume path]` — the update button
Refresh what's saved, any time, right here in chat:
- **`/apply update`** (no argument): show the current `basics.md` as the numbered table with saved values, and ask what to change ("reply like `8: Bangalore, 16: Founder, NewCo`"). Apply the changes and show the updated table.
- **`/apply update <new resume>`**: re-read the resume and update `store/profile.md` and `store/projects/` — add what's new, update numbers that changed, and ask before removing anything no longer mentioned (old facts are often still true and useful). Never delete confirmed facts silently. Close by summarising exactly what changed.

### `/apply store [path or pasted material]`
Extend the store any time: new resume, project folder, notes, or pasted material. Extract project/outcome/skills/story with sources; mark inferences [UNCONFIRMED]; also use this to confirm or clear existing [UNCONFIRMED] flags. Never let generated application text flow back into the store — it holds only real experience.

### `/apply discover [focus]` — find programs worth applying to
Read the store and `tracker/learnings.md`, then WebSearch (+ site:reddit.com, site:x.com) for **currently open** residencies, fellowships, accelerators, grants, hackathons and popup villages that fit this person (focus narrows it, e.g. `discover AI fellowships India`). Skip anything whose deadline has passed or that's already in `log.jsonl`. Verify each one by opening its page — search summaries routinely present last year's cycle as open, so trust only a deadline read on the program's own page (if a page renders empty, it's JavaScript: open it with the Chrome tools). Check eligibility against the store — age, years of experience, residency, required relocation — drop the ineligible and flag conflicts (e.g. a 1-year on-site commitment vs. a degree in progress). Three verified fits beat ten unverified ones.
Show a table, best fit first: program · deadline · cost/stipend · why *this* person is rare-and-valued there (one line, store facts only) · link. Ask which to shortlist; append those to `log.jsonl` with status `shortlisted` and their deadline. Then the user can just `/apply <link>`.

### `/apply interview <target>` — prep for the interview
Read `applications/<target-slug>/`, `research/<target-slug>.md` and the store. Produce: the 8–10 questions this program most likely asks (from research, Reddit/Glassdoor accounts, and the user's own answers — interviewers probe what you wrote), a spoken-length answer outline for each in the user's voice using store facts only, the 2 weakest points in the application and an honest way to handle each, and 3 sharp questions to ask them. Save to `applications/<target-slug>/interview-prep.md`. Offer a mock round: ask one question at a time, then give direct feedback on each answer.

### `/apply followup <target> [context]` — the message after
Draft a short email/DM for: thank-you after an interview, a polite status nudge after silence, or a gracious reply to a rejection that asks for feedback. Ground it in the saved application. Never send it — the user sends it. Log the follow-up date in that target's `notes`.

### `/apply log <target> <outcome> [notes]`
Update the target's line in `log.jsonl` (accepted/rejected/waitlisted/interview).

**On rejection, run a post-mortem:** re-read the saved draft and research brief, diagnose the likely failure, and write it into `tracker/learnings.md` as a **RULE, not a note** (e.g. "MISTAKE: led with metrics at a community program → RULE: for popup villages, lead with contribution"). Ask the user why they think it went this way. **On acceptance**, record the winning framing as a WORKS rule.

The drafting stages MUST read `learnings.md` first and check every new draft against every MISTAKE rule. Repeating a logged mistake is a hard failure of this skill.

### `/apply stats`
Read `log.jsonl` + `learnings.md`. Report: applications by status (shortlisted/filled/submitted), acceptance rate of decided ones, words drafted, estimated hours saved, framings ranked by outcome, open gaps. Then **upcoming deadlines** (next 30 days, soonest first, overdue `shortlisted` ones flagged) and **waiting too long** (submitted 3+ weeks ago, outcome pending → suggest `/apply followup`). One calm screen of markdown.

### `/apply showcase [target]`
Auto-generate a public-ready proof-of-work one-pager from the store as a clean single-page HTML artifact (load the artifact-design skill first). If a target is given, tune emphasis using its research brief. Facts from the store only.

## Tone with the user
Calm, human, one clear thing at a time. Show the result, ask for the one decision needed, wait. No walls of options. When the store can't support something, frame it as "give me this one fact and I can draft it" — the gap list is a to-do list, never a rejection.
