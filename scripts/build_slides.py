"""把 slides/src/<名稱>.html（只有投影片內容）包成可直接瀏覽的完整簡報。

用法：python3 scripts/build_slides.py hover adaptive-rag
每張 <section class="slide"> 必須有 data-wiki="wiki/...md"（可多個，用空白分隔），
頁尾會自動顯示「Wiki 來源」連結。
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/milli722/multihop-rag-wiki/blob/main/"

SHELL = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --ink:#1c2430; --muted:#5b6473; --line:#dcd7cc; --paper:#fbfaf7; --bg:#e9e6df;
  --accent:#0f6b66; --accent-soft:#e3f1ef; --warn:#b45309; --warn-soft:#fdf1e2;
  --bad:#b42318; --good:#1f7a3f;
}}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; height:100%; background:var(--bg); color:var(--ink);
  font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei","Heiti TC",system-ui,sans-serif; }}
#stage {{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center; }}
#deck {{ width:1280px; height:720px; position:relative; transform-origin:center center; }}
.slide {{ position:absolute; inset:0; background:var(--paper); border-radius:6px;
  box-shadow:0 10px 40px rgba(0,0,0,.12); padding:56px 72px 64px; display:none; flex-direction:column; overflow:hidden; }}
.slide.active {{ display:flex; }}
.kicker {{ font-size:15px; letter-spacing:.12em; color:var(--accent); font-weight:700; margin-bottom:8px; }}
h1 {{ font-size:54px; line-height:1.2; margin:0 0 18px; }}
h2 {{ font-size:36px; margin:0 0 26px; line-height:1.3; }}
h3 {{ font-size:22px; margin:0 0 10px; color:var(--accent); }}
p, li {{ font-size:24px; line-height:1.6; }}
ul {{ margin:0; padding-left:1.2em; }} li {{ margin:6px 0; }}
.small, .small li {{ font-size:20px; }}
.muted {{ color:var(--muted); }}
.en {{ color:var(--muted); font-size:.8em; }}
b, strong {{ color:var(--ink); }}
.hl {{ background:linear-gradient(transparent 60%, #fde7c2 60%); font-weight:700; }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:36px; align-items:start; }}
.cols3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }}
.card {{ border:1.5px solid var(--line); border-radius:10px; padding:18px 22px; background:#fff; }}
.card.accent {{ border-color:var(--accent); background:var(--accent-soft); }}
.card.warn {{ border-color:var(--warn); background:var(--warn-soft); }}
.card p, .card li {{ font-size:21px; margin:4px 0; }}
.flow {{ display:flex; align-items:stretch; gap:10px; }}
.flow .step {{ flex:1; border:1.5px solid var(--accent); border-radius:10px; padding:14px 16px; background:#fff; }}
.flow .step > b {{ display:block; color:var(--accent); font-size:20px; margin-bottom:4px; }}
.flow .step > span {{ font-size:19px; line-height:1.5; display:block; }}
.flow .arrow {{ align-self:center; font-size:26px; color:var(--accent); }}
table {{ border-collapse:collapse; width:100%; font-size:21px; background:#fff; }}
th, td {{ border:1px solid var(--line); padding:10px 14px; text-align:left; }}
table.small {{ font-size:20px; }}
th {{ background:#f1eee7; }}
td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
tr.me td {{ background:var(--accent-soft); font-weight:700; }}
.big {{ font-size:64px; font-weight:800; color:var(--accent); line-height:1; }}
.big.bad {{ color:var(--bad); }}
.bars .row {{ display:grid; grid-template-columns:90px 1fr 90px; align-items:center; gap:14px; margin:14px 0; font-size:20px; }}
.bars .track {{ height:30px; background:#eeebe4; border-radius:4px; overflow:hidden; }}
.bars .fill {{ height:100%; background:var(--accent); }}
.bars .val {{ text-align:right; font-weight:700; font-variant-numeric:tabular-nums; }}
.note {{ font-size:16px; color:var(--muted); margin-top:auto; padding-top:10px; }}
.warnbox {{ border-left:5px solid var(--warn); background:var(--warn-soft); padding:10px 16px; font-size:17px; border-radius:4px; }}
details {{ border:1.5px solid var(--line); border-radius:8px; padding:10px 16px; margin:10px 0; background:#fff; font-size:22px; }}
summary {{ cursor:pointer; font-weight:700; }}
details p {{ font-size:19px; margin:8px 0 2px; color:var(--accent); }}
.src {{ position:absolute; left:72px; right:72px; bottom:18px; font-size:13px; color:var(--muted);
  display:flex; justify-content:space-between; border-top:1px solid var(--line); padding-top:8px; }}
.src a {{ color:var(--accent); }}
.cover {{ justify-content:center; background:linear-gradient(135deg,#fbfaf7 55%,var(--accent-soft)); }}
.tag {{ display:inline-block; border:1.5px solid var(--accent); color:var(--accent); border-radius:999px; padding:3px 12px; font-size:15px; margin-right:8px; }}
#bar {{ position:fixed; left:0; top:0; height:4px; background:var(--accent); transition:width .2s; z-index:5; }}
#nav {{ position:fixed; right:16px; top:10px; display:flex; gap:8px; align-items:center; font-size:14px; color:var(--muted); z-index:5; }}
#nav button {{ border:1px solid var(--line); background:#fff; border-radius:6px; padding:6px 12px; font-size:15px; cursor:pointer; }}
#nav a {{ color:var(--muted); margin-right:8px; }}
@media print {{ #nav,#bar {{ display:none; }} #stage {{ position:static; display:block; }}
  #deck {{ transform:none!important; height:auto; }} .slide {{ display:flex; position:relative; page-break-after:always; height:720px; box-shadow:none; }} }}
</style>
</head>
<body>
<div id="bar"></div>
<div id="stage"><div id="deck">
{body}
</div></div>
<div id="nav"><a href="../index.html">← 首頁</a><button id="prev" aria-label="上一張">◀</button><span id="count"></span><button id="next" aria-label="下一張">▶</button></div>
<script>
const REPO = "{repo}";
const slides = [...document.querySelectorAll('.slide')];
slides.forEach((s, i) => {{
  const refs = (s.dataset.wiki || '').split(/\\s+/).filter(Boolean)
    .map(p => `<a href="${{REPO}}${{p}}" target="_blank" rel="noopener">${{p.replace('wiki/','')}}</a>`).join('、');
  const f = document.createElement('div'); f.className = 'src';
  f.innerHTML = `<span>📘 Wiki 來源：${{refs || '—'}}</span><span></span>`;
  s.appendChild(f);
}});
let cur = Math.min(Math.max(parseInt(location.hash.slice(1)) - 1 || 0, 0), slides.length - 1);
function show(n) {{
  cur = Math.min(Math.max(n, 0), slides.length - 1);
  slides.forEach((s, i) => s.classList.toggle('active', i === cur));
  document.getElementById('count').textContent = `${{cur + 1}} / ${{slides.length}}`;
  document.getElementById('bar').style.width = `${{(cur + 1) / slides.length * 100}}%`;
  history.replaceState(null, '', '#' + (cur + 1));
}}
function fit() {{
  const k = Math.min(innerWidth / 1320, innerHeight / 760);
  document.getElementById('deck').style.transform = `scale(${{k}})`;
}}
addEventListener('keydown', e => {{
  if (['ArrowRight','PageDown',' ','Enter'].includes(e.key)) {{ e.preventDefault(); show(cur + 1); }}
  if (['ArrowLeft','PageUp','Backspace'].includes(e.key)) {{ e.preventDefault(); show(cur - 1); }}
  if (e.key === 'Home') show(0);
  if (e.key === 'End') show(slides.length - 1);
}});
document.getElementById('prev').onclick = () => show(cur - 1);
document.getElementById('next').onclick = () => show(cur + 1);
addEventListener('resize', fit); fit(); show(cur);
</script>
</body>
</html>
"""

def build(name):
    src = (ROOT / "slides" / "src" / f"{name}.html").read_text(encoding="utf-8")
    m = re.search(r"<!--\s*title:\s*(.+?)\s*-->", src)
    title = m.group(1) if m else name
    out = SHELL.format(title=title, body=src, repo=REPO)
    (ROOT / "slides" / f"{name}.html").write_text(out, encoding="utf-8")
    print(f"built slides/{name}.html")

if __name__ == "__main__":
    for n in sys.argv[1:]:
        build(n)
