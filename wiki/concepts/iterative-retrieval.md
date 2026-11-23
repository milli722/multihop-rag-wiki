---
type: concept
tags: [RAG, multi-step]
---
# 迭代／多步檢索（Iterative / Multi-step Retrieval）

## 定義
檢索和推理交替進行：每一輪用「原問題＋目前找到的東西」再去檢索，直到能回答為止。
Adaptive-RAG 的寫法：dᵢ = Retriever(q, cᵢ)，āᵢ = LLM(q, dᵢ, cᵢ)，cᵢ 是前幾輪的文件與中間答案。[adaptive-rag](../sources/adaptive-rag.md)

## 為什麼多跳需要它
多跳問題後面幾跳的證據，常常要靠前一跳的答案才找得到（例如先知道「年度新秀是誰」，才能查他開什麼車）。[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)

## 代價
- 每多一輪就多一次 LLM 和檢索器呼叫。Adaptive-RAG 實驗中，多步策略平均 2.81 步、時間是單步的 3.33 倍（GPT-3.5）。[adaptive-rag](../sources/adaptive-rag.md)
- 上下文會越來越長、混入重複段落 → [adagate](../sources/adagate.md) 改用「替換而非擴張」控制長度。

## 各論文的做法
| 論文 | 做法 |
|---|---|
| [adaptive-rag](../sources/adaptive-rag.md) | 只在分類器判為 C（複雜）時才用多步 |
| [papelo-fever2024](../sources/papelo-fever2024.md) | LLM 根據已有問答**追問還缺什麼**，夠了就提前停止；比一次列完所有問題 Acc +.045 |
| [adagate](../sources/adagate.md) | 帳本記錄已知事實與缺口，針對缺口發微查詢，再在 token 預算內替換證據 |

## 「下一步查什麼」怎麼決定
| 做法 | 例子 |
|---|---|
| 用問題難度事先決定要不要多步 | [adaptive-rag](../sources/adaptive-rag.md) |
| 用自然語言追問缺的證據 | [papelo-fever2024](../sources/papelo-fever2024.md) |
| 用結構化帳本找缺口 | [adagate](../sources/adagate.md) |
