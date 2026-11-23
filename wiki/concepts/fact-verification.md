---
type: concept
tags: [fact-verification]
---
# 事實查核（Fact Verification / Claim Verification）

## 定義
給一句**說法（claim）**，系統要找證據，並判斷說法是否被證據支持。

## 標籤設計比較
| 資料集／任務 | 標籤 |
|---|---|
| FEVER (2018) | SUPPORTED / REFUTED / NOT ENOUGH INFO |
| [hover](../sources/hover.md) (2020) | SUPPORTED / NOT-SUPPORTED（把後兩類合併，因為多跳時人也分不清楚） |
| FEVER 2024 AVeriTeC（[papelo-fever2024](../sources/papelo-fever2024.md)） | Supported / Refuted / Not Enough Evidence / Conflicting；但 Papelo 後兩類 F1 = 0，最後只做二分類 |

## 典型流程
說法 → [找證據](../concepts/evidence-retrieval.md) → 判斷（通常是自然語言推論 NLI 模型）

## 關鍵發現
- 判斷模型拿到完整證據時表現不錯（HoVer：81.2%），只看說法也有 63.7%，所以**證據找不找得齊**才是瓶頸。[hover](../sources/hover.md)

- 開放網路上，證據會以問答對提交，LLM 也可能偷用自己的知識，可追溯性是新問題。[papelo-fever2024](../sources/papelo-fever2024.md)
- 兩篇查核論文都把「不被支持」的細分類簡化掉，**區分「被推翻」與「證據不足」仍是缺口**。[hover](../sources/hover.md)、[papelo-fever2024](../sources/papelo-fever2024.md)

## 相關概念
[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)、[evidence-retrieval](../concepts/evidence-retrieval.md)
