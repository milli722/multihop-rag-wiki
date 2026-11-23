# 檢查紀錄（一次實際執行，2026-11-23）

這份紀錄有兩種來源：
- **A. 人工＋LLM 檢查**：ingest、核對數字、看截圖時發現的問題（手寫）
- **B. 自動檢查**：`scripts/lint_wiki.py`、`scripts/check_slides.py` 的執行結果（check_slides 會自動附加到檔案最後面）

## A. 各節點發現的問題與處理

| # | 發生節點 | 發現什麼 | 怎麼發現的 | 處理方式 |
|---|---|---|---|---|
| 1 | 寫 Wiki（HoVer） | 原文表 7 兩列標籤（BERT+GOLD / BERT+RETR）跟內文敘述對不上：內文說最佳模型 67.6%，引言又說 73.7% | 數字核對：拿內文數字回頭對表格 | source 頁標 ⚠️；簡報只用內文明確的 14.9% / 15.32% |
| 2 | 寫 Wiki（Adaptive-RAG） | 初稿寫「AdaGATE 把 Self-RAG、Adaptive-k 當比較對象」，但當時 AdaGATE **還沒 ingest**，是 LLM 從標題猜的 | 寫完重讀「與其他論文的關係」段落時發現 | 改成「ingest 時再確認」；之後 ingest AdaGATE 確認屬實，回頭改正。**並新增規則：跨論文連結只能寫已讀過的論文**（CLAUDE.md v2） |
| 3 | 寫 Wiki（Adaptive-k） | Adaptive-k 把 Adaptive-RAG 描述成「反覆詢問 LLM 能否回答」，跟 Adaptive-RAG 原文（事先用分類器判斷）不同 | 因為 Wiki 已有 adaptive-rag 頁，可以直接對照 | 兩邊都記，以原文為準（使用者同意）；寫進 overview 的矛盾彙整表 |
| 4 | 寫 Wiki（AdaGATE） | 摘要說「比 Adaptive-k 少用 2.6× token」，但用表 2 算：1116 / 360 ≈ 3.1×，三種情境都沒有 2.6× | 數字核對：自己用表格重算倍數 | 標 ⚠️，改寫為「約 3 倍」並附原始數字 |
| 5 | Lint（第一次跑） | `log.md` 被判定有「待 ingest」「待確認」字樣 | `lint_wiki.py` | 判斷是誤報：log 是歷史紀錄本來就會有 → 修改 lint 規則，log 不檢查這項 |
| 6 | 產生 HTML（HoVer v1） | ① 投影片頁尾的頁碼和右下角導覽按鈕重疊 ② 流程方塊中的粗體字被強制換行（如「2-hop 說法」斷開）③ 第 2 張兩張卡片被拉得太高 ④ 字太小，下方大量留白 | 用 Chrome 截圖逐頁看 | 修改共用 CSS：導覽列移到右上、`.flow .step > b` 只套用在標題、grid 改 `align-items:start`、字級放大 → 重新 build 兩份簡報 |
| 7 | 檢查器本身 | 兩份簡報第一次檢查都 0 錯誤，要確認檢查器不是「什麼都放行」 | 自我測試：故意放一個假數字（17.3%）和一張沒標來源的投影片 | 兩個錯誤都被抓到 → 檢查器有效 |

## B. 自動檢查結果

### lint_wiki.py
- 第 1 次：13 頁，2 個問題（#5 誤報）→ 修改規則
- 第 2 次：✅ 全部通過 → 執行 `--fix` 把 `[[頁名]]` 轉成 GitHub 可點的連結
- 第 3 次（--fix 後）：✅ 全部通過
- 第 4 次（寫完簡報紀錄後）：❌ 1 個問題，log.md 裡寫說明文字時打了「[ [頁名] ]」被判定為斷鏈 → 改成文字描述
- 第 5 次：✅ 全部通過

### check_slides.py（自動附加）

### [2026-11-23 11:42] check_slides | hover：15 張，0 張有問題
- ✅ 全部通過（每張都有 Wiki 來源，數字都能在 Wiki 找到）

### [2026-11-23 11:42] check_slides | _selftest：2 張，2 張有問題
- 第 1 張：數字 17.3 在來源 Wiki 頁找不到
- 第 2 張：沒有標註 data-wiki 來源

### [2026-11-23 11:43] check_slides | adaptive-rag：15 張，0 張有問題
- ✅ 全部通過（每張都有 Wiki 來源，數字都能在 Wiki 找到）

### [2026-11-23 11:46] check_slides | hover：15 張，0 張有問題
- ✅ 全部通過（每張都有 Wiki 來源，數字都能在 Wiki 找到）

### [2026-11-23 11:46] check_slides | adaptive-rag：15 張，0 張有問題
- ✅ 全部通過（每張都有 Wiki 來源，數字都能在 Wiki 找到）
