"""Build deck.json (Research suggestions swipe deck) from deck-source.json.
Usage: python3 tools/build_deck.py [source.json] [out.json]   (run from the repo root; defaults deck-source.json -> deck.json)
Planning decks (product-plan/) also use the types in tools/plan_mocks.py.
Mockup types: qr, mic, walk, review, search, prompt, offline, handoff, list.
"""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from svgkit import t, h1, lbl, rect, ln, dot, btn, tag, ic, esc, INK, MUTE, LINE, SOFT, W, H, TERRA, LAGOON, JUNGLE, SAFFRON
from plan_mocks import EXTRA
ACC = {"terracotta": TERRA, "lagoon": LAGOON, "jungle": JUNGLE, "saffron": SAFFRON}
_n = [0]
def screen(body, bg="#FFFFFF"):
    _n[0] += 1; cid = f"mk{_n[0]}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-hidden="true">'
            f'<clipPath id="{cid}"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#{cid})"><rect width="{W}" height="{H}" fill="{bg}"/>'
            + body + f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
def bar(title, a):
    return rect(0, 0, W, 4, a) + t(14, 30, title, 15, INK, "khand")
def row(y, s, a=None, icon=None, h=30):
    out = rect(14, y, 212, h, "#FFFFFF", LINE, 6)
    x = 24
    if icon: out += ic(icon, 22, y + h / 2 - 7, 14, a or INK); x = 44
    return out + t(x, y + h / 2 + 4, s, 10.5, INK, "hind", 600) + ic("chev", 206, y + h / 2 - 6, 12, MUTE)
def mock(m, a):
    k = m["type"]; b = ""
    if k == "qr":
        b += rect(0, 0, W, H, "#F7F4EF")
        b += rect(18, 26, 86, 120, "#FFFFFF", "#BDB6AA", 10, 1.5) + t(61, 44, m["unit"].upper(), 6.5, MUTE, "hind", 600, "middle", 'letter-spacing="1"')
        b += rect(36, 62, 50, 50, "#FFFFFF", INK, 3, 1.5)
        for i, (x, y) in enumerate([(40,66),(70,66),(40,96)]): b += rect(x, y, 12, 12, INK)
        for x, y in [(57,70),(62,82),(56,90),(72,88),(78,100),(64,102),(58,78),(74,80)]: b += rect(x, y, 5, 5, INK)
        b += t(61, 130, "Scan Me", 9, a, "khand", anchor="middle")
        b += f'<path d="M110 86 H128" stroke="{a}" stroke-width="2" stroke-linecap="round"/><path d="M123 80 L130 86 L123 92" fill="none" stroke="{a}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        b += rect(136, 20, 90, 150, "#FFFFFF", INK, 12, 1.5) + rect(136, 20, 90, 4, a)
        b += t(146, 44, m["unit"], 11, INK, "khand")
        for i, s in enumerate(m["rows"]): b += ln(54 + i * 26, 146, 216) + t(146, 70 + i * 26, s, 7.6, INK, "hind", 600)
        b += lbl(14, 196, "Any phone camera, no app") + ln(206)
        b += row(216, "Opens that unit's page", a, "phone") + row(254, "Sign-in stays on", a, "check")
    elif k == "mic":
        b += bar(m["title"], a) + rect(14, 44, 212, 92, SOFT, "none", 8) + f'<path d="M40 126 L84 82 L112 108 L136 90 L200 126 Z" fill="#E5E0D8"/><circle cx="170" cy="66" r="9" fill="#E5E0D8"/>' + lbl(22, 58, "Photo 2", MUTE) + lbl(14, 156, "Notes")
        b += rect(14, 164, 212, 64, "#FFFFFF", INK, 6, 1.2) + t(24, 186, m["text"], 9.5, INK, "hind")
        b += t(24, 202, "Edit if needed", 8, MUTE, "hind")
        b += f'<circle cx="120" cy="262" r="22" fill="{a}"/>' + ic("mic", 108, 250, 24, "#FFFFFF", 2)
    elif k == "walk":
        b += bar(m["title"], a)
        for i in range(19):
            hgt = [6,12,20,10,26,16,8,22,14,28,10,18,24,8,16,20,12,6,14][i]
            b += rect(22 + i * 10.5, 74 - hgt / 2, 5, hgt, a if i < 11 else "#D6D0C6", "none", 2)
        b += lbl(14, 112, "One note, all stops")
        for i, s in enumerate(m["rows"]):
            y = 122 + i * 46; b += rect(14, y, 212, 38, "#FFFFFF", LINE, 6)
            for j in range(3): b += rect(22 + j * 26, y + 7, 22, 24, SOFT, "#D6D0C6", 3)
            b += t(110, y + 23, s, 9.5, INK, "hind", 600)
        b += btn(266, "Make Document", "outline", INK, h=22, size=8)
    elif k == "review":
        b += bar("Thai Vocab", a) + lbl(14, 56, m["title"]) + t(14, 92, m["count"], 34, a, "khand")
        b += rect(14, 108, 212, 84, SOFT, "none", 10) + t(120, 146, "word", 22, INK, "khand", anchor="middle") + t(120, 170, "Tap to see meaning", 8.5, MUTE, "hind", 400, "middle")
        for i, s in enumerate(m["buttons"]):
            x = 14 + i * 54; on = s == "Good"
            b += rect(x, 206, 50, 30, a if on else "#FFFFFF", a if on else INK, 0, 1.2) + t(x + 25, 225, s.upper(), 7.5, "#FFFFFF" if on else INK, "hind", 600, "middle", 'letter-spacing=".8"')
        b += lbl(14, 258, "Missed words return this session") + lbl(14, 274, "Known words drift to weeks out", MUTE)
    elif k == "search":
        b += bar(m["title"], a) + lbl(14, 56, "Address")
        b += rect(14, 64, 212, 32, "#FFFFFF", INK, 6, 1.5) + ic("search", 22, 72, 16, MUTE) + t(44, 85, m["typed"], 11, INK, "hind", 600) + rect(44 + len(m["typed"]) * 5.6, 72, 1.5, 16, a)
        b += rect(14, 100, 212, 3 * 30 + 4, "#FFFFFF", LINE, 6)
        for i, s in enumerate(m["rows"]):
            y = 102 + i * 30
            if i == 0: b += rect(16, y, 208, 30, a + "1F")
            b += ic("home", 24, y + 8, 14, a if i == 0 else MUTE) + t(46, y + 19, s, 10, INK, "hind", 600 if i == 0 else 400)
        b += rect(14, 214, 212, 30, JUNGLE + "14", "none", 6) + ic("check", 22, 221, 16, JUNGLE) + t(46, 233, m["ok"], 10, JUNGLE, "hind", 600)
        b += btn(258, "Continue", "fill", INK, h=26)
    elif k == "prompt":
        b += bar(m["title"], a) + rect(14, 44, 212, 26, SOFT, "none", 6) + rect(14, 78, 212, 26, SOFT, "none", 6) + rect(14, 112, 140, 26, SOFT, "none", 6)
        b += rect(14, 160, 212, 116, "#FFFFFF", INK, 10, 1.5) + ic("phone", 26, 174, 22, a) + t(56, 190, m["card"], 10.5, INK, "khand")
        b += t(56, 206, "Opens like an app", 8.5, MUTE, "hind")
        b += btn(226, m["yes"], "fill", a, x=26, w=92, h=28) + btn(226, m["no"], "outline", INK, x=126, w=88, h=28)
    elif k == "offline":
        b += bar(m["title"], a) + tag(170, 18, "Offline", a, True, 6.5)
        b += f'<g transform="translate(96,46)"><path d="M4 24 Q24 4 44 24" fill="none" stroke="#BDB6AA" stroke-width="3" stroke-linecap="round"/><path d="M12 32 Q24 20 36 32" fill="none" stroke="#BDB6AA" stroke-width="3" stroke-linecap="round"/><circle cx="24" cy="40" r="3" fill="#BDB6AA"/><path d="M6 6 L42 44" stroke="{a}" stroke-width="3" stroke-linecap="round"/></g>'
        b += lbl(14, 116, "Saved on this phone")
        for i, s in enumerate(m["rows"]): b += row(124 + i * 38, s, a, "check", 32)
        b += lbl(120, 262, "Works in airplane mode", MUTE, 7, "middle")
    elif k == "handoff":
        b += rect(0, 0, W, H, "#F7F4EF") + lbl(14, 30, "Max Voted Love")
        for i, s in enumerate(m["rows"]):
            y = 40 + i * 52; b += rect(14, y, 212, 42, "#FFFFFF", LINE, 8) + ic("heart", 24, y + 12, 18, "#DC2626") + t(50, y + 26, s, 10.5, INK, "hind", 600)
        b += f'<path d="M120 152 V182" stroke="{a}" stroke-width="2.5" stroke-linecap="round"/><path d="M112 175 L120 184 L128 175" fill="none" stroke="{a}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        b += rect(50, 196, 140, 56, "#FFFFFF", INK, 10, 1.5) + f'<circle cx="74" cy="224" r="14" fill="{a}"/>' + t(74, 229, m["to"][0], 13, "#FFFFFF", "khand", anchor="middle") + t(96, 229, m["to"], 13, INK, "khand")
        b += lbl(120, 276, "Owner plans after approval", MUTE, 7, "middle")
    elif k in EXTRA:
        b += EXTRA[k](m, a)
    else:
        b += bar(m.get("title", ""), a)
        for i, s in enumerate(m.get("rows", [])): b += row(48 + i * 40, s, a)
    return screen(b, "#FFFFFF")
def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sp = sys.argv[1] if len(sys.argv) > 1 else "deck-source.json"; op = sys.argv[2] if len(sys.argv) > 2 else "deck.json"
    src = json.load(open(os.path.join(root, sp)))
    out = {k: v for k, v in src.items() if k != "cards"}; out["cards"] = []
    for c in src["cards"]:
        a = ACC.get(c.get("accent"), JUNGLE); d = dict(c); d["accent"] = a
        if c.get("pair"):
            for s in ("optionA", "optionB"):
                o = dict(c[s]); o["svg"] = mock(o.pop("mock"), a); d[s] = o
        else:
            d["svg"] = mock(d.pop("mock"), a)
        assert not re.search("[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(d, ensure_ascii=False)), "emoji found in " + c["id"]
        out["cards"].append(d)
    json.dump(out, open(os.path.join(root, op), "w"), indent=1, ensure_ascii=False)
    print(op + ":", len(out["cards"]), "suggestion cards")
if __name__ == "__main__": main()
