# 🧠 Stroke Prediction Data Pipeline

A full-stack data pipeline project for analyzing and predicting stroke risks using real-world healthcare data.

---

## 📊 Project Overview

This project demonstrates an **end-to-end data pipeline** that includes data ingestion, transformation, modeling, quality checks, storage, and visualization using modern data tools and best practices.

- **📦 Data Source**: [Kaggle - Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)
- **🎯 Goal**: Clean and transform healthcare data to analyze and predict stroke risks
- **🧱 Architecture**: Modular pipeline using Python, MySQL, DBT, and visualization tools

---

## 🧭 System Architecture

```text
資料來源 (Kaggle Dataset)
        ↓
ETL (Python / Pandas / SQL)
        ↓
資料倉儲 (MySQL)
        ↓
數據建模 (DBT: staging / intermediate / mart)
        ↓
資料品質監控 (Python rule checks + logs)
        ↓
可視化 (Power BI / Tableau / Streamlit)
        ↓
版本控管 + 自動化 (Git + GitHub Actions)

```

---

## 🛠 Tech Stack

| Stage                   | Tool / Language           |
|-------------------------|---------------------------|
| Data Ingestion          | Python, Pandas            |
| SQL Query Engine        | DuckDB (local analysis)   |
| Data Warehouse          | MySQL                     |
| Data Modeling           | DBT                       |
| Data Quality Monitoring | Python (custom rules)     |
| Visualization           | Streamlit / Power BI      |
| CI/CD & Version Control | Git + GitHub Actions      |

---

## 📁 Project Structure

```text
stroke-prediction-pipeline/
│
├── data/                            # Raw and cleaned datasets
│   └── healthcare-dataset-stroke-data.csv
│
├── etl/                             # ETL pipeline scripts
│   └── load_data.py                 # Cleans and loads data into MySQL
│
├── dbt/                             # DBT project folder
│   └── stroke_project/              # Contains DBT models (staging, mart, etc.)
│
├── quality_checks/                 # Data validation scripts
│   └── validate_data.py            # Rule-based quality checks and logging
│
├── dashboards/                      # Visualization layer
│   ├── streamlit_app.py            # Streamlit dashboard app (optional)
│   └── powerbi_dashboard.pbix      # Power BI dashboard file (optional)
│
├── .github/                         # GitHub Actions CI/CD config
│   └── workflows/
│       └── etl_ci.yml              # Workflow for automated ETL validation
│
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```
## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/stroke-prediction-pipeline.git
cd stroke-prediction-pipeline
```
### 2. Install Python Dependencies
pip install -r requirements.txt

### 3. Load Data into MySQL

Update MySQL credentials in etl/load_data.py, then run:

python etl/load_data.py

### 4. Run DBT Models

Navigate to the DBT project directory and execute:

cd dbt/stroke_project
dbt run
dbt test

### 5. Start Streamlit Dashboard (Optional)
streamlit run dashboards/streamlit_app.py

## ✅ Key Features

### 🧼 Data Cleaning with Pandas (e.g., missing BMI values, gender filtering)

### 🏗 DBT Data Models:

stg_stroke_data

int_patient_risk

mart_stroke_summary

### 🧪 Data Validation (null checks, type checks, rule-based QA)

### 📊 Interactive Dashboards (Streamlit or Power BI)

### 🔁 CI/CD with GitHub Actions (auto-run ETL on push)

### 🔒 Version Control using Git

## 🧠 Insights

### 🔺 Age and hypertension are the strongest indicators for stroke

### 🚬 Smokers with heart disease show higher average stroke probability

### 🧮 BMI and glucose levels moderately influence stroke risk
