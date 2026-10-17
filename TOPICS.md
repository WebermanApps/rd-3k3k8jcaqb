# Research Topics workflow (Possible Topics / Approved Topics)

The dashboard shows two carousels built from `topics.json`:
- **Possible Topics**: every topic with `"status": "possible"`, numbered 01, 02... in file order (newest first). Buttons: Approve, Reject, More Info / Note.
- **Approved Topics**: `"status": "approved"`, no numbers. Rejected topics are hidden.

## Add a new researched topic
1. Write the research: `/workspace/ops/research/<date>-<slug>.md`, and a page in `writeups/` if it has one.
2. Make a 16:9 SVG thumbnail in `topics/` (white, beige #FAF6EE, dark #171717, gold #b08a3e; no emoji).
3. Insert at the TOP of `topics` in `topics.json`:
   `{"id","title","summary","detail","thumb","link","link_label","kind":"topic","status":"possible","notes":[],"answer":"","created","updated"}`
4. Pages are locked: `git pull`, `/workspace/security/pagelock/unlock .`, edit, `check.js` at 393/1470/2560, `/workspace/security/pagelock/relock .`, check every `.html` contains `mwPagesKey`, commit, push. (`topics.json` itself is plain JSON and not locked.)

## How a decision reaches Research
- A tap updates the page at once (localStorage key `research-topics-state`) and calls `MWSubmit.send` (shared `submit.js`, password gate) with
  `{agent:'research', app:'research-dashboard', deck:'research-topics', results:{type:'topic-decision', topic_id, title, decision:'approve'|'reject'|'note', note, at}}`.
- Grok Bot's Deck Results Router delivers rows for agent `research`; or pull them with `/workspace/ops/submit/pull.sh research` (files in `/workspace/ops/submit/inbox/research/`).
- If the password isn't given, nothing is sent and the card goes back to how it was.

## Apply submitted decisions
For each row with `deck: research-topics`:
- `approve`: set that topic's `"status": "approved"` and `updated`. It moves to Approved Topics.
- `reject`: set `"status": "rejected"`.
- `note`: append `{"text": <note>, "at": <time>}` to `notes`, research the question, and write the reply in `"answer"` (shows in the card's expanded detail as "Research: ...").
Then commit and push `topics.json` (and the lock steps above if you touched any HTML), and log it in `/workspace/ops/team-sync/air-reports/research.md`.
The device's local state yields to `topics.json` once the file records a decision.

- 2026-10-16 Anonymous Builder Brand: writeups/anonymous-builder-brand.html (possible)
- 2026-10-17 UpKeep Tech Certifications: writeups/upkeep-tech-certs.html (possible)

## Ongoing projects
An approved topic can become an ongoing project that Max works on right from the dashboard. Model: Coder's Dictionary (`coders-dictionary/`, data in `coders-dictionary/terms.json`).
- The project page lives behind its topic card (same thumbnail, `link` in `topics.json`, status `approved`). Everything for the project stays on that page.
- Max's stars and notes arrive via the submit inbox (`/workspace/ops/submit/pull.sh research`), one deck name per project, e.g. `deck: coders-dictionary` with `results.type` `favorite` (`term`, `starred`) or `note` (`text`).
- Research applies them: update `favorites` in the data file, research note requests, add new items with `"new": "<date>"`, keep all old items, bump the card's `summary`/`updated`, then publish with the page-lock rule.
- 2026-10-17 Condensed Investor Pitch Deck: archived (hidden; writeup kept at writeups/condensed-pitch-deck.html). Max moved the project to UpKeep.
