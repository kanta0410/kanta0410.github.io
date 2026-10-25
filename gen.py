"""DeepSeek で brief.md から index.html を作る。

使い方: uv run --no-project python gen.py [--model deepseek-v4-pro] [--fix "直したいこと"]
--fix を付けると、今の index.html を直させる。使った金額の目安を最後に出す。
"""
import argparse
import json
import pathlib
import re
import urllib.request

HERE = pathlib.Path(__file__).parent
PRICE = {  # 100万トークンあたりのドル(高い方=平日の混む時間)
    "deepseek-v4-pro": (1.32, 3.96),
    "deepseek-flash": (0.3, 1.2),
}


def key():
    for line in (HERE / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit(".env に DEEPSEEK_API_KEY がない")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-v4-pro")
    ap.add_argument("--fix", default="")
    a = ap.parse_args()

    brief = (HERE / "brief.md").read_text(encoding="utf-8")
    system = (
        "あなたは世界で一番の Web デザイナー兼フロントエンドエンジニア。"
        "受け取った指示書から、完成した1枚の index.html だけを ```html のコードブロックで返す。説明は書かない。"
    )
    user = brief
    if a.fix:
        user += "\n\n## 今の index.html\n```html\n" + (HERE / "index.html").read_text(encoding="utf-8") + "\n```\n\n## 直すこと\n" + a.fix

    body = json.dumps({
        "model": a.model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": 32000,
    }).encode()
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key()}"},
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        res = json.load(r)

    text = res["choices"][0]["message"]["content"]
    m = re.search(r"```html\s*(.*?)```", text, re.S)
    html = m.group(1) if m else text
    out = HERE / "index.html"
    if out.exists():
        n = len(list(HERE.glob("history/*.html")))
        (HERE / "history").mkdir(exist_ok=True)
        out.replace(HERE / "history" / f"v{n + 1:02d}.html")
    out.write_text(html, encoding="utf-8")

    u = res.get("usage", {})
    pin, pout = PRICE.get(a.model, (0, 0))
    cost = u.get("prompt_tokens", 0) / 1e6 * pin + u.get("completion_tokens", 0) / 1e6 * pout
    print(f"index.html を書いた。入力 {u.get('prompt_tokens')} / 出力 {u.get('completion_tokens')} トークン、高く見て {cost:.3f} ドル")


if __name__ == "__main__":
    main()
