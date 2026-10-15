#!/usr/bin/env python3
"""Viewport check for Research dashboard shelf retry. Usage: python3 tools/check.py URL TAG"""
import sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

url = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else "shelf-retry"
out = Path("/workspace/research-dashboard/shots/shelf-retry")
out.mkdir(parents=True, exist_ok=True)

sizes = [(393, 852, 3), (1470, 956, 2), (2560, 1440, 1)]
chrome = "/usr/bin/google-chrome"
fails = []

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome)
    for w, h, d in sizes:
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=d)
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3500)
        page.evaluate("Promise.all([...document.images].map(i => i.decode().catch(() => 0)))")
        info = page.evaluate(
            """() => {
              const de = document.documentElement;
              const texts = [...document.querySelectorAll('body *')].filter(el => {
                const t = (el.childNodes && [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim()));
                if (!t) return false;
                const st = getComputedStyle(el);
                return st.display !== 'none' && st.visibility !== 'hidden' && parseFloat(st.fontSize) > 0;
              }).slice(0, 80);
              const sizes = texts.map(el => parseFloat(getComputedStyle(el).fontSize)).filter(n => n >= 8);
              const minFs = sizes.length ? Math.min(...sizes) : 16;
              return {
                sw: de.scrollWidth,
                cw: de.clientWidth,
                shelf: !!document.querySelector('[data-shelf]'),
                shelfCards: document.querySelectorAll('[data-shelf] a, [data-shelf] .card, [data-shelf] [class*=deck]').length,
                qc: !!document.getElementById('qc'),
                qcards: document.querySelectorAll('.qcard').length,
                routines: !!document.querySelector('[data-routines]'),
                evening: /Evening Report/i.test(document.body.innerText) && !!document.querySelector('#report-bar .report-type') && /Evening/i.test((document.querySelector('#report-bar .report-type')||{}).textContent||''),
                morning: /Morning/i.test((document.querySelector('#report-bar .report-type')||{}).textContent||''),
                minFs: minFs,
                title: document.title
              };
            }"""
        )
        page.screenshot(path=str(out / f"{tag}-{w}x{h}.png"), full_page=False)
        sideways = info["sw"] > info["cw"] + 1
        print(w, h, info, "errs=", errs)
        if sideways:
            fails.append(f"{w}x{h} sideways scroll sw={info['sw']} cw={info['cw']}")
        if errs:
            fails.append(f"{w}x{h} pageerrors: {errs}")
        if info["minFs"] < 12.9:
            fails.append(f"{w}x{h} min font {info['minFs']}")
        if not info["shelf"] or not info["qc"] or info["qcards"] < 4:
            fails.append(f"{w}x{h} missing shelf/qc (shelf={info['shelf']} qc={info['qc']} qcards={info['qcards']})")
        if info.get("evening"):
            fails.append(f"{w}x{h} Evening Report still showing")
        page.close()
    browser.close()

if fails:
    print("FAIL:", *fails, sep="\n- ")
    sys.exit(1)
print("PASS all viewports")
