---
type: concept
tags: [retrieval, RAG]
---
# 證據檢索（Evidence Retrieval）

## 定義
從大量文件中找出回答問題或查核說法所需要的段落／句子。在 RAG（檢索增強生成）中，檢索到的內容會放進 LLM 的上下文再生成答案。

## 常見做法
| 做法 | 說明 | 出現於 |
|---|---|---|
| 稀疏檢索 TF-IDF / BM25 | 依字詞重疊打分，快但依賴字面相似 | [hover](../sources/hover.md) baseline |
| 神經重新排序 | 用 BERT 對候選文件重新打分 | [hover](../sources/hover.md) baseline |
| 一次檢索（single-step） | 只檢索一輪 | [hover](../sources/hover.md) baseline、[adaptive-rag](../sources/adaptive-rag.md) |
| 多步檢索（multi-step） | 檢索與推理交替多輪，見 [iterative-retrieval](../concepts/iterative-retrieval.md) | [adaptive-rag](../sources/adaptive-rag.md)、[papelo-fever2024](../sources/papelo-fever2024.md)、[adagate](../sources/adagate.md) |
| 稠密檢索（dense） | 用 embedding 算 cosine 相似度 | [adaptive-k](../sources/adaptive-k.md)、[adagate](../sources/adagate.md) |
| 網路搜尋 | 直接用 Google 搜尋開放網路 | [papelo-fever2024](../sources/papelo-fever2024.md) |

## 核心難題
1. **找得齊嗎？**（召回）— 多跳時後面幾跳難找。[hover](../sources/hover.md)
2. **要放幾篇？**（數量）— [adaptive-k](../sources/adaptive-k.md) 用相似度落差；[adagate](../sources/adagate.md) 用效用落差＋token 預算
3. **要不要查、查幾輪？**（迭代）— 依問題難度決定，見 [adaptive-rag](../sources/adaptive-rag.md)、[adaptive-retrieval](../concepts/adaptive-retrieval.md)

4. **放進去的對不對、重不重複？**（品質）— 精確率與召回率常互相拉扯：[adagate](../sources/adagate.md) 實驗中 Adaptive-k 召回 .820、精確率只有 .278

## 相關概念
[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)、[fact-verification](../concepts/fact-verification.md)、[adaptive-retrieval](../concepts/adaptive-retrieval.md)、[iterative-retrieval](../concepts/iterative-retrieval.md)
