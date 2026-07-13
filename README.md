<div align="center">

```
                  ·  ˙    ·    ˙  ·
               ˙    .-"""""""-.    ˙
              ·    /  ·  ˙  ·  \    ·
                  |  (●)   (●)  |
              ˙    \     ▽     /    ˙
               ·    '-._____.-'    ·
                  ˙  ·    ˙    ·  ˙

    ███████╗ ██████╗ ██████╗ ███╗   ███╗
    ██╔════╝██╔═══██╗██╔══██╗████╗ ████║
    █████╗  ██║   ██║██████╔╝██╔████╔██║
    ██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║
    ██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝
    ███████╗██╗██╗     ██╗     ███████╗██████╗
    ██╔════╝██║██║     ██║     ██╔════╝██╔══██╗
    █████╗  ██║██║     ██║     █████╗  ██████╔╝
    ██╔══╝  ██║██║     ██║     ██╔══╝  ██╔══██╗
    ██║     ██║███████╗███████╗███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝

         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~🐆
      paste a link. the leopard does the rest.
```

**Set up once with your resume → paste any application link → the form fills itself → you click Submit.**

*An honest AI application agent that runs inside your own Claude Code. Your data never leaves your laptop.*

**In blind-scored testing, its drafts more than doubled application quality — 7.6 → 16.5 out of 20.** [↓ proof](#does-it-actually-work)

</div>

---

# Form Filler — your honest advocate for applications

You apply to residencies, fellowships, popup villages, hackathons, clubs, and accelerators. Every form asks the same things about you, but each program selects for something different — and most people lose not on facts, but on presentation.

This is a Claude Code skill that acts like the best counsellor money can buy: it knows your real story, researches who each program *actually* selects, and writes every answer as the strongest **honest** version of you — then fills the form in your own browser and stops before Submit.

**Set up once, then just paste links.** Attach your resume, answer a few basics (name, phone, LinkedIn, X, age — the fields every form asks), and you're done. From then on: paste any application URL and the agent researches the program, drafts your answers, and fills the form.

**Hard rules baked in:** it never invents or exaggerates anything — and that's the point, not a limitation. In blind scoring tests, the honest grounded draft beat the inflated one every time; reviewers can smell padding. Every claim traces to real work in your store. If it can't support a claim, it asks you for the missing fact instead of making something up. And it never clicks Submit — you do.

## Install (2 minutes)

Requires [Claude Code](https://claude.com/claude-code) (any paid plan) and the [Claude in Chrome extension](https://claude.com/chrome) for form-filling.

```bash
git clone https://github.com/23029-MUITP/Form-Filler
cp -r Form-Filler/skills/apply ~/.claude/skills/apply
cp -r Form-Filler/template ~/application-agent
```

Then open Claude Code and run:

```
/apply setup
```

That's genuinely the whole learning curve. Three things to remember:

| You type | What happens |
|---|---|
| `/apply setup` | once — reads your resume, fills your basics table |
| `/apply <link>` | every time — researches, drafts, fills the form, stops before Submit |
| `/apply update` | when life changes — edit your table or hand it a new resume |

It asks for your resume (that alone is enough — add more if you want), then shows a table of the basics every form needs (name, email, phone, LinkedIn, X/GitHub, age, city) right in the chat — pre-filled from your resume, and you fill the gaps in one reply. No extra windows. Everything goes into your **store** — the single source of truth about you, as plain files on your machine. The more real detail you give it (numbers, dates, outcomes), the stronger every future application.

(Prefer a full-screen terminal form instead? One ships in the repo — `python3 ~/.claude/skills/apply/setup_form.py` — with a 🐆 walking a progress bar as you fill. Entirely optional.)

**Your memory is permanent.** Set up once; next time you apply anywhere, you just paste the link — every answer draws on what's already saved. Life changed? `/apply update` shows your saved table to edit in one reply, or hand it a new resume — `/apply update resume.pdf` — and it refreshes your projects without silently deleting anything.

## Use

```
/apply <form-url>                      → the whole thing: research → draft → fill; you review and submit
/apply answer <paste any question>     → one tailored, grounded answer + why that framing wins
/apply update [new resume]             → refresh basics (pre-filled form) or re-read a new resume
/apply store <resume / notes / folder> → add more real work to your store any time
/apply log "Program" accepted|rejected → feeds the learning loop (do this every time!)
/apply stats                           → applications, time saved, what framings win
/apply showcase                        → auto-generate a public proof-of-work page from your store
```

## Does it actually work?

We tested it the hard way before releasing it. Six synthetic applicant personas — a student, a SaaS founder, a community organiser, a researcher, an exaggerator, and a beginner — each wrote their own application answers, then the agent drafted the same answers from their real facts. All 22 answers were scored **blind** (shuffled and anonymised, scorer couldn't tell who wrote what) on specificity, selection-fit, verifiability, and voice.

| Result | Number |
|---|---|
| Average answer quality, written alone | **7.6 / 20** |
| Average answer quality, drafted by the agent | **16.5 / 20** |
| Average lift per answer | **+8.9 points — more than 2×** |
| Biggest single jump (buried facts, corporate prose) | 4.5 → 18.5 |

The finding that surprised us: **honesty out-scored exaggeration.** One persona's self-written answer leaned on inflated claims and scored 8/20 ("reads as unverified sales pitch" — blind scorer). The agent refused the inflated claims, drafted only the modest true record, and scored 19/20 ("candid, precise numbers, doesn't inflate"). The no-lying rule isn't ethics theatre — it's what wins.

Honest caveats: quality scores are a reviewer-proxy, not an acceptance guarantee — real programs have competition and luck. And the agent can't invent substance: the beginner persona with nothing shipped barely improved (it told him what to go build first instead). If you have real work, it will present it better than you do.

## Why it gets better over time

Every outcome you log becomes a rule in `tracker/learnings.md` — "this framing won at builder residencies", "leading with metrics failed at community programs". The agent must check every new draft against those rules. Your rejections literally train your future applications.

## What to expect

- If your store is thin, the agent won't pretend otherwise — it will tell you exactly which real artefact (a demo link, a number, a shipped thing) would unlock a stronger answer. That list is the highest-value output it can give you early on.
- Form auto-fill works in your own signed-in Chrome session and is best-effort: some login-gated or unusual forms may need you to paste the drafted answers yourself. The drafts are the product; the filling is the convenience.

## Privacy

Everything lives in plain files on your machine (`~/application-agent/`). Nothing is hosted, no telemetry, nothing leaves your computer except the applications you choose to submit. Your data is yours — this project never sees it.

## License

MIT
