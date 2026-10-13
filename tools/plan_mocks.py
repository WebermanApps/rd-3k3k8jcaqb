"""Extra drawn mockups for planning decks (product-plan). Used by build_deck.py.
Types: lanes, bars, prices, xlist, report, tiers, timeline, landing, persona, lock, offer."""
from svgkit import t, lbl, rect, ln, btn, tag, ic, INK, MUTE, LINE, SOFT, W, H, JUNGLE, TERRA, LAGOON, SAFFRON
EXTRA_IC = {
 "hat": '<path d="M3 17 H21 V19 H3 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/><path d="M5 17 Q5 8 12 8 Q19 8 19 17" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M10 8 V5 H14 V8" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
 "user": '<circle cx="12" cy="8" r="4" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M4 21 Q4 14 12 14 Q20 14 20 21" fill="none" stroke="{c}" stroke-width="{sw}"/>',
 "lock": '<rect x="5" y="10" width="14" height="11" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8 10 V7 Q8 3 12 3 Q16 3 16 7 V10" fill="none" stroke="{c}" stroke-width="{sw}"/>',
 "box": '<path d="M3 7 L12 3 L21 7 V17 L12 21 L3 17 Z M3 7 L12 11 L21 7 M12 11 V21" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M3 7 L12 13 L21 7" fill="none" stroke="{c}" stroke-width="{sw}"/>',
 "doc": '<path d="M6 3 H14 L19 8 V21 H6 Z M14 3 V8 H19" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
 "sun": '<circle cx="12" cy="12" r="4" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 2 V5 M12 19 V22 M2 12 H5 M19 12 H22 M5 5 L7 7 M17 17 L19 19 M19 5 L17 7 M7 17 L5 19" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
 "moon": '<path d="M20 14 A8 8 0 1 1 10 4 A6 6 0 0 0 20 14 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
}
def ic2(kind, x, y, s=16, c=INK, sw=1.8):
    if kind in EXTRA_IC: return f'<g transform="translate({x},{y}) scale({s/24})">' + EXTRA_IC[kind].format(c=c, sw=sw) + '</g>'
    return ic(kind, x, y, s, c, sw)
ACCS = [TERRA, LAGOON, JUNGLE, SAFFRON]
def head(title, a): return rect(0, 0, W, 4, a) + t(14, 30, title, 15, INK, "khand")
def lanes(m, a):
    b = head(m.get("title", "Apps Home"), a) + lbl(14, 48, m.get("sub", "One Tile Per Agent"))
    for i, s in enumerate(m["rows"]):
        col, r = i % 3, i // 3; x, y = 14 + col * 72, 58 + r * 62; c = ACCS[i % 4]
        b += rect(x, y, 66, 54, "#FFFFFF", LINE, 8) + rect(x, y, 66, 3, c) + f'<circle cx="{x+16}" cy="{y+22}" r="9" fill="{c}"/>' + t(x + 16, y + 26, s[0], 10, "#FFFFFF", "khand", anchor="middle") + t(x + 8, y + 45, s, 8, INK, "hind", 600)
    if m.get("foot"): b += lbl(120, 288, m["foot"], MUTE, 7, "middle")
    return b
def bars(m, a):
    b = head(m["title"], a) + lbl(14, 48, m.get("sub", ""))
    mx = max(v for _, v, _ in m["rows"]); base = 236
    n = len(m["rows"]); bw = 150 / n
    for i, (l, v, s) in enumerate(m["rows"]):
        h = max(6, 150 * v / mx); x = 30 + i * (180 / n)
        b += rect(x, base - h, bw, h, a if i == n - 1 else "#D6D0C6", "none", 3) + t(x + bw / 2, base - h - 8, s, 12, INK, "khand", anchor="middle") + t(x + bw / 2, base + 16, l, 9, MUTE, "hind", 600, "middle")
    b += ln(base + 0.5) + lbl(120, 282, m.get("foot", "Analyst Estimate"), MUTE, 7, "middle")
    return b
def prices(m, a):
    b = head(m["title"], a) + lbl(14, 48, m.get("sub", "Published Price"))
    for i, (n, p) in enumerate(m["rows"]):
        y = 56 + i * 34; hl = i == m.get("hl", -1)
        b += rect(14, y, 212, 28, (a + "14") if hl else "#FFFFFF", a if hl else LINE, 6) + t(24, y + 18, n, 9.5, INK, "hind", 600) + t(216, y + 18, p, 10.5, a if hl else INK, "khand", anchor="end")
    return b
def xlist(m, a):
    b = head(m["title"], a) + lbl(14, 48, m.get("sub", ""))
    icon = m.get("icon", "x"); col = MUTE if icon == "x" else a
    for i, s in enumerate(m["rows"]):
        y = 58 + i * 40
        b += rect(14, y, 212, 34, "#FFFFFF", LINE, 6) + ic2(icon, 22, y + 9, 16, col) + t(46, y + 21, s, 9.5, INK, "hind", 600)
    if m.get("foot"): b += lbl(120, 288, m["foot"], MUTE, 7, "middle")
    return b
def report(m, a):
    b = rect(0, 0, W, 64, "#F5F5F5") + rect(0, 0, 3, 64, a) + ic2("sun", 14, 12, 16, a) + t(36, 25, "Morning Report", 12, INK, "khand") + lbl(150, 24, "4:55 AM", MUTE)
    b += t(14, 42, m.get("r1", "3 jobs today, 1 quote waiting"), 8.5, INK, "hind") + t(14, 55, m.get("r2", "Supplier price check done"), 8.5, INK, "hind")
    b += rect(30, 78, 180, 150, "#FFFFFF", INK, 12, 1.4) + rect(30, 78, 180, 4, a) + lbl(42, 100, "Suggestion 2 Of 6") + t(42, 122, m.get("card", "Send Quote Follow-Up"), 12, INK, "khand")
    b += rect(42, 132, 156, 50, SOFT, "none", 6) + t(50, 152, "Drafted by the Office lane", 8, MUTE, "hind") + t(50, 168, "Ready when you say yes", 8, MUTE, "hind")
    for i, s in enumerate(["No", "Maybe", "Love", "Yes"]):
        x = 42 + i * 40; on = s == "Yes"
        b += rect(x, 192, 36, 24, a if on else "#FFFFFF", a if on else INK, 0, 1.1) + t(x + 18, 208, s.upper(), 6.5, "#FFFFFF" if on else INK, "hind", 600, "middle")
    b += ic2("moon", 14, 246, 14, MUTE) + t(34, 257, "Evening Report at 6:00 PM", 9, MUTE, "hind", 600) + lbl(120, 286, "Phone First, Your Brand", MUTE, 7, "middle")
    return b
def tiers(m, a):
    b = head(m["title"], a) + lbl(14, 48, m.get("sub", "Estimate, To Test"))
    for i, (n, p, per, rows) in enumerate(m["rows"]):
        y = 56 + i * 76; hl = i == m.get("hl", 1); c = a if hl else INK
        b += rect(14, y, 212, 68, "#FFFFFF", c, 8, 2 if hl else 1) + t(24, y + 20, n, 11, INK, "khand") + t(216, y + 21, p, 13, c, "khand", anchor="end") + t(216, y + 33, per, 7, MUTE, "hind", 600, "end")
        for j, r in enumerate(rows): b += t(24, y + 40 + j * 12, r, 7.8, MUTE, "hind")
        if hl: b += tag(88, y + 10, "Start Here", a, True, 5.6)
    return b
def timeline(m, a):
    b = head(m["title"], a) + lbl(14, 48, m.get("sub", ""))
    b += f'<line x1="30" y1="66" x2="30" y2="262" stroke="{LINE}" stroke-width="2"/>'
    for i, (d, s1, s2) in enumerate(m["rows"]):
        y = 66 + i * 66; c = ACCS[i % 4]
        b += f'<circle cx="30" cy="{y+8}" r="9" fill="{c}"/>' + t(30, y + 12, str(i + 1), 9, "#FFFFFF", "khand", anchor="middle")
        b += t(48, y + 12, d, 12, INK, "khand") + t(48, y + 28, s1, 8.5, INK, "hind", 600) + t(48, y + 41, s2, 8.5, MUTE, "hind")
    return b
def landing(m, a):
    b = rect(0, 0, W, H, "#FFFFFF") + rect(0, 0, W, 4, a) + lbl(14, 26, m.get("brand", "Your Brand Here"))
    b += t(14, 56, m.get("h1", "Your Business, Run By"), 15, INK, "khand") + t(14, 74, m.get("h2", "A Team Of AI Agents"), 15, INK, "khand")
    b += t(14, 92, "Morning and evening reports on your phone.", 8, MUTE, "hind") + t(14, 104, "Swipe yes or no. Done.", 8, MUTE, "hind")
    b += rect(14, 118, 212, 30, "#FFFFFF", INK, 6, 1.4) + ic2("mail", 22, 125, 16, MUTE) + t(44, 137, "you@business.com", 9, MUTE, "hind")
    b += btn(156, m.get("cta", "Join The Pilot List"), "fill", a, h=28)
    b += rect(14, 198, 212, 50, SOFT, "none", 8) + t(24, 218, m.get("price", "Founding Price Shown Up Front"), 9, INK, "hind", 600) + t(24, 234, "3 pilot spots this month", 8.5, MUTE, "hind")
    b += lbl(120, 278, m.get("foot", "Count Signups And Paid Pilots"), MUTE, 7, "middle")
    return b
def persona(m, a):
    b = rect(0, 0, W, 92, SOFT) + rect(0, 0, W, 4, a) + f'<circle cx="44" cy="48" r="24" fill="#FFFFFF" stroke="{a}" stroke-width="2"/>' + ic2(m.get("icon", "user"), 30, 34, 28, a, 2)
    b += t(80, 44, m["title"], 13, INK, "khand") + t(80, 60, m.get("sub", ""), 8.5, MUTE, "hind")
    for i, s in enumerate(m["rows"]):
        y = 106 + i * 40
        b += rect(14, y, 212, 34, "#FFFFFF", LINE, 6) + ic2("check", 22, y + 9, 16, a) + t(46, y + 21, s, 9.5, INK, "hind", 600)
    return b
def lock(m, a):
    b = rect(0, 0, W, H, "#F7F4EF") + rect(30, 26, 180, 236, "#FFFFFF", INK, 14, 1.4) + rect(30, 26, 180, 4, a)
    b += f'<circle cx="120" cy="74" r="22" fill="{a}1F"/>' + ic2("lock", 106, 60, 28, a, 2) + t(120, 120, m.get("title", "Sign In To Your Team"), 12, INK, "khand", anchor="middle")
    b += rect(46, 134, 148, 26, "#FFFFFF", INK, 5, 1.2) + t(56, 151, "you@business.com", 8.5, MUTE, "hind") + btn(168, "Send Sign-In Link", "fill", INK, x=46, w=148, h=26, size=7.5)
    for i, s in enumerate(m["rows"]): b += ic2("check", 46, 206 + i * 16, 11, JUNGLE) + t(62, 215 + i * 16, s, 8, INK, "hind", 600)
    return b
def offer(m, a):
    b = head(m["title"], a) + rect(14, 44, 212, 66, a + "14", "none", 8) + ic2(m.get("icon", "box"), 24, 58, 30, a, 2) + t(66, 70, m.get("price", ""), 18, a, "khand") + t(66, 92, m.get("per", ""), 8.5, MUTE, "hind", 600)
    for i, s in enumerate(m["rows"]):
        y = 122 + i * 34
        b += ln(y + 28) + ic2("check", 16, y + 6, 14, a) + t(38, y + 18, s, 9.5, INK, "hind", 600)
    return b
EXTRA = {k: v for k, v in globals().items() if k in ("lanes", "bars", "prices", "xlist", "report", "tiers", "timeline", "landing", "persona", "lock", "offer")}
