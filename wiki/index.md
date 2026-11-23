# Index — 多跳檢索與事實查核 LLM Wiki

> LLM 回答問題或做簡報前，先讀這頁找相關頁面。每次 ingest 後更新。

## 總覽
- [overview](overview.md) — 5 篇論文的主線、比較表、跨論文觀察、原文矛盾彙整

## Sources（論文，一篇一頁）
| 頁面 | 摘要 | 年份 | 簡報 |
|---|---|---|---|
| [hover](sources/hover.md) | 最多 4-hop 的查核資料集；證明跳越多越難找齊證據 | 2020 | ✅ |
| [adaptive-rag](sources/adaptive-rag.md) | 小模型判斷問題難度 → 選不檢索／單步／多步 | 2024 | ✅ |
| [adaptive-k](sources/adaptive-k.md) | 用相似度最大落差決定放幾篇，不訓練、單次檢索 | 2025 | — |
| [papelo-fever2024](sources/papelo-fever2024.md) | LLM 依缺口迭代追問，在開放網路上查核說法 | 2024 | — |
| [adagate](sources/adagate.md) | 帳本追蹤缺口＋效用分數，在 token 預算內替換證據（預印本 🔶） | 2026 | — |

## Concepts（概念，跨論文）
| 頁面 | 摘要 | 出現在 |
|---|---|---|
| [multi-hop-reasoning](concepts/multi-hop-reasoning.md) | 要串多份證據才能回答／查核 | 全部 |
| [fact-verification](concepts/fact-verification.md) | 給說法找證據並判斷真假；標籤設計比較 | hover、papelo |
| [evidence-retrieval](concepts/evidence-retrieval.md) | 找證據的方法與四個核心難題 | 全部 |
| [adaptive-retrieval](concepts/adaptive-retrieval.md) | 依問題動態調整：要不要查、查幾輪、放幾篇 | adaptive-rag、adaptive-k、adagate |
| [iterative-retrieval](concepts/iterative-retrieval.md) | 檢索與推理交替多輪；下一步查什麼怎麼決定 | adaptive-rag、papelo、adagate |

## 其他
- [log](log.md) — 每次 ingest／檢查的時間紀錄
- [Raw sources 出處](../raw/README.md)
