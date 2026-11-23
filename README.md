# 多跳檢索與事實查核 LLM Wiki

用 Karpathy 的「LLM Wiki」模式建立的論文知識庫，並從 Wiki 產生教學 HTML 簡報。

🌐 **網站**：https://milli722.github.io/multihop-rag-wiki/

| 內容 | 位置 |
|---|---|
| 教學簡報 | [HoVer](https://milli722.github.io/multihop-rag-wiki/slides/hover.html)、[Adaptive-RAG](https://milli722.github.io/multihop-rag-wiki/slides/adaptive-rag.html) |
| Wiki | [wiki/index.md](wiki/index.md)、[overview](wiki/overview.md)、[log](wiki/log.md) |
| Schema | [CLAUDE.md](CLAUDE.md) |
| Loop / Graph | [process/workflow.md](process/workflow.md) |
| 檢查紀錄 | [process/check-log.md](process/check-log.md) |
| 反思 | [process/reflection.md](process/reflection.md) |
| 原始論文出處 | [raw/README.md](raw/README.md)（PDF 不上傳） |

## 結構
```
CLAUDE.md               Schema：Wiki 規則與流程
raw/                    原始論文（只讀；PDF 不進 git）
wiki/
  index.md  log.md  overview.md
  sources/              一篇論文一頁（11 個固定段落）
  concepts/             跨論文概念頁
slides/src/             投影片內容（每張標 data-wiki）
slides/*.html           build 出來的完整簡報
scripts/
  lint_wiki.py          Wiki 健康檢查（斷鏈、孤兒頁、待確認、缺段落）
  build_slides.py       產生 HTML 簡報
  check_slides.py       檢查投影片來源與數字是否出自 Wiki
process/                流程設計、檢查紀錄、反思
```

## 重跑檢查
```bash
python3 scripts/lint_wiki.py
python3 scripts/build_slides.py hover adaptive-rag
python3 scripts/check_slides.py hover adaptive-rag
```
