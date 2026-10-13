# Updating the Research Dashboard
Live URL: https://webermanapps.github.io/rd-3k3k8jcaqb/ (repo WebermanApps/rd-3k3k8jcaqb; old research-dashboard URL is retired). Keep the page noindex.
Run right after any Research work.

## Research Deck (standing format, top of page)
Research suggestions are published as a swipe deck at the top of the page (right under the report bar). The page reads deck.json; never hand-edit deck.json, edit deck-source.json and rebuild.
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
   - Morning Report: post by 7:00 ICT. Short news of what Research is working on (one or two plain lines is fine; group by `category` when there are more items).
   - Evening Report: at 18:00 ICT, replace the morning report. Cover what got done today and what to expect tomorrow.
   - Shape: `{"type":"Morning"|"Evening","time":"YYYY-MM-DD HH:MM ICT","items":[{"category":"optional","text":"..."}]}`. Omit `category` for plain lines.
3. Public page: no tenant, rent, tax, finance, client or personal data. Titles and one-line summaries only.
4. Check: python3 -m json.tool data.json >/dev/null
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
