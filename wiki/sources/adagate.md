---
type: source
paper: AdaGATE
year: 2026
tags: [RAG, multi-hop, evidence-assembly, token-budget]
credibility: low   # 課程專題預印本，未經同儕審查
---
# AdaGATE：缺口導向、省 token 的多跳證據組裝

> 🔶 **可信度註記**：本篇是 NYU 課程專題（DS-GA / LING-GA 1012）的 arXiv 預印本（2026 年 5 月），**未經同儕審查**，評估只有 200 題。引用時要保守。

## 1. 基本資料
- **標題**：AdaGATE: Adaptive Gap-Aware Token-Efficient Evidence Assembly for Multi-Hop Retrieval-Augmented Generation
- **作者**：Yilin Guo、Yinshan Wang（New York University）
- **年份／出處**：2026，arXiv:2605.05245v1
- **論文類型**：方法論文（預印本）

## 2. 背景：要做什麼
把多跳 RAG 看成**在 token 預算內組裝證據**的問題：在檢索不完美（有雜訊、有重複）的情況下，挑出一小組**互補**的段落給生成模型。

## 3. 動機：為什麼要做
- 多跳問題**漏掉一個橋接事實**就會失敗；放進重複或誤導的段落又會扭曲答案。[p.1]
- 稠密檢索常回傳一堆幾乎重複的段落，覆蓋不到整條推理鏈。[p.1]
- 既有方法各管一部分：Self-RAG 決定何時檢索、Adaptive-k 決定放幾篇、SEAL-RAG 做缺口修補，但**沒有一個同時平衡缺口修補、去重複和 token 效率**。[p.1, §2]

## 4. 欲解決的問題
怎麼在**固定 token 預算**下，同時做到：補齊缺的證據、不放重複內容、不被雜訊帶偏？

## 5. 研究方法：怎麼做 [§3, 圖1]
不需訓練的控制器（controller），架在固定的檢索器和 LLM 上，每一輪做四件事：**擷取 → 搜尋 → 評分 → 替換**。
1. **擷取（extract）**：LLM 把目前的證據整理成**實體帳本（ledger）**（實體－關係－值＋信心分數），並列出還缺的**資訊缺口（gaps）**。
2. **搜尋（search）**：針對每個缺口產生**微查詢（micro-query）**；另外加上**根據原問題的備援查詢**，防止缺口抽得不準。
3. **評分（score）**：每個候選段落的效用分數
   S = λ₁ 補缺口 + λ₂ 佐證既有事實 + λ₃ 新資訊 − λ₄ 重複 + λ₅ 與原問題相關
4. **替換（replace）**：找效用分數**落差最大**的位置決定有效容量 K_eff（＋緩衝 2 篇），在 token 預算 B 內，用高分段落**替換**低分段落（不是一直往上加）。
- 停止條件：沒有可修補的、沒有缺口了，或達到最多修補輪數 L。

## 6. 核心理論／概念：用來處理什麼
| 概念 | 處理什麼問題 |
|---|---|
| **實體帳本＋缺口追蹤** | 明確知道還缺哪個[橋接事實](../concepts/multi-hop-reasoning.md) |
| **微查詢＋問題備援** | 針對缺口去找；缺口抽錯時還有原問題當保底 |
| **效用分數（5 項）** | 同時考慮補缺口、佐證、新穎、去重複、相關性 |
| **替換而非擴張（replace, don't expand）** | 控制上下文不會越疊越長 |
| **效用落差決定容量** | 借用 [adaptive-k](../sources/adaptive-k.md) 的「最大落差」想法，但用在效用分數上 |

## 7. 實驗設計 [§4]
- **資料**：HotpotQA distractor 設定；用 1,000 題驗證集建索引（10,919 個 chunk），評估 **200 題**
- **三種情境**：乾淨（clean）、重複注入（redundancy，改寫版正解段落，ρ = 0.5）、雜訊注入（noise，打亂字詞＋其他題的段落，ρ = 0.5）
- **共用設定**：OpenAI text-embedding-3-small＋Pinecone，每次查詢取 k = 3；生成模型 gpt-4o-mini
- **比較對象**：Basic RAG、Self-RAG、[adaptive-k](../sources/adaptive-k.md)、SEAL-RAG（L = 1, 3）、AdaGATE（L = 1, 3，預算 B = 3000）
- **指標**：答題正確率（GPT-4o 評審）、證據 P / R / F1（對正解文件標題）、ARES（CR / AF / AR）、token 用量

## 8. 主要結果 [表2]
**證據 F1（AdaGATE 三種情境都最高）**

| 方法 | Clean | Redundancy | Noise |
|---|---|---|---|
| Basic RAG | .601 | .615 | .605 |
| Adaptive-k | .408 | .187 | .414 |
| SEAL-RAG (L=3) | .549 | .595 | .540 |
| **AdaGATE (L=1)** | **.623** | .709 | **.627** |
| **AdaGATE (L=3)** | .620 | **.712** | **.627** |

**但答題正確率不是最高**（Clean）：Adaptive-k 69.0%、SEAL-RAG (L=3) 68.5%、AdaGATE (L=3) 64.5%、(L=1) 63.0%。

**token 用量（Clean，平均輸入 token／平均文件數）**：Adaptive-k 1116 / 8.6、AdaGATE (L=1) 360 / 2.9、SEAL-RAG 約 136–140 / 1.0。

**其他發現**
- Adaptive-k 召回最高（.820）但精確率只有 .278，因為平均放 8.6 篇。
- SEAL-RAG 精確率最高但召回卡在約 .42：作者發現它的**實作和論文描述不一致**（實作要 LLM「選最少實體」，結果幾乎只放 1 篇）。
- 重複注入時，AdaGATE 的去重複項發揮作用，token 從 360 降到 220，F1 反而升到 .709 / .712。
- ARES 分數最高的是 Adaptive-k，因為放很多篇時「總有一篇支持答案」→ 作者指出 ARES 反映的是**有沒有上下文**，不是證據精準度。

> ⚠️ 原文數字不一致：摘要和 §5.2 都說「比 Adaptive-k 少用 **2.6×** 輸入 token」，但依表 2，Clean 為 1116 / 360 ≈ **3.1×**、Noise 為 1073 / 328 ≈ 3.3×、Redundancy 為 1592 / 220 ≈ 7.2×，沒有任何一組是 2.6×。本 Wiki 引用時改寫為「約 3 倍」並附原始數字。

## 9. 研究缺口與限制
**作者自己指出的**：
- 每次只取 k = 3，候選池小，token 預算其實沒有發揮限制作用。
- 缺口偵測太保守時會**拒答**，而 ARES 會把拒答算成不忠實。

**Wiki 整理者觀察到的**：
- 只有 200 題、只用 HotpotQA（2-hop），沒有測 3/4-hop（例如 [hover](../sources/hover.md)）。
- 擷取帳本和找缺口都靠 LLM，作者把它們當黑箱，沒評估缺口抽得準不準。
- 5 個權重 λ 怎麼設定、敏感度如何，論文沒有說明。
- 證據 F1 最高，但答題正確率不是最高 → 「證據組得好」不等於「答得好」。

## 10. 與其他論文的關係
- [adaptive-k](../sources/adaptive-k.md)：直接當比較對象；AdaGATE 把「最大落差」從相似度換成效用分數，並加上去重複。
- [papelo-fever2024](../sources/papelo-fever2024.md)：都是「依缺口產生新查詢」的迭代方法；Papelo 用自然語言追問，AdaGATE 用帳本缺口＋微查詢，並多了 token 預算與替換。
- [adaptive-rag](../sources/adaptive-rag.md)：AdaGATE 在相關研究中把它歸為「決定何時／要不要檢索」的方法，與自己的「證據組裝」區分。
- [hover](../sources/hover.md)：HoVer 說瓶頸在找齊證據；AdaGATE 是「找齊又不灌水」的一種嘗試。
- 概念：[iterative-retrieval](../concepts/iterative-retrieval.md)、[adaptive-retrieval](../concepts/adaptive-retrieval.md)、[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)

## 11. 一句話記住這篇
**AdaGATE 用帳本追蹤還缺什麼，針對缺口去查，再用效用分數在 token 預算內替換掉重複或沒用的段落；證據 F1 最好，但它只是 200 題的課程預印本。**
