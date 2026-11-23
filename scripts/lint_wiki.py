"""Wiki 健康檢查（Lint）。

用法：
  python3 scripts/lint_wiki.py         # 只檢查
  python3 scripts/lint_wiki.py --fix   # 把 [[頁名|文字]] 轉成 GitHub 可點的相對連結

檢查項目：
  1. 連結指向不存在的頁面
  2. 孤兒頁（沒有任何頁面連到它）
  3. 還留著「待 ingest / 待確認 / 待補」的字樣
  4. source 頁缺少固定段落（CLAUDE.md 規定的 11 段）
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
pages = {p.stem: p for p in WIKI.rglob("*.md")}
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
MDLINK = re.compile(r"\]\(([^)#]+\.md)\)")
SECTIONS = ["基本資料", "背景", "動機", "欲解決的問題", "研究方法", "核心理論",
            "實驗設計", "主要結果", "研究缺口", "與其他論文的關係", "一句話記住"]

def fix_links(path):
    text = path.read_text(encoding="utf-8")
    def sub(m):
        name, label = m.group(1), m.group(2) or m.group(1)
        if name not in pages:
            return m.group(0)  # 留著讓檢查報錯
        rel = pathlib.Path(*[".."] * (len(path.relative_to(WIKI).parts) - 1),
                           pages[name].relative_to(WIKI))
        return f"[{label}]({rel.as_posix()})"
    new = WIKILINK.sub(sub, text)
    if new != text:
        path.write_text(new, encoding="utf-8")

def main():
    fix = "--fix" in sys.argv
    problems, inbound = [], {name: 0 for name in pages}
    for name, path in pages.items():
        if fix:
            fix_links(path)
        text = path.read_text(encoding="utf-8")
        for m in WIKILINK.finditer(text):
            target = m.group(1)
            if target not in pages:
                problems.append(f"[斷鏈] {path.relative_to(ROOT)} → [[{target}]]")
            elif target != name:
                inbound[target] += 1
        for m in MDLINK.finditer(text):
            target = (path.parent / m.group(1)).resolve()
            if not target.exists():
                problems.append(f"[斷鏈] {path.relative_to(ROOT)} → {m.group(1)}")
            elif target.stem in inbound and target.stem != name:
                inbound[target.stem] += 1
        for kw in ("待 ingest", "待確認", "待補", "TODO"):
            if kw in text and name != "log":  # log 是歷史紀錄，不檢查
                problems.append(f"[未完成] {path.relative_to(ROOT)} 還有「{kw}」")
        if path.parent.name == "sources":
            for sec in SECTIONS:
                if not re.search(rf"^## \d+\. .*{sec}", text, re.M):
                    problems.append(f"[缺段落] {path.relative_to(ROOT)} 缺「{sec}」")
    for name, n in inbound.items():
        if n == 0 and name not in ("index", "log"):
            problems.append(f"[孤兒頁] wiki/{pages[name].relative_to(WIKI)} 沒有被任何頁面連結")
    print(f"檢查 {len(pages)} 頁")
    for p in problems:
        print("  " + p)
    print("✅ 全部通過" if not problems else f"❌ {len(problems)} 個問題")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
