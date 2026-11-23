---
type: overview
---
# 總覽：5 篇論文怎麼串在一起

## 一條主線：多跳時「找齊證據」的三個問題
```
[問題]        多跳說法/問題，證據要好幾篇才湊得齊 ............ HoVer (2020)
   │
   ├─ Q1 要不要查？查幾輪？ ..................................... Adaptive-RAG (2024)
   ├─ Q2 每次放幾篇？ ........................................... Adaptive-k (2025)
   └─ Q3 缺的證據怎麼追？放進去的怎麼不重複、不超預算？
          ├─ 自然語言追問（查核、開放網路） ..................... Papelo @ FEVER 2024
          └─ 帳本找缺口＋效用替換（token 預算） ................. AdaGATE (2026, 預印本)
```

## 比較表
| | [hover](sources/hover.md) | [adaptive-rag](sources/adaptive-rag.md) | [adaptive-k](sources/adaptive-k.md) | [papelo-fever2024](sources/papelo-fever2024.md) | [adagate](sources/adagate.md) |
|---|---|---|---|---|---|
| 類型 | 資料集 | 方法 | 方法 | 競賽系統 | 方法（預印本） |
| 任務 | 事實查核 | 開放域問答 | 長上下文問答 | 事實查核（網路） | 多跳問答 |
| 核心想法 | 替換實體增加跳數 | 難度分類器選策略 | 相似度最大落差定 k | 依缺口迭代追問 | 帳本缺口＋效用替換 |
| 需要訓練？ | baseline 需要 | 需要（T5） | 不需要 | 第一題 T5 需要 | 不需要 |
| 迭代？ | 否 | 視難度 | 否 | 是 | 是 |
| 主要指標 | HoVer Score 14.9% | F1 50.91（GPT-3.5） | token −99%（事實型） | AVeriTeC .477（test） | 證據 F1 .623（clean） |

## 跨論文觀察
1. **檢索是瓶頸**：HoVer 給完整證據時判斷 81.2%，整體流程卻只有 14.9% 完全做對。後面 4 篇其實都在處理「怎麼找到、怎麼放進去」。
2. **效率與效果的取捨**：多步最準但最慢（Adaptive-RAG：時間 3.33 倍）；放很多篇召回高但精確率低（Adaptive-k 在 AdaGATE 實驗中精確率 .278）。
3. **「最大落差」這個想法被重複使用**：Adaptive-k 用在相似度，AdaGATE 用在效用分數。
4. **查核的標籤問題沒解決**：HoVer 和 Papelo 都把「證據不足／衝突」簡化掉。
5. **評估要小心**：AdaGATE 指出 ARES 會因為上下文多而虛高；Papelo 的改寫補題主要是為了 AVeriTeC 分數。

## 原文矛盾彙整（Lint 紀錄）
| 位置 | 問題 | Wiki 處理方式 |
|---|---|---|
| [hover](sources/hover.md) 表 7 | 兩列標籤與內文敘述不一致 | 只引用內文明確的 14.9% / 15.32% |
| [adaptive-k](sources/adaptive-k.md) §2 | 對 Adaptive-RAG 的描述與其原文不符 | 以 [adaptive-rag](sources/adaptive-rag.md) 原文為準 |
| [adagate](sources/adagate.md) 摘要 | 「2.6× 少 token」與表 2 算出的 3.1× 不符 | 改寫為「約 3 倍」並附原始數字 |
