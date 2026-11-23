---
type: source
paper: Adaptive-RAG
year: 2024
tags: [RAG, adaptive-retrieval, query-complexity]
---
# Adaptive-RAG：依問題難度調整檢索策略

## 1. 基本資料
- **標題**：Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity
- **作者**：Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, Jong C. Park（KAIST）
- **年份／出處**：2024，NAACL 2024（Long Papers），pp. 7036–7050
- **論文類型**：方法論文（提出新框架）

## 2. 背景：要做什麼
檢索增強的 LLM（retrieval-augmented LLM）回答問題有三種策略 [§3.1]：
| 策略 | 寫法 | 特性 |
|---|---|---|
| 不檢索（No Retrieval） | ā = LLM(q) | 最快，但 LLM 不知道的事就答不出來 |
| 單步（Single-step） | ā = LLM(q, d) | 先檢索一次再回答 |
| 多步（Multi-step） | āᵢ = LLM(q, dᵢ, cᵢ) | 檢索、推理重複好幾輪，cᵢ 是前幾輪的文件和中間答案；最強但最貴 |

這篇要做一個**能依每個問題自動挑策略**的問答框架。

## 3. 動機：為什麼要做
- 真實世界的問題難度不一：多數是簡單問題（如「巴黎是哪國首都？」），偶爾才有複雜的多跳問題。[p.2]
- 每題都多步 → 簡單題浪費運算；每題都單步或不檢索 → 複雜題答不好。[圖2]
- 既有的「適應式檢索」不夠好：
  - 依實體出現頻率決定要不要檢索（Mallen et al., 2023）→ 只有「要／不要」兩種，**沒考慮多跳**。
  - 依模型輸出決定何時停止（Trivedi et al., 2023）→ 太複雜，要跑好幾輪才停。[p.2]

## 4. 欲解決的問題
**能不能在回答之前，先判斷問題有多難，再選最適合的策略**，同時兼顧準確率與效率？

## 5. 研究方法：怎麼做 [§3.2]
1. **難度分類器（Query Complexity Classifier）**：用較小的語言模型（T5-Large，770M）把問題分三類：
   - **A**：簡單，LLM 自己答 → 不檢索
   - **B**：中等 → 單步檢索
   - **C**：複雜 → 多步檢索
2. **自動產生訓練標籤（不需人工）**，分兩步：
   - **Silver data（依模型結果）**：三種策略都跑一遍，**最簡單就答對的策略**當標籤（同時答對時，簡單的優先）。
   - **Inductive bias（依資料集特性）**：三種都答錯的題目沒有標籤，就看它來自哪裡——單跳資料集標 B，多跳資料集標 C。
3. 用 cross-entropy loss 訓練分類器；推論時 o = Classifier(q)，再交給對應策略。
4. 三種策略共用同一個 LLM 和檢索器，切換時**不用改模型參數**。

## 6. 核心理論／概念：用來處理什麼
| 概念 | 處理什麼問題 |
|---|---|
| [適應式檢索](../concepts/adaptive-retrieval.md) | 不是每題都需要一樣多的檢索 → 依問題決定 |
| **問題難度（query complexity）** | 把「要不要檢索、檢索幾輪」轉成一個三分類問題 |
| **自動標註（silver label + dataset bias）** | 沒有現成的難度標註資料 → 用模型答對與否和資料集來源代替人工 |
| [多步／迭代檢索](../concepts/iterative-retrieval.md) | 複雜的 [多跳](../concepts/multi-hop-reasoning.md)問題需要邊推理邊檢索 |

## 7. 實驗設計 [§4]
- **資料集**：混合單跳與多跳，模擬真實情境
  - 單跳：SQuAD v1.1、Natural Questions、TriviaQA
  - 多跳：MuSiQue、HotpotQA、2WikiMultiHopQA
  - 每個資料集取 500 題測試
- **檢索器**：BM25（字詞式稀疏檢索），所有方法共用
- **生成 LLM**：FLAN-T5-XL (3B)、FLAN-T5-XXL (11B)、GPT-3.5（gpt-3.5-turbo-instruct）
- **比較對象**：
  - Simple：不檢索、單步
  - Adaptive：Adaptive Retrieval（Mallen et al.）、Self-RAG、Adaptive-RAG
  - Complex：多步（IRCoT 類，Trivedi et al. 2023）
  - Oracle：Adaptive-RAG + 完美分類器（上限）
- **指標**：
  - 效果：EM（完全相同）、F1（字詞重疊）、Accuracy（答案包含正解）
  - 效率：Step（檢索＋生成的次數）、Time（相對於單步的時間）

## 8. 主要結果（本 Wiki 以 GPT-3.5 為主）
**表 1（6 個資料集平均，GPT-3.5）**

| 方法 | EM | F1 | Acc | Step | 相對時間 |
|---|---|---|---|---|---|
| 不檢索 | 35.77 | 48.56 | 44.27 | 0.00 | 0.71 |
| 單步 | 34.73 | 46.99 | 45.27 | 1.00 | 1.00 |
| Adaptive Retrieval | 35.90 | 48.20 | 45.30 | 0.50 | 0.86 |
| Self-RAG* | 10.87 | 22.98 | 34.13 | 0.74 | 1.50 |
| **Adaptive-RAG** | **37.97** | **50.91** | **48.97** | 1.03 | 1.46 |
| 多步 | 38.13 | 50.87 | 49.70 | 2.81 | 3.33 |
| Adaptive-RAG + 完美分類器 | 47.70 | 62.80 | 58.57 | 0.50 | 1.03 |

*Self-RAG 用的是 LLaMA2，不是 GPT-3.5，不能直接比。[表1說明]

**重點解讀**
- Adaptive-RAG 的 F1（50.91）和多步（50.87）差不多，但時間只要 1.46 vs 3.33，**不到一半**。
- 如果分類器完美，F1 可到 62.80，時間只要 1.03 → 分類器是關鍵。

**分類器分析（FLAN-T5-XL 實驗）**[表3、表4、圖3]
- 分類器整體準確率 **54.52%**；A（不用檢索）只認對 **30.52%**，B 66.28%，C 65.45%。[表4]
- 混淆矩陣：A 常被誤判成 B（約 47%）；C 約 31% 被誤判成 B。[圖3]
- 各類實際耗時：A 0.35 秒、B 3.08 秒、C 27.18 秒；分類器預測比例 A 8.60%、B 53.33%、C 38.07%。[表3]
- 拿掉任一種標註方式都會變差：只用 dataset bias → 不會判斷「不用檢索」；只用 silver data → 分類準確率高（60.30%）但 QA F1 變低。[表4]
- 分類器大小影響不大：60M、223M、770M 的 F1 分別 45.83、45.97、46.94。[表6]

## 9. 研究缺口與限制
**作者自己指出的** [Limitations]：
- 沒有現成的「問題難度」標註資料集，自動標註可能標錯。
- 現在分類器和完美分類器之間差距很大，分類器架構還能改進。
- 只分 3 個難度等級，更細的分級留給未來。[註2]

**Wiki 整理者觀察到的**：
- 難度在**一開始就決定**，回答過程中不會再調整；如果一開始判錯（例如 C 判成 B），就沒有補救機會。
- 決定的是「檢索幾輪」，但沒處理「每輪放幾篇文件」→ 這是 [adaptive-k](../sources/adaptive-k.md) 處理的問題。
- 檢索器只用 BM25，沒測試較強的稠密檢索器。

## 10. 與其他論文的關係
- [hover](../sources/hover.md)：證明多跳比單跳難；Adaptive-RAG 則承認題目有難有易，依難度分配資源。
- [adaptive-k](../sources/adaptive-k.md)：Adaptive-RAG 決定「查幾輪」，Adaptive-k 決定「每次放幾篇」；Adaptive-k 的摘要也指出 Self-RAG 這類適應式方法需要反覆呼叫 LLM。
- [papelo-fever2024](../sources/papelo-fever2024.md)：Papelo 在查核時一直追問到證據夠為止，是「多步」策略的實際應用。
- [adagate](../sources/adagate.md)：AdaGATE 把 Self-RAG、Adaptive-k 當實驗比較對象，並把 Adaptive-RAG 歸類為「決定何時檢索」的方法；它處理的是多步之後「證據怎麼組合」。
- 概念：[adaptive-retrieval](../concepts/adaptive-retrieval.md)、[iterative-retrieval](../concepts/iterative-retrieval.md)、[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)、[evidence-retrieval](../concepts/evidence-retrieval.md)

## 11. 一句話記住這篇
**Adaptive-RAG 先用小模型判斷問題難度，再決定不檢索、檢索一次或多步檢索，用不到一半的時間達到接近多步的效果；但分類器準確率只有 54.52%，是最大的改進空間。**
