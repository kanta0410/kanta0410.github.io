# ハサカン / Hasakan

趣味で AI 研究をしている人の個人サイト。公開先: https://kanta0410.github.io/

- `index.html` — サイト本体(1枚。CSS と JS も中に書いてある)
- `brief.md` — 中身の指示書
- `gen.py` — DeepSeek で `brief.md` から `index.html` を作る(鍵は `.env`。リポジトリには入れない)
- `shoot.py` — デスクトップとスマホの幅で全体を撮って確かめる

## アクセス計測

`index.html` の `</body>` 直前に、Cloudflare が返した Web Analytics のビーコンが1行ある。公開サイトは GitHub Pages のままで、Cloudflare のプロキシは通していない。測るのはこれからのページ表示、パス、参照元。サイト内の `#career` などのアンカーは別パスにならない。名刺の QR は `https://kanta0410.github.io` のままで、パラメータは付けていない。QR・アドレス直打ち・ブックマークは、いずれも参照元が空の直接訪問としてまとまる。

ダッシュボード: [Web Analytics](https://dash.cloudflare.com/) → Analytics & Logs → Web Analytics → `kanta0410.github.io`。サイトタグ `802ac62bc025425698fc737a6df13b43`。トークンはホストに紐づく公開の識別子で、秘密情報ではない。数字が出るのは、この変更が `master` に入り GitHub Pages が更新されたあとで、公式手順では数分かかる。

`gen.py` で `index.html` を作り直すと、この1行は消える。消えたら同じ行を戻す。計測をやめるときは、その1行を消してマージする。アカウント側のサイトも消すなら、ダッシュボードの Manage site から削除する。
