---
type: concept
tags: [RAG, adaptive]
---
# 適應式檢索（Adaptive Retrieval）

## 定義
不對每個問題都用一樣的檢索設定，而是**依問題或檢索結果動態調整**：要不要檢索、檢索幾輪、放幾篇文件。

## 可以「適應」的三個維度
| 維度 | 問的問題 | 代表做法 |
|---|---|---|
| 要不要檢索 | LLM 自己知道答案嗎？ | Mallen et al. (2023) 依實體頻率判斷 |
| 檢索幾輪 | 單步夠嗎，還是要多步？ | [adaptive-rag](../sources/adaptive-rag.md)：難度分類器 A/B/C |
| 每次放幾篇 | 前 5 篇夠嗎？ | [adaptive-k](../sources/adaptive-k.md)：找相似度最大落差當切點 |
| 放哪幾篇（組合） | 在預算內怎麼組出互補證據？ | [adagate](../sources/adagate.md)：效用分數＋替換 |

## 為什麼需要
- 問題難度不一，固定策略不是浪費就是不夠。[adaptive-rag](../sources/adaptive-rag.md)
- 多步檢索雖準，但時間是單步的 3.33 倍（GPT-3.5）。[adaptive-rag](../sources/adaptive-rag.md)

## 方法比較
| 方法 | 需要訓練？ | 需要多次呼叫 LLM？ | 處理多跳？ |
|---|---|---|---|
| [adaptive-rag](../sources/adaptive-rag.md) | 是（T5 分類器） | 視分類結果（C 類才多步） | 是（交給多步策略） |
| [adaptive-k](../sources/adaptive-k.md) | 否 | 否（單次） | 否 |
| [adagate](../sources/adagate.md) | 否 | 是（帳本、缺口靠 LLM） | 是（缺口修補） |

> ⚠️ 描述衝突：[adaptive-k](../sources/adaptive-k.md) 把 Adaptive-RAG 描述成「反覆詢問 LLM 能否回答」，與 [adaptive-rag](../sources/adaptive-rag.md) 原文（事先用分類器判斷）不同，以原文為準。

## 相關概念
[iterative-retrieval](../concepts/iterative-retrieval.md)、[evidence-retrieval](../concepts/evidence-retrieval.md)
