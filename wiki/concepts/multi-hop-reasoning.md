---
type: concept
tags: [multi-hop]
---
# 多跳推理（Multi-hop Reasoning）

## 定義
答案或查核結果需要**串起好幾份證據**才能得出，而且後面的證據常常要靠前面證據提供的線索才找得到。「跳數（hop）」＝需要的證據文件數。[hover](../sources/hover.md)

## 例子（改寫自 HoVer 表 1）
「1997 年 CART 賽季的年度新秀開的車款，是 2006 年式推出的。」
1. 第 1 跳：查 1997 CART 賽季 → 年度新秀是 Patrick Carpentier
2. 第 2 跳：查 Patrick Carpentier → 他開 Ford Fusion
3. 第 3 跳：查 Ford Fusion → 2006 年式推出 ✅

光看原句，幾乎找不到「Ford Fusion」那篇，因為字面上沒有提到。

## 為什麼難
- **字面比對失效**：後面幾跳的文件跟原句不像。HoVer 中 TF-IDF 前 100 篇能找齊證據的比例，從 2-hop 的 80% 掉到 4-hop 的 15.59%。[hover](../sources/hover.md)
- **錯一跳就全錯**：漏掉中間的「橋接事實（bridge fact）」，後面就接不下去。[adagate](../sources/adagate.md)

## 各論文的對應做法
| 論文 | 對多跳的處理 |
|---|---|
| [hover](../sources/hover.md) | 建立最多 4-hop 的資料集，證明問題存在 |
| [adaptive-rag](../sources/adaptive-rag.md) | 多跳問題判為 C，交給多步檢索 |
| [papelo-fever2024](../sources/papelo-fever2024.md) | 迭代追問，一跳一跳找證據 |
| [adagate](../sources/adagate.md) | 追蹤缺少的橋接事實，用微查詢補上 |
| [adaptive-k](../sources/adaptive-k.md) | 未直接處理多跳（只看與原問題的相似度） |

## 相關概念
[fact-verification](../concepts/fact-verification.md)、[evidence-retrieval](../concepts/evidence-retrieval.md)
