# Updating the Research Dashboard
Live URL: https://webermanapps.github.io/rd-3k3k8jcaqb/ (repo WebermanApps/rd-3k3k8jcaqb; old research-dashboard URL is retired). Keep the page noindex.
Run right after any Research work.

## Research Deck (standing format, top of page)
Research suggestions are published as a swipe deck pinned at the very top of the page, right under the shared top bar and title and above the report (R63). Newest unfinished deck goes there. The page reads deck.json; never hand-edit deck.json, edit deck-source.json and rebuild.
- Morning Deck: publish by 5:00 AM ICT. Today's top 6 to 8 suggestions from /workspace/ops/research/<date>*.md and /workspace/vision/ideas-app/ideas.json. Set "edition":"Morning", "date", "time", "subtitle" ("Top Picks For Mon D, YYYY").
- Evening Recap: at 18:00 ICT. Set "edition":"Evening", subtitle like "Evening Recap, Mon D"; keep cards still waiting on a vote, drop cards Max already voted on, add any new card from the day. Update the report bar at the same time.
- Each card: id (idea id), label (Title Case, short), line (one line of why, real sourced numbers only), project, owner, effort, accent (terracotta | lagoon | jungle | saffron; micro-dose), source {title,url}, next (one suggested next step), mock {type, ...}. Mock types: qr, mic, walk, review, search, prompt, offline, handoff, list (title + rows). Use example data only in mocks.
- A/B pair: when an idea has two real options, set "pair": true with optionA/optionB {label, desc, mock} instead of mock.
- No emoji anywhere (the build fails if one slips in). No tenant, rent, finance, tax, client or personal names. Ideas only; owners build after Max approves.
- Build: python3 tools/build_deck.py && python3 -m json.tool deck.json >/dev/null
- Shots: python3 shots/deck_shot.py http://localhost:<port>/ shots/deck (serve the folder with python3 -m http.server on a free port; 8765 may be taken). Check 393x852 first, then 1470x956, 2560x1440, 1920x1080, 3840x2160: no sideways scroll, deck readable.
- Voting on the page: swipe right = Yes, left = No, Maybe and Love buttons in the middle, Skip under, optional Add Note on every card. Votes and notes stay in the browser (localStorage key rd-deck-<date>) and go to Max only through Share.
1. Edit data.json only: set "updated" (ICT time), "status", "open", "decisions", "votes"; add the newest day to the top of "days" (keep about 5, compact).
2. Report bar (`report` object): keep the current Morning or Evening Report at the top of the page.
   - Morning Report: post by 5:00 ICT (routine runs at 4:41; the old 7:00 rule is dropped). Short news of what Research is working on (one or two plain lines is fine; group by `category` when there are more items).
   - Evening Report: at 18:00 ICT, replace the morning report. Cover what got done today and what to expect tomorrow.
   - Shape: `{"type":"Morning"|"Evening","time":"YYYY-MM-DD HH:MM ICT","items":[{"category":"optional","text":"..."}]}`. Omit `category` for plain lines.
3. Public page: no tenant, rent, tax, finance, client or personal data. Titles and one-line summaries only.
   - Report file (catch-up Oct 14): every Morning (4:41 routine) and Evening (18:00 routine) run also rewrites report.json at the site root, matching data.json's report:
     `{"type":"Morning"|"Evening"|"Fresh Start","title":"Morning Report","time":"YYYY-MM-DD HH:MM ICT","agent":"research","dashboard":"https://webermanapps.github.io/rd-3k3k8jcaqb/","items":<count>}`
     Quick way: python3 -c "import json;r=json.load(open('data.json'))['report'];json.dump({'type':r['type'],'title':r['type']+' Report','time':r['time'],'agent':'research','dashboard':'https://webermanapps.github.io/rd-3k3k8jcaqb/','items':len(r['items'])},open('report.json','w'),indent=1)"
   - The report shows as an open card: the first 2 items are the key lines, the rest sit in a More dropdown (R23). Put the most important lines first.
4. Check: python3 -m json.tool data.json >/dev/null && python3 -m json.tool report.json >/dev/null
5. Before publish, screenshot at iPhone 15 393x852, MacBook Air 1470x956, 2560x1440, 1920x1080 TV, and 3840x2160 4K TV into shots/final (python3 python3 shots/shot.py http://localhost:8765/ shots/final; headless check: no sideways scroll, big TV text).
6. Publish: git add -A && git commit -m "Update dashboard YYYY-MM-DD" && git push  (GitHub Pages redeploys in about 1 minute)
7. Post a line to /workspace/ops/team-feed.md as Research if the change matters.

## Planning Decks (separate pages, e.g. /product-plan/)
- Folder per deck with its own index.html (deck-only copy of the main page script), deck-source.json and deck.json.
- Build: python3 tools/build_deck.py product-plan/deck-source.json product-plan/deck.json
- Extra mock types live in tools/plan_mocks.py: lanes, bars, prices, xlist, report, tiers, timeline, landing, persona, lock, offer.
- Optional card fields (both pages): "source2" {title,url}, "link" {label,url} (renders an Open button), empty "effort" hides the chip; deck-level "close" {title,text,cta} sets the closing card.
- Link each planning deck from a card at the top of deck-source.json (with "link").
- Shots: python3 shots/plan_shot.py http://127.0.0.1:<port>/product-plan/ shots/product-plan http://127.0.0.1:<port>/

## Submit Rules (2026-10-13)
- Submit is shown under every deck at all times, not only on the closing card. It sends the answers so far; the payload lists `answered` and `unanswered` card ids (`partial:true` when some are left).
- After pulling a submission (`/workspace/ops/submit/pull.sh research`), carry every `unanswered` id into the next deck's deck-source.json.
- After a send, the confirmation shows a big "Back to Deck Building" button (https://webermanapps.github.io/branding-djqmb410/decks/). Each deck header has a small "Deck Building" link.

## Answered Cards And Skips (Oct 14, R61 / R64)
- After Max presses Submit, every card he answered (vote or A/B pick) or noted disappears from that deck on his device (ids in localStorage `<deck key>-done`). Only unanswered and skipped cards stay.
- The Submit payload lists `answered` (voted, picked or noted), `unanswered`, and `results.skipped` (cards Max tapped Skip on).
- Next deck: carry every unanswered id. For every skipped id, reword the card more clearly (plainer label and line, clearer A/B options) or drop it; never carry a skipped card unchanged. Give a reworded card a new id suffix like `-r2`.
- Rulebook Clash pass done Oct 14: cream #FDFBF6 page with white cards, Share is a small icon in the top bar corner, report is an open card. Test 393x852, 1470x956 and 2560x1440 before every publish (R11).

## Also in the next 4:41 run (Max's rules, Oct 14 19:43-20:05 ICT)
- Decks only in the top shelf, max 5 total. Move or remove the lower deck sections (Checkout And Next Steps Deck etc.). Use kit/deck-shelf.js/.css, <section data-shelf="shelf.json">, agent 'research' (Ready To Swipe look + swipe counts); ready_shelf.py supports --source and --name. Spec: ops/team-sync/handoffs/ready-to-swipe-look-2026-10-14.md.
- Show swipes completed at the top.
- Only ONE daily report: Morning by 5:00 ICT. Evening Report retired (routine paused). Remove Evening sections and evening late-flags; report.json type is always Morning.
- Routines section goes at the very BOTTOM of the page (above the footer). Mark Research Evening Report as paused in routines.json.
- Questions Center picks: /workspace/ops/team-sync/handoffs/router-to-research.md (apply when a Questions Center ships).
- Then commit, push, add a team-feed line, and reply to Branding Agent with the commit hash.

## Shipped Oct 15 2026 (shelf retry)
- Ready To Swipe shelf at top via kit deck-shelf.js?v=3 + shelf.json (agent research, max 5 decks of 20).
- Old #deckPin / deck.json carousel and lower deck surfaces removed.
- Morning Report only; Evening Report routine paused in routines.json.
- Questions Center below Morning Report (questions.json, Ask for more detail on each).
- Routines at bottom via routines-section.js?v=3.
- Build: `python3 /workspace/style-swipe/tools/ready_shelf.py build <topic> --shelf shelf.json --agent research --name "Name" --source tools/research-....json`
- Check: `python3 tools/check.py http://127.0.0.1:<port>/ local` (393 / 1470 / 2560).
