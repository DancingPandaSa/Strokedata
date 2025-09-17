import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import numpy as np

# 1. 從 MySQL 讀取資料
engine = create_engine("mysql+pymysql://root:6363@localhost:3306/stroke")
df = pd.read_sql("SELECT * FROM stg_strokedata;", engine)

# 2. 目標變數 & 特徵
y = df['stroke']
X = df.drop(columns=['stroke', 'id'])

# 3. 類別型特徵 → One-Hot Encoding
X = pd.get_dummies(X, drop_first=True)
feature_names = X.columns

# 4. 拆分資料集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# --- 模型 1: Logistic Regression ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
lr.fit(X_train_scaled, y_train)
y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]
auc_lr = roc_auc_score(y_test, y_prob_lr)

# --- 模型 2: Random Forest ---
rf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
rf.fit(X_train, y_train)
y_prob_rf = rf.predict_proba(X_test)[:, 1]
auc_rf = roc_auc_score(y_test, y_prob_rf)

# --- 比較結果 ---
print(f"Logistic Regression AUC: {auc_lr:.4f}")
print(f"Random Forest AUC: {auc_rf:.4f}")

# --- 選出最佳模型 ---
if auc_lr > auc_rf:
    print("✅ Logistic Regression 表現比較好，建議使用它")
    best_model = lr
    best_model_name = "Logistic Regression"
    importance = np.abs(best_model.coef_[0])  # 取絕對值來表示影響程度
else:
    print("✅ Random Forest 表現比較好，建議使用它")
    best_model = rf
    best_model_name = "Random Forest"
    importance = best_model.feature_importances_

# --- 畫出條形圖 ---
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})
importance_df['Percentage'] = (importance_df['Importance'] / importance_df['Importance'].sum()) * 100
importance_df = importance_df.sort_values(by="Percentage", ascending=True)

# 畫圖
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Percentage'])
plt.xlabel("Importance (%)")
plt.ylabel("Features")
plt.title(f"Feature Importance - {best_model_name}")
plt.yticks(fontsize=8)
plt.tight_layout()
plt.show()


# --- 建立重要性資料表 ---
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})
importance_df['Percentage'] = (importance_df['Importance'] / importance_df['Importance'].sum()) * 100
importance_df = importance_df.sort_values(by="Percentage", ascending=False).reset_index(drop=True)

# --- 列印出每個特徵佔的比例 ---
print("\n📊 特徵重要性（依比例排序）:")
print(importance_df)

# --- 匯出為 Excel 檔案 ---
excel_filename = f"feature_importance_{best_model_name.replace(' ', '_')}.xlsx"
importance_df.to_excel(excel_filename, index=False)
print(f"\n✅ 特徵重要性已儲存為 Excel 檔案：{excel_filename}")
