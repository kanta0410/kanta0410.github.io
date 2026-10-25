"""スマホ幅でメニューを開いて閉じられるかを確かめる。"""
import pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((here / "index.html").resolve().as_uri(), wait_until="networkidle")
    btn = pg.locator("#hamburger, .nav-hamburger").first
    btn.click(); pg.wait_for_timeout(600)
    pg.screenshot(path=str(here / "shots" / "menu_open.png"))
    btn.click(timeout=3000); pg.wait_for_timeout(600)
    ov = pg.evaluate("(() => { const o = document.querySelector('.mobile-overlay, #mobileOverlay, .mobile-menu'); if(!o) return 'no overlay'; const s = getComputedStyle(o); return s.visibility + ' ' + s.opacity + ' ' + s.display + ' ' + o.className; })()")
    print("閉じたあと:", ov); print("JS エラー:", errs or "なし")
    b.close()
