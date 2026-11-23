"""簡報檢查：投影片內容是否「有 Wiki 根據」。

用法：python3 scripts/check_slides.py hover adaptive-rag

對每一張 <section class="slide">：
  1. 一定要有 data-wiki，而且指向的檔案存在
  2. 投影片上出現的每個數字（例如 80.02、14.9%、26,171），
     都必須出現在 data-wiki 指定的 Wiki 頁面裡 → 防止 LLM 自己編數字
     （年份、頁碼這類 1～4 位整數若出現在 Wiki 任何一頁也算通過）
結果會附加到 process/check-log.md，作為「檢查紀錄」。
"""
import datetime, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTION = re.compile(r'<section class="slide[^"]*"([^>]*)>(.*?)</section>', re.S)
NUM = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.])\d+(?:\.\d+)?")
ALL_WIKI = " ".join(p.read_text(encoding="utf-8") for p in (ROOT / "wiki").rglob("*.md")).replace(",", "")

def plain(fragment):
    fragment = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return html.unescape(fragment)

def check(name):
    src = (ROOT / "slides" / "src" / f"{name}.html").read_text(encoding="utf-8")
    results = []
    for i, m in enumerate(SECTION.finditer(src), 1):
        attrs, body = m.group(1), m.group(2)
        wm = re.search(r'data-wiki="([^"]*)"', attrs)
        refs = wm.group(1).split() if wm else []
        issues = []
        if not refs:
            issues.append("沒有標註 data-wiki 來源")
        texts = []
        for r in refs:
            p = ROOT / r
            if not p.exists():
                issues.append(f"來源檔不存在：{r}")
            else:
                texts.append(p.read_text(encoding="utf-8"))
        wiki = " ".join(texts).replace(",", "")
        for raw in sorted(set(NUM.findall(plain(body)))):
            n = raw.replace(",", "")
            if n in wiki:
                continue
            if re.fullmatch(r"\d{1,4}", n) and n in ALL_WIKI:
                continue  # 小整數／年份：其他 Wiki 頁有即可
            issues.append(f"數字 {raw} 在來源 Wiki 頁找不到")
        results.append((i, refs, issues))
    return results

def main(names):
    lines, total = [], 0
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    for name in names:
        res = check(name)
        bad = [r for r in res if r[2]]
        total += sum(len(r[2]) for r in res)
        print(f"== {name}: {len(res)} 張投影片，{len(bad)} 張有問題")
        lines.append(f"\n### [{stamp}] check_slides | {name}：{len(res)} 張，{len(bad)} 張有問題")
        for i, refs, issues in bad:
            for msg in issues:
                print(f"  第 {i} 張：{msg}")
                lines.append(f"- 第 {i} 張：{msg}")
        if not bad:
            lines.append("- ✅ 全部通過（每張都有 Wiki 來源，數字都能在 Wiki 找到）")
    log = ROOT / "process" / "check-log.md"
    if not log.exists():
        log.write_text("# 檢查紀錄（自動附加）\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("✅ 全部通過" if total == 0 else f"❌ 共 {total} 個問題")
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
