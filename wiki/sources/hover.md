---
type: source
paper: HoVer
year: 2020
tags: [dataset, fact-verification, multi-hop]
---
# HoVer：多跳事實抽取與說法查核資料集

## 1. 基本資料
- **標題**：HoVer: A Dataset for Many-Hop Fact Extraction And Claim Verification
- **作者**：Yichen Jiang, Shikha Bordia, Zheng Zhong, Charles Dognin, Maneesh Singh, Mohit Bansal（UNC Chapel Hill、Verisk Analytics）
- **年份／出處**：2020，Findings of EMNLP 2020（arXiv:2011.03088）
- **論文類型**：資料集論文（dataset paper），主要貢獻是一份新資料集與基準結果，不是新模型。

## 2. 背景：要做什麼
做一份**事實查核（fact verification）**資料集：給一句說法（claim），系統要
1. 從多篇 Wikipedia 文章中**找出相關證據**（fact extraction），
2. 判斷這個說法是 **SUPPORTED（被支持）** 還是 **NOT-SUPPORTED（不被支持）**。

HoVer 的說法最多需要串起 **4 篇** Wikipedia 文章才能查證，這就是 [多跳推理](../concepts/multi-hop-reasoning.md)。

## 3. 動機：為什麼要做
- 社群媒體讓不實訊息變多，需要能「自動找證據、再查證」的系統。[p.1]
- 既有的 FEVER 資料集有 **87% 以上**的說法只需要**一篇** Wikipedia 文章，太接近單跳。[p.1]
- 多跳問答資料集（HotpotQA、QAngaroo）最多 2～3 篇文件，而且研究發現**單跳模型也能拿到好成績**，代表題目可以靠字詞比對走捷徑（reasoning shortcut）。[p.1]

## 4. 欲解決的問題
現有資料集無法真正測出「多跳」能力。作者認為理想的多跳題目應該有**至少一篇證據，光用說法本身做語意比對是找不到的**，必須先找到前一篇文件，才能從中得到線索去找下一篇。[p.1]

## 5. 研究方法：怎麼做（資料建構三階段）[p.2–3, 圖1]
1. **說法建立（Claim Creation）**
   - 請標註員把 HotpotQA 的問答對改寫成 **2-hop 說法**。
   - **擴充跳數**：把說法中的某個實體，換成「描述該實體的另一篇 Wikipedia 文章資訊」→ 變成 3-hop；再做一次 → 4-hop。
   - 3/4-hop 說法鼓勵寫成多句，用代名詞串接（共指，coreference）。
   - 例：「Patrick Carpentier 開 Ford Fusion」→ 把人名換成「1997 年 CART 賽季年度新秀」，必須多查一篇才知道是誰。[表1]
2. **說法改寫（Claim Mutation）**：用人工改寫（變得更具體／更籠統／否定）加上自動換字換實體，產生不被支持的說法。
3. **標註（Claim Labeling）**：原本分三類 SUPPORTED / REFUTED / NOT ENOUGH INFO，但多跳情境下 REFUTED 和 NOT ENOUGH INFO 連受訓標註員都分不清楚，所以**合併成 NOT-SUPPORTED，變成二元分類**。[p.2]
   - 只保留至少 3 位標註員意見一致的說法，Fleiss kappa = 0.63。[p.3]

## 6. 核心理論／概念：用來處理什麼
| 概念 | 處理什麼問題 |
|---|---|
| [多跳推理](../concepts/multi-hop-reasoning.md)與**推理圖（reasoning graph）** | 每個節點是一篇證據文件，邊是超連結或比較關係；4-hop 有 3 種不同形狀的圖，用來確保推理結構多樣 [表1] |
| **降低語意重疊** | 讓說法和部分證據文件字面上不像，堵住「字詞比對」的捷徑 |
| [事實查核](../concepts/fact-verification.md)的**流水線（pipeline）** | 文件檢索 → 句子挑選 → 說法判斷，見 [證據檢索](../concepts/evidence-retrieval.md) |
| **HoVer Score** | 只有「每篇證據文件都至少找到一句證據」**且**「標籤判斷正確」才算對，同時評估檢索和判斷 |

## 7. 實驗設計
- **資料規模**：共 26,171 則說法；train 18,171、dev 4,000、test 4,000。[表2]
- **說法長度**：2/3/4-hop 平均 19.0 / 24.2 / 31.6 tokens，FEVER 平均只有 9.4。[p.4]
- **基準系統（baseline）**：仿照 FEVER 的頂尖系統（Nie et al., 2019a）
  1. 規則式文件檢索：bi-gram TF-IDF
  2. 神經文件檢索：BERT-base 重新排序 TF-IDF 前 20 篇
  3. 神經句子挑選：BERT-base 從前 5 篇文件中挑句子
  4. 說法判斷：BERT-base 做自然語言推論（NLI）二元分類
- **指標**：文件／句子檢索用 EM 與 F1；判斷用 Accuracy；整體用 HoVer Score。
- **人類表現**：抽 100 則說法請人做。

## 8. 主要結果
**(1) 跳數越多，檢索越難** — TF-IDF 取前 100 篇時，能找齊所有證據文件的比例 [表3]：

| Hit@100 | 2-hop | 3-hop | 4-hop |
|---|---|---|---|
| TF-IDF | 80.02% | 39.18% | 15.59% |

只取前 5 篇時，4-hop 只剩 0.38%。[表3]

**(2) 神經文件檢索也一樣下降** — BERT 文件檢索 EM：2-hop 30.1、3-hop 5.6、4-hop 0.6；人類分別是 85.0 / 82.4 / 65.8。[表4]

**(3) 判斷本身不是最大瓶頸** [p.5, 表6]
- 給完整證據（oracle）：判斷準確率 **81.2%**
- 完全不給證據（只看說法）：**63.7%** → 說法本身有一點偏誤可利用，但比有證據低 17.5 個百分點

**(4) 整條流程** [表7、表8]
- 最佳流程在 dev set 的 HoVer Score 只有 **14.9%**，test set **15.32%**；人類 HoVer Score **81%**、準確率 88%。
- test set 上 Evidence F1 = 49.5。

> ⚠️ 原文矛盾：表 7 中「BERT+GOLD」列為 67.6% 準確率／14.9 分、「BERT+RETR」列為 73.7%／14.5 分，但內文說「最佳 BERT 模型 67.6% 準確率、14.9% HoVer Score」，引言又寫判斷模型「只達到 73.7%」。兩列標籤疑似對調或敘述不一致。本 Wiki 以**內文說法（最佳 HoVer Score 14.9%）**為準，簡報不引用 67.6/73.7 這組有爭議的數字。

## 9. 研究缺口與限制
**作者自己指出的：**
- 瓶頸在**檢索**：模型拿到完整證據時判斷得還不錯，但多跳情境下證據找不齊。需要「能做多跳推理的檢索方法」。[p.2]
- 3/4-hop 標註成本、時間、品質控管都急遽上升，第一版只用了 12k 個 HotpotQA 例子。[p.4]

**Wiki 整理者觀察到的：**
- REFUTED 和 NOT ENOUGH INFO 合併後，系統無法區分「被推翻」和「證據不足」，跟真實查核情境（例如 [FEVER 2024](../sources/papelo-fever2024.md) 有四類標籤）有落差。
- 資料只來自英文 Wikipedia，不是開放網路。
- baseline 是 2019 年的 BERT 流水線，**一次檢索到底**，沒有迭代檢索。

## 10. 與其他論文的關係
- [papelo-fever2024](../sources/papelo-fever2024.md)：把「證據要一跳一跳追」做成迭代提問；而且從 Wikipedia 走到開放網路。
- [adaptive-rag](../sources/adaptive-rag.md)：HoVer 證明多跳題比單跳難，Adaptive-RAG 則是先判斷題目難度，再決定檢索策略。
- [adaptive-k](../sources/adaptive-k.md)、[adagate](../sources/adagate.md)：HoVer 顯示「檢索幾篇」很關鍵（前 5 vs 前 100 差很多），這兩篇處理「放幾篇、放哪幾篇」。
- 概念：[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)、[fact-verification](../concepts/fact-verification.md)、[evidence-retrieval](../concepts/evidence-retrieval.md)

## 11. 一句話記住這篇
**HoVer 用「替換實體來增加跳數」造出最多 4-hop 的查核題，證明跳數越多、證據越難找齊，而瓶頸在檢索，不在判斷。**
