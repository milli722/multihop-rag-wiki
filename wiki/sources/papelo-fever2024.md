---
type: source
paper: Papelo (FEVER 2024)
year: 2024
tags: [fact-verification, iterative-retrieval, web-search, LLM]
---
# Papelo @ FEVER 2024：多跳證據追問（Multi-hop Evidence Pursuit）

## 1. 基本資料
- **標題**：Multi-hop Evidence Pursuit Meets the Web: Team Papelo at FEVER 2024
- **作者**：Christopher Malon（NEC Laboratories America）
- **年份／出處**：2024，Proceedings of the Seventh FEVER Workshop，pp. 27–36
- **論文類型**：競賽系統論文（shared task system paper），參加 FEVER 2024（AVeriTeC）

## 2. 背景：要做什麼
FEVER 2024 的 AVeriTeC 任務：查核**真實網路上的說法**，分成四類（Supported / Refuted / Not Enough Evidence / Conflicting Evidence/Cherrypicking），而且必須提交**問答對（QA pairs）形式的證據**，每個答案要附網址。標籤正確**且**證據足夠才給分。[p.1]

## 3. 動機：為什麼要做
- 從 Wikipedia 走到**開放網路**，檢索難度大增；訓練資料只有 3,068 則，難以自己訓練檢索器 → 改用 Google 搜尋與 GPT-4o。[p.1–2]
- 官方知識庫的網頁擷取常失敗：dev set 500 則中有 297 則的正解文件抽出來是空的。[p.2]
- 過去多跳查核系統（如 FEVEROUS 的參賽者）大多**看完說法就一次把證據找完**，沒處理「初次檢索漏掉的證據」。[§2]

## 4. 欲解決的問題
**下一個要查的問題，應該在看過前面的證據之後才決定**，而不是一開始就把所有問題列好。怎麼結合 LLM 和搜尋引擎做到這件事？

## 5. 研究方法：怎麼做 [§3, 演算法1、2]
**迭代追問迴圈（本 Wiki 重點）**
1. `GetFirstQuestion`：用微調的 **T5** 根據說法產生第一個問題。
2. `GetAnswer`：把「說法＋問題」拿去 Google 搜尋 → LLM 從前 10 筆挑一篇最好的 → 抓全文，對齊搜尋摘要附近的 **5 句**當上下文 → LLM 回答。搜尋沒結果時，改用專有名詞重搜。
3. `GetNextQuestion`：用 **GPT-4o** 讀「說法＋目前所有問答」，問出**還缺的證據**；如果已經能判斷真假，就輸出 True / False **提前停止**。
4. 最多 5 個問題；如果提前停了，就用 LLM **改寫既有問題**、重新找答案，補到 5 組。
5. `LLMVerdict`：最後**重新看整條問答鏈**下判斷，可以推翻提前停止時的判斷。

**為什麼第一題用 T5、後續用 GPT-4o**：正解的第一題通常只是把說法換句話說，T5 學得好；GPT-4o 反而會問得太複雜。後續問題需要根據答案做較深的推理，T5 做不到。[§4.1]

## 6. 核心理論／概念：用來處理什麼
| 概念 | 處理什麼問題 |
|---|---|
| [迭代檢索](../concepts/iterative-retrieval.md)／**證據追問（evidence pursuit）** | 多跳證據無法只靠說法事先預測，要邊找邊問 |
| **依缺口產生問題** | 每個新問題都針對「還缺什麼」，避免問無關問題 |
| **提前停止** | 證據夠了就停，省成本 |
| **重新考慮（reconsideration）** | 最後看完整證據鏈再判斷，修正提早下的結論 |
| **Metadata（標題、網站、日期）** | 幫 LLM 判斷來源可信度 |

## 7. 實驗設計 [§4]
- **LLM**：GPT-4o（gpt-4o-2024-05-13）；**seq2seq**：T5-large；**搜尋**：Google
- **消融實驗**：只用 dev set 前 200 題（為了省錢、加快開發）
- **指標**：各類 F1、Accuracy、**AVeriTeC score**（標籤正確且證據問答與正解問答的 METEOR 平均超過 0.25 才算）

## 8. 主要結果
**消融實驗（dev 前 200 題）**[表2]

| 系統 | Acc | AVeriTeC |
|---|---|---|
| **演算法 1（完整）** | .750 | .495 |
| AllAtOnce（一次產生所有問題） | .705 | .340 |
| LLM+LLM（第一題也用 GPT-4o） | .720 | .385 |
| Seq+Seq（後續也用 T5） | .715 | .370 |
| No late verdict（不重新考慮） | .705 | .450 |
| No paraphrase（不改寫補題） | .745 | .225 |
| 4 class（四分類） | .415 | .245 |

- 迭代追問比一次產生全部問題：Acc **+.045**、AVeriTeC **+.155**。[摘要, 表2]
- 改寫補題對 Acc 影響很小，但 AVeriTeC 掉到一半以下（.225），因為證據問答對變少。[§4.4]
- **最終成績**：dev AVeriTeC .510、test **.477**（把 5 組問答複製到 10 組後）。[表3]

## 9. 研究缺口與限制
**作者自己指出的** [Limitations]：
- **Not Enough Evidence 和 Conflicting 兩類完全預測不出來**（F1 = 0），所以最後只做二分類；整體準確率只有 .754，人不該不看理由就相信系統。
- LLM 只看網站名稱，難以判斷網站整體可信度；在網路上被多方轉傳的錯誤資訊可能騙過系統。
- 無法保證 LLM 沒偷用自己的知識：搜尋有限制日期，但 GPT-4o 的訓練資料晚於說法日期。
- 首次報導的新事件（網路上還沒有證據）無法查核。

**Wiki 整理者觀察到的**：
- 每輪只取**一篇**最佳文件的 5 句，若那篇是錯的，下一個問題會被帶偏。
- 證據是問答對，不是句子，和 [hover](../sources/hover.md) 的句子級證據形式不同。
- 改寫補題主要是為了 AVeriTeC 分數（評分機制鼓勵多交問答對），不一定代表查核品質更好。

## 10. 與其他論文的關係
- [hover](../sources/hover.md)：HoVer 證明多跳檢索是瓶頸；Papelo 用迭代追問實際解決，並把場景從 Wikipedia 擴大到開放網路。兩篇都把標籤簡化成二分類，原因都是「不被支持」的細分類太難。
- [adaptive-rag](../sources/adaptive-rag.md)：Adaptive-RAG 的「多步策略」在這篇以查核任務的形式出現；Papelo 的提前停止，類似在迴圈中動態決定步數。
- [adagate](../sources/adagate.md)：兩者都「針對缺口產生新查詢」——Papelo 用自然語言問題，AdaGATE 用帳本中的缺口產生微查詢。
- 概念：[iterative-retrieval](../concepts/iterative-retrieval.md)、[fact-verification](../concepts/fact-verification.md)、[multi-hop-reasoning](../concepts/multi-hop-reasoning.md)

## 11. 一句話記住這篇
**Papelo 讓 LLM 每找到一個答案，就追問「還缺什麼」，證據夠了才停，最後再看整條證據鏈下判斷；比一次列完所有問題更準、證據更完整。**
