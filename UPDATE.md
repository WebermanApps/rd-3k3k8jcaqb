# Updating the Research Dashboard
Run right after any Research work.
1. Edit data.json only: set "updated" (ICT time), "status", "open", "decisions", "votes"; add the newest day to the top of "days" (keep about 5, compact).
2. Report bar (`report` object): keep the current Morning or Evening Report at the top of the page.
   - Morning Report: post by 7:00 ICT. Short news of what Research is working on (one or two plain lines is fine; group by `category` when there are more items).
   - Evening Report: at 18:00 ICT, replace the morning report. Cover what got done today and what to expect tomorrow.
   - Shape: `{"type":"Morning"|"Evening","time":"YYYY-MM-DD HH:MM ICT","items":[{"category":"optional","text":"..."}]}`. Omit `category` for plain lines.
3. Public page: no tenant, rent, tax, finance, client or personal data. Titles and one-line summaries only.
4. Check: python3 -m json.tool data.json >/dev/null
5. Before publish, screenshot at phone 390, laptop 1440, and large monitor 2560 (see AGENT-DASHBOARD-SPEC.md).
6. Publish: git add -A && git commit -m "Update dashboard YYYY-MM-DD" && git push  (GitHub Pages redeploys in about 1 minute)
7. Post a line to /workspace/ops/team-feed.md as Research if the change matters.
