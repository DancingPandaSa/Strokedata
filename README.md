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
可視化 (Power BI)
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

Install all required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt

```
### 3. Load Data into MySQL

Update MySQL credentials in etl/load_data.py, then run:
```bash
python etl/load_data.py
```
### 4. Run DBT Models

Navigate to the DBT project directory and execute:
```bash
cd dbt/stroke_project
dbt run
dbt test
```
### 5. Start Streamlit Dashboard (Optional)
streamlit run dashboards/streamlit_app.py

## ✅ Key Features

- 🧼 **Data Cleaning** with Pandas  
  Handle missing values, outlier filtering, gender normalization, and feature encoding (e.g., BMI median fill, gender uppercase trimming).

- 🏗 **DBT Data Models**
  - `stg_stroke_data` – Raw data staging layer
  - `int_patient_risk` – Transformed intermediate layer
  - `mart_stroke_summary` – Final reporting-ready dataset

- 🧪 **Data Validation**  
  Custom Python checks for:
  - Null values
  - Data types
  - Business rules (e.g., valid age range, bmi > 0, etc.)

- 📊 **Interactive Dashboards**  
  Visualize key trends and KPIs using:
  - Power BI (optional)

- 🔁 **CI/CD with GitHub Actions**  
  Automate data quality checks and ETL validation on every push or pull request.

- 🔒 **Version Control**  
  Project managed with Git, following modular, reusable, and production-ready folder structure.

