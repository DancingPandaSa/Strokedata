# 🧠 腦中風資料分析專案

本專案的目標是透過 **公開資料集 + 臨床模擬資料庫**，進行 **腦中風風險預測** 與 **台灣腦血管疾病死亡趨勢驗證**。  
專案涵蓋了 **數據管線 (Data Pipeline)**、**資料建模 (Data Modeling)**、**商業智慧 (Power BI)**、以及 **機器學習預測模型 (Machine Learning)**。

---

## 📊 專案架構

### 1. 資料管線 (Data Pipeline)
- **資料來源**：MySQL (模擬醫療資料庫，表名 `strokedata`)
- **ETL 工具**：`dbt` 進行資料清洗與轉換  
- **流程設計**：`staging → intermediate → mart`
- **資料倉儲**：模擬 Snowflake / BigQuery / Postgres

### 2. 資料建模 (Data Modeling)
- 採用 **星型模型 (Star Schema)**
- **事實表 (Fact Table)**：`fact_stroke`（紀錄個體是否中風）
- **維度表 (Dimension Tables)**：
  - `dim_patient`（性別、年齡、婚姻、居住地）
  - `dim_health`（高血壓、心臟病、BMI、血糖）
  - `dim_lifestyle`（職業型態、居住類型、吸菸狀態）

### 3. 商業智慧 (Power BI)
- 製作中風案例的視覺化分析
- 包含 **性別、年齡、吸菸、BMI、疾病共病** 的影響
- 👉 [查看 Power BI 報表](https://app.powerbi.com/view?r=eyJrIjoiYTE5NDgzMTYtMmRhZi00ZjhmLWFkYjktZjIwZTY4NzJkOTFhIiwidCI6ImM3ODIzYzk2LWFmNDgtNGJlNC05YmUxLWFhN2I2MDEyMTk5NyIsImMiOjZ9)

### 4. 機器學習 (Machine Learning)
- **方法比較**：
  - Logistic Regression（邏輯迴歸）
  - Random Forest（隨機森林）
- **流程設計**：  
  `資料探索 → 預處理 → 建模 → 評估 → 模型選擇 → 模型解釋 → 外部驗證`
- **輸出 Demo**：  
  - GitHub Pages → [中風風險預測 Demo](https://dancingpandasa.github.io/Strokedata/)  
  - 使用者可輸入 **年齡、性別、BMI、血糖等個人資訊**，系統會計算 **中風風險機率**，並提供與 **台灣腦血管疾病死亡率 (MOHW)** 的趨勢比較。

---

## 📂 資料來源

1. [Kaggle – Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset?resource=download)  
   國際公開腦中風資料集，包含患者基本屬性與中風標籤。

2. [衛生福利部 111 年國人死因統計 – 腦血管疾病死亡資料](https://dep.mohw.gov.tw/DOS/lp-5069-113-2-20.html)  
   台灣官方公共衛生資料，用於模型驗證與趨勢比對。

3. [Power BI 視覺化報表](https://app.powerbi.com/view?r=eyJrIjoiYTE5NDgzMTYtMmRhZi00ZjhmLWFkYjktZjIwZTY4NzJkOTFhIiwidCI6ImM3ODIzYzk2LWFmNDgtNGJlNC05YmUxLWFhN2I2MDEyMTk5NyIsImMiOjZ9)  
   探索資料特徵、群組差異、風險因子。

4. [機器學習預測 Demo – GitHub Pages](https://dancingpandasa.github.io/Strokedata/)  
   使用者輸入個人資訊（年齡、性別、身高、體重、血糖…），即可預測中風機率。

---

## 🚀 專案亮點

- ✅ 整合 **國際資料集 + 台灣官方統計**  
- ✅ 建立 **資料管線 & 星型模型**  
- ✅ 使用 **Power BI** 製作可視化儀表板  
- ✅ 應用 **機器學習模型** 預測中風風險  
- ✅ 與 **台灣腦血管疾病死亡率** 進行外部驗證  

---

## 📎 專案展示

- Power BI 分析報表 → [點此查看](https://app.powerbi.com/view?r=eyJrIjoiYTE5NDgzMTYtMmRhZi00ZjhmLWFkYjktZjIwZTY4NzJkOTFhIiwidCI6ImM3ODIzYzk2LWFmNDgtNGJlNC05YmUxLWFhN2I2MDEyMTk5NyIsImMiOjZ9)  
- 機器學習預測 Demo (GitHub Pages) → [點此進入](https://dancingpandasa.github.io/Strokedata/)

---


