# Updating the Research Dashboard
Run right after any Research work.
1. Edit data.json only: set "updated" (ICT time), "status", "open", "decisions", "votes"; add the newest day to the top of "days" (keep about 5, compact).
2. Public page: no tenant, rent, tax, finance, client or personal data. Titles and one-line summaries only.
3. Check: python3 -m json.tool data.json >/dev/null
4. Publish: git add -A && git commit -m "Update dashboard YYYY-MM-DD" && git push  (GitHub Pages redeploys in about 1 minute)
5. Post a line to /workspace/ops/team-feed.md as Research if the change matters.
