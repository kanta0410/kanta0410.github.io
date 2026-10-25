"""og_src.html から X 用のカード画像 og.png(1200x630)を作る。"""
import pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto((here / "og_src.html").resolve().as_uri(), wait_until="networkidle")
    pg.screenshot(path=str(here / "og.png"))
    b.close()
