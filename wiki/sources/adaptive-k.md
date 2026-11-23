---
type: source
paper: Adaptive-k
year: 2025
tags: [RAG, context-selection, long-context]
---
# Adaptive-k：依相似度落差決定要放幾篇

## 1. 基本資料
- **標題**：Efficient Context Selection for Long-Context QA: No Tuning, No Iteration, Just Adaptive-k
- **作者**：Chihiro Taguchi（Notre Dame）、Seiji Maekawa、Nikita Bhutani（Megagon Labs）
- **年份／出處**：2025，EMNLP 2025，pp. 20105–20130
- **論文類型**：方法論文

## 2. 背景：要做什麼
RAG 和長上下文模型（LCLM）都要面對同一個問題：**要放多少外部內容進去？** 這篇提出一個方法，針對每個問題自動決定要檢索幾篇（k）。

## 3. 動機：為什麼要做
- 固定 top-k 不是放太少（漏掉證據），就是放太多（浪費 token、干擾模型、變慢）。[p.1]
- 既有的適應式方法（Self-RAG、SELF-ROUTE 等）需要反覆呼叫 LLM，或需要 LLM 內部存取權／微調，不適合 API 型的閉源模型。[p.1, 表1]
- **彙整型問題（aggregation QA）**，例如「加州有哪些學生超過一萬人的大學？」，需要的證據量差異很大，固定 k 特別不適合。[§2]

## 4. 欲解決的問題
**不用監督訓練、不用迭代呼叫 LLM**，怎麼估計每個問題最適合的檢索數量？[p.2]

## 5. 研究方法：怎麼做 [§3, 演算法1]
1. 計算問題和每個段落的 cosine 相似度。
2. 分數由高到低排序，算相鄰兩個分數的差距。
3. 找**差距最大的位置** → 前面的就是 k 篇。
4. 實務調整：多拿 **B = 5** 篇當緩衝，避免切點後面剛好有相關段落；只在前 90% 的段落裡找最大落差，避免在尾端找到落差而整批收下。
- 時間複雜度 O(n log n)，只需一次矩陣計算，可以直接插進既有的檢索器－讀取器流程。

## 6. 核心理論／概念：用來處理什麼
| 概念 | 處理什麼問題 |
|---|---|
| **相似度分布的最大落差** | 假設最大落差就是「相關／不相關」的分界，用來決定 k |
| [適應式檢索](../concepts/adaptive-retrieval.md)的「數量」維度 | 每個問題需要的證據量不同 |
| **Plug-and-play／single pass** | 不改 LLM、不迭代，相容閉源 API 模型 |

## 7. 實驗設計 [§4]
- **事實型 QA**：HotpotQA、NQ、TriviaQA（HELMET 長上下文版本，128k tokens），各取 100 題
- **彙整型 QA**：HoloBench（90 題，總上下文固定 100k tokens，相關資訊量 5k / 10k / 25k / 50k tokens）
- **Embedding**：Contriever（109M）、BGE-large（335M）、GTE-Qwen2（1.78B）
- **Reader LLM**：GPT-4o-mini、GPT-4o、Gemini-2.5-Flash、Llama4-Scout、Llama4-Maverick
- **比較對象**：zero-shot（不給上下文）、全文、SELF-ROUTE（先給 5k tokens，答不出來再給全文）、固定 n tokens（1k～50k，最好的當 oracle）
- **指標**：context recall、SubEM（事實型）、LLM-as-a-judge（彙整型）、輸入 token 數

## 8. 主要結果
- **事實型 QA**：比全文少用 **99%** 輸入 token，比 SELF-ROUTE 少 90%，品質比 zero-shot 好。[§5.2]
- **彙整型 QA**：context recall 大約都在 **70%**，比 SELF-ROUTE 高三倍以上；相關資訊量越多，Adaptive-k 會自動拿越多。[§5.1, 表2]
  - 例：info 25k 時，SELF-ROUTE 29.67 vs Adaptive-k 68.67（Contriever）。[表3]
- **事實型 QA 的召回率反而比 SELF-ROUTE 低**：HotpotQA（BGE）70.83 vs 90.83。[表3]
- **embedding 影響很大**：事實型 QA 用 BGE 較好，HoloBench 用 GTE 較好；作者推薦 BGE。[§5.4]
- 大模型（GPT-4o、Gemini、Maverick）收益明顯，小模型收益較小。[§5.3]

## 9. 研究缺口與限制
**作者自己指出的** [Limitations]：
- 不適用摘要任務（需要看全文）。
- 只適合自然語言，不適合 JSON 這類結構化資料。
- 錯字等表面變化會影響 embedding。
- 惡意段落可能刻意製造假的落差。

**Wiki 整理者觀察到的**：
- 只看「問題」和段落的相似度，**不處理多跳**：後面幾跳的證據跟原問題不像（見 [hover](../sources/hover.md)），可能落在切點之後。
- 不處理重複內容：相似的段落會一起被收下。[adagate](../sources/adagate.md) 的實驗中，它平均放 8.6 篇，精確率只有 0.278。

> ⚠️ 跨論文描述衝突：本篇 §2 描述 Adaptive-RAG「iteratively asks an LLM whether it can answer」，但 [adaptive-rag](../sources/adaptive-rag.md) 原文是用 T5 分類器**事先**判斷難度（A/B/C），不是反覆詢問 LLM。本 Wiki 以 Adaptive-RAG 原文為準。

## 10. 與其他論文的關係
- [adaptive-rag](../sources/adaptive-rag.md)：決定「查幾輪」；Adaptive-k 決定「每次放幾篇」，兩者可以互補。
- [adagate](../sources/adagate.md)：AdaGATE 借用「最大落差」的想法，但改成看**效用分數**的落差，而不是相似度；並把 Adaptive-k 當比較對象。
- [hover](../sources/hover.md)：HoVer 顯示前 5 篇和前 100 篇的召回差很多，正是「k 該取多少」的問題。
- 概念：[adaptive-retrieval](../concepts/adaptive-retrieval.md)、[evidence-retrieval](../concepts/evidence-retrieval.md)

## 11. 一句話記住這篇
**Adaptive-k 找相似度分數裡落差最大的地方當切點，不用訓練、只檢索一次，就能大幅減少 token；但只看和問題像不像，處理不了多跳和重複。**
