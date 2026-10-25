"""index.html をデスクトップとスマホの幅で全体撮影する(確認用)。"""
import sys, pathlib
from playwright.sync_api import sync_playwright
tag = sys.argv[1] if len(sys.argv) > 1 else "cur"
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w, h in [(1280, 860), (390, 844)]:
        pg = b.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
        pg.goto(pathlib.Path(__file__).with_name("index.html").resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){scrollTo(0,y);await new Promise(r=>setTimeout(r,80))}scrollTo(0,0)}")
        pg.wait_for_timeout(800)
        over = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
        pg.screenshot(path=f"shots/{tag}_{w}.png", full_page=True)
        print(w, "横はみ出し px:", over)
    b.close()
