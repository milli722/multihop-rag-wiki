# Log（只增不改）

## [2026-11-23] setup | 建立 Wiki
- 主題：多跳檢索與事實查核。來源：5 篇論文（使用者之前為研究計畫讀過的）。
- 討論結果：使用者決定**一篇論文產生一份教學簡報**，對象是「要讀懂論文的碩士生」。
- 簡報架構由使用者提出：背景、動機、欲解決問題、研究方法、理論用來處理什麼、內文整理、研究缺口；LLM 建議再加入「實驗設計、主要結果、與其他論文的關係」，使用者同意。
- 建立 CLAUDE.md（schema）、index.md、log.md。

## [2026-11-23] ingest | HoVer (2020)
- **LLM 先提出的重點**：背景（FEVER 87% 單篇）、動機（舊資料集可走捷徑）、三階段造資料、TF-IDF Hit@100 80/39/15%、瓶頸在檢索。
- **LLM 問使用者**：(1) 簡報重點要放「資料怎麼造」還是「為什麼跳越多越難」？(2) 要不要加入使用者自己的研究計畫？
- **使用者回饋**：簡報就是完整講解這份 PDF，不只挑一個重點；先不要放自己的研究計畫。
- **生成**：`sources/hover.md`；新增概念頁 `multi-hop-reasoning`、`fact-verification`、`evidence-retrieval`。
- **檢查發現**：原文表 7 兩列標籤（BERT+GOLD / BERT+RETR）與內文敘述不一致 → 在 source 頁標 ⚠️，簡報只用內文明確的 14.9% / 15.32%。

## [2026-11-23] ingest | Adaptive-RAG (NAACL 2024)
- **LLM 先提出的重點**：三種策略（不檢索／單步／多步）、T5-Large 難度分類器、自動標註（silver + dataset bias）、GPT-3.5 結果 F1 50.91 vs 多步 50.87、時間 1.46 vs 3.33、分類器準確率 54.52%。
- **LLM 問使用者**：(1) 主要數字用哪個模型？(2) 研究缺口是否強調分類器準確率？
- **使用者回饋**：用 GPT-3.5；研究缺口強調分類器可以。
- **生成**：`sources/adaptive-rag.md`；新增概念頁 `adaptive-retrieval`、`iterative-retrieval`；更新 `evidence-retrieval`、`multi-hop-reasoning`。
- **檢查發現**：初稿寫「AdaGATE 把 Self-RAG、Adaptive-k 當比較對象」「Adaptive-k 把 Self-RAG 當比較對象」，但這兩篇還沒 ingest，屬於**未經證實的跨論文連結** → 改成保守寫法，待 ingest 時確認。

## [2026-11-23] ingest | Adaptive-k (EMNLP 2025)、Papelo (FEVER 2024)、AdaGATE (arXiv 2026)
- 使用者決定：**簡報只做 HoVer 與 Adaptive-RAG**，這 3 篇只進 Wiki，因此合併成一輪討論。
- **LLM 先提出的重點**：三篇各自的問題／方法／結果／缺口，並主動指出兩個問題：
  1. Adaptive-k 對 Adaptive-RAG 的描述與 Adaptive-RAG 原文不一致。
  2. AdaGATE 自稱「token 少 2.6×」，但用它自己的表 2 算是 3.1×；且為課程預印本。
- **LLM 問使用者**：(1) 描述衝突要怎麼記？(2) Papelo 要偏重「迭代追問」還是「網路證據可信度」？(3) AdaGATE 要不要標低可信度？
- **使用者回饋**：(1) 兩邊都記、以原文為準 (2) 偏重**迭代追問** (3) 要標記。
- **生成**：`sources/adaptive-k.md`、`sources/papelo-fever2024.md`（方法段落以迭代迴圈為主）、`sources/adagate.md`（frontmatter `credibility: low` ＋ 🔶 註記）、`overview.md`。
- **更新**：5 個概念頁全部補上新論文；`adaptive-retrieval` 新增方法比較表與描述衝突註記；`iterative-retrieval` 新增「下一步查什麼怎麼決定」。
- **回頭修正**：上一輪在 adaptive-rag 頁標「待確認」的跨論文連結 → 已確認 AdaGATE 確實把 Self-RAG、Adaptive-k 當比較對象；Adaptive-k 只在相關研究中提到 Self-RAG。

## [2026-11-23] lint | 全 Wiki
- 第 1 次：log.md 被誤判有「待 ingest／待確認」→ 修改 lint 規則（log 不檢查）。
- 第 2 次：通過；執行 `--fix` 把雙中括號連結轉成 GitHub 可點的連結。

## [2026-11-23] query → slides | HoVer、Adaptive-RAG
- 依 index.md 找頁：`sources/hover.md`、`sources/adaptive-rag.md`，加上概念頁與 overview。
- 每份 15 張；每張標 `data-wiki`。`check_slides.py` 兩份都 0 問題；另做自我測試，確認檢查器會抓到假數字。
- 截圖發現 HoVer v1 有 4 個版面問題 → 修共用 CSS，兩份重新 build。

## [2026-11-23] schema | CLAUDE.md v2
- Ingest 加「數字核對」；跨論文連結只能寫已 ingest 的論文；簡報加「截圖看版面」；Wiki 缺資料要回 Ingest 補。
