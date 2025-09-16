import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# 建立連線 (請修改帳號密碼/資料庫)
engine = create_engine("mysql+pymysql://root:6363@localhost:3306/stroke")

# ============================
# 資料品質檢查函式
# ============================

def check_data_quality(df, valid_categories=None, numeric_ranges=None):
    report = {}

    # 先檢查 BMI "N/A"
    if "bmi" in df.columns:
        na_count = (df["bmi"] == "N/A").sum()
        total_rows = len(df)
        if na_count > 0:
            report["bmi_NA_strings"] = {
                "count": int(na_count),
                "percentage": round(na_count / total_rows * 100, 2),
            }

    # 1. 缺失值
    missing = df.isnull().sum()
    report["missing_values"] = missing[missing > 0].to_dict()

    # 2. 重複值
    report["duplicate_rows"] = int(df.duplicated().sum())

    # 3. 類別異常值
    categorical_issues = {}
    if valid_categories:
        for col, valid_vals in valid_categories.items():
            if col in df.columns:
                invalid = df.loc[~df[col].isin(valid_vals), col].unique().tolist()
                if invalid:
                    categorical_issues[col] = invalid
    report["categorical_issues"] = categorical_issues

    # 4. 數值範圍異常
    range_issues = {}
    if numeric_ranges:
        for col, (low, high) in numeric_ranges.items():
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                invalid = df.loc[(df[col] < low) | (df[col] > high), col]
                if not invalid.empty:
                    range_issues[col] = {
                        "count": int(len(invalid)),
                        "examples": invalid.head(10).tolist()
                    }
    report["range_issues"] = range_issues

    # 5. IQR 異常
    iqr_outliers = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].nunique() <= 2:
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = df.loc[(df[col] < lower) | (df[col] > upper), col]
        if not outliers.empty:
            iqr_outliers[col] = {
                "count": int(len(outliers)),
                "examples": outliers.head(10).tolist()
            }
    report["iqr_outliers"] = iqr_outliers

    return report

def print_quality_report(report):
    print("="*60)
    print("📊 資料品質檢查結果")
    print("="*60)

    # 缺失值
    print("\n❌ 缺失值 (Missing Values)")
    if report["missing_values"]:
        for col, count in report["missing_values"].items():
            print(f"  - {col}: {count} 筆缺失")
    else:
        print("  ✅ 無缺失值")

    # 重複列
    print("\n❌ 重複列 (Duplicate Rows)")
    if report["duplicate_rows"] > 0:
        print(f"  - 發現 {report['duplicate_rows']} 筆重複列")
    else:
        print("  ✅ 無重複列")

    # 類別異常
    print("\n❌ 類別異常 (Categorical Issues)")
    if report["categorical_issues"]:
        for col, invalids in report["categorical_issues"].items():
            print(f"  - {col}: {len(invalids)} 種異常值 → {invalids}")
    else:
        print("  ✅ 無類別異常")

    # 數值範圍異常
    print("\n❌ 數值範圍異常 (Range Issues)")
    if report["range_issues"]:
        for col, info in report["range_issues"].items():
            print(f"  - {col}: {info['count']} 筆異常 (例子: {info['examples']})")
    else:
        print("  ✅ 無數值範圍異常")

    # IQR 離群值
    print("\n❌ 統計異常 (IQR Outliers)")
    if report["iqr_outliers"]:
        for col, info in report["iqr_outliers"].items():
            print(f"  - {col}: {info['count']} 筆異常 (例子: {info['examples']})")
    else:
        print("  ✅ 無統計異常")

    # BMI "N/A" 檢查
    print("\n❌ BMI 'N/A' 字串檢查")
    if "bmi_NA_strings" in report:
        print(f"  - 發現 {report['bmi_NA_strings']['count']} 筆 'N/A' "
              f"({report['bmi_NA_strings']['percentage']}% of total)")
    else:
        print("  ✅ 無 'N/A' 字串問題")

    print("\n📌 檢查完成")


# ============================
# 🔹 匯出 Excel 報表
# ============================
def export_quality_report(report, filename="quality_report.xlsx"):
    with pd.ExcelWriter(filename) as writer:
        # 缺失值
        if report["missing_values"]:
            pd.DataFrame.from_dict(report["missing_values"], orient="index", columns=["missing_count"]).to_excel(writer, sheet_name="Missing_Values")
        # 重複列
        pd.DataFrame([{"duplicate_rows": report["duplicate_rows"]}]).to_excel(writer, sheet_name="Duplicate_Rows", index=False)
        # 類別異常
        if report["categorical_issues"]:
            pd.DataFrame([(col, vals) for col, vals in report["categorical_issues"].items()],
                         columns=["Column", "Invalid_Values"]).to_excel(writer, sheet_name="Categorical_Issues", index=False)
        # 範圍異常
        if report["range_issues"]:
            pd.DataFrame([(col, info["count"], info["examples"]) for col, info in report["range_issues"].items()],
                         columns=["Column", "Count", "Examples"]).to_excel(writer, sheet_name="Range_Issues", index=False)
        # IQR 異常
        if report["iqr_outliers"]:
            pd.DataFrame([(col, info["count"], info["examples"]) for col, info in report["iqr_outliers"].items()],
                         columns=["Column", "Count", "Examples"]).to_excel(writer, sheet_name="IQR_Outliers", index=False)
        # BMI "N/A" 檢查
        if "bmi_NA_strings" in report:
            pd.DataFrame([report["bmi_NA_strings"]]).to_excel(writer, sheet_name="BMI_NA_Strings", index=False)

    print(f"✅ 資料品質報告已匯出到 {filename}")


# ============================
# 🏃‍♀️ 使用範例
# ============================
if __name__ == "__main__":
    query = "SELECT * FROM strokedata;"
    strokedata = pd.read_sql(query, engine)

    valid_categories = {
        "gender": ["M", "F", "Other", "Male", "Female"],
        "ever_married": ["Yes", "No"],
        "work_type": ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
        "Residence_type": ["Urban", "Rural"],
        "smoking_status": ["formerly smoked", "never smoked", "smokes", "Unknown"]
    }

    numeric_ranges = {
        "age": (0, 120),
        "bmi": (10, 70),
        "avg_glucose_level": (40, 300)
    }

    quality_report = check_data_quality(strokedata, valid_categories, numeric_ranges)

    print_quality_report(quality_report)

    # 匯出 Excel
    # export_quality_report(quality_report, "stroke_quality_report.xlsx")
