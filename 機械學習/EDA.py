# 1. 讀入資料與基本設定
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline as ImbPipeline  # 用於 SMOTE 等處理
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score, roc_curve,
    precision_recall_curve, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import shap
import warnings
warnings.filterwarnings("ignore")

# 讀取 MySQL 中的 kaggle 資料表
engine = create_engine("mysql+pymysql://root:6363@localhost:3306/stroke")
kaggle = pd.read_sql("SELECT * FROM strokedata;", engine)

# 處理 BMI 欄位（轉數字 + 補中位數）
kaggle["bmi"] = pd.to_numeric(kaggle["bmi"], errors="coerce")
kaggle["bmi"] = kaggle["bmi"].fillna(kaggle["bmi"].median())

# 顯示缺失值報告
def missing_report(df):
    miss = df.isnull().sum()
    return pd.DataFrame({
        "missing_count": miss,
        "missing_pct": miss / len(df) * 100
    }).sort_values("missing_pct", ascending=False)

print("Kaggle missing:\n", missing_report(kaggle))

# 分類欄位補充處理
categorical_cols = ['gender','ever_married','work_type','Residence_type','smoking_status']
categorical_cols = [c for c in categorical_cols if c in kaggle.columns]

# 特徵工程：新增 age group
def add_age_groups(df):
    df['age_group'] = pd.cut(df['age'], bins=[0,40,60,80,120], labels=['<40','40-59','60-79','80+'])
    return df

kaggle = add_age_groups(kaggle)

# 數值與類別欄位定義
num_features = ['age','bmi','avg_glucose_level']
num_features = [c for c in num_features if c in kaggle.columns]
cat_features = [c for c in categorical_cols if c in kaggle.columns]

# 預處理 pipeline
num_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', num_transformer, num_features),
    ('cat', cat_transformer, cat_features)
])

# 分割資料
TARGET = 'stroke'
X = kaggle.drop(columns=[TARGET])
y = kaggle[TARGET]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# 建立模型
models = {
    'lr': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'rf': RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced'),
    'xgb': XGBClassifier(n_estimators=200, scale_pos_weight=10, eval_metric='logloss', random_state=42)
}

def evaluate_model(pipe, X_tr, y_tr, X_te, y_te):
    pipe.fit(X_tr, y_tr)
    y_pred = pipe.predict(X_te)
    y_prob = pipe.predict_proba(X_te)[:, 1]
    print(classification_report(y_te, y_pred, digits=4))
    auc = roc_auc_score(y_te, y_prob)
    print("ROC AUC:", auc)
    return pipe, auc

# 訓練模型並比較
best_auc = 0
best_model = None
best_name = ""

for name, clf in models.items():
    print("="*40)
    print(f"Training {name}")
    pipe = ImbPipeline([
        ('preproc', preprocessor),
        ('clf', clf)
    ])
    trained_pipe, auc = evaluate_model(pipe, X_train, y_train, X_val, y_val)
    if auc > best_auc:
        best_auc = auc
        best_model = trained_pipe
        best_name = name

print(f"\n✅ Best model: {best_name.upper()} (AUC={best_auc:.4f})")

# 評估圖形
y_prob = best_model.predict_proba(X_val)[:, 1]
fpr, tpr, _ = roc_curve(y_val, y_prob)
plt.plot(fpr, tpr, label=f"{best_name.upper()} (AUC={best_auc:.3f})")
plt.plot([0,1],[0,1],'k--')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()

# PR 曲線
prec, rec, _ = precision_recall_curve(y_val, y_prob)
plt.plot(rec, prec, label=best_name)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.show()

# 混淆矩陣
y_pred = (y_prob >= 0.5).astype(int)
cm = confusion_matrix(y_val, y_pred)
ConfusionMatrixDisplay(cm).plot()
plt.title("Confusion Matrix")
plt.show()

# === SHAP 分析 ===
clf = best_model.named_steps["clf"]
X_train_pre = best_model.named_steps["preproc"].transform(X_train)
X_val_pre = best_model.named_steps["preproc"].transform(X_val)

# 特徵名稱提取函數
def get_feature_names_from_column_transformer(column_transformer):
    output_features = []
    for name, transformer, cols in column_transformer.transformers_:
        if transformer == "drop":
            continue
        if transformer == "passthrough":
            output_features.extend(cols)
        else:
            if hasattr(transformer, "get_feature_names_out"):
                output_features.extend(transformer.get_feature_names_out(cols))
            else:
                output_features.extend(cols)
    return output_features

feat_names = get_feature_names_from_column_transformer(best_model.named_steps['preproc'])

# 建立 explainer 並計算 shap 值
if isinstance(clf, LogisticRegression):
    masker = shap.maskers.Independent(X_train_pre)
    explainer = shap.LinearExplainer(clf, masker=masker)
    shap_values = explainer(X_val_pre)
    shap_vals = shap_values.values
elif isinstance(clf, (RandomForestClassifier, XGBClassifier)):
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_val_pre)
    shap_vals = shap_values[1] if isinstance(shap_values, list) else shap_values
else:
    raise ValueError(f"不支援的模型類型: {type(clf)}")

# 特徵重要性計算與顯示
shap_importance = np.abs(shap_vals).mean(axis=0)
shap_df = pd.DataFrame({
    "Feature": feat_names,
    "Importance": shap_importance
})
shap_df["Percentage"] = shap_df["Importance"] / shap_df["Importance"].sum() * 100
shap_df = shap_df.sort_values("Importance", ascending=False).reset_index(drop=True)

print("\n📊 SHAP 特徵重要性（前10名）:")
print(shap_df.head(10).round(2))

# SHAP 條形圖
plt.figure(figsize=(10, 6))
sns.barplot(x="Importance", y="Feature", data=shap_df, palette="viridis")
plt.title(f"Feature Importance based on SHAP ({best_name.upper()})")
plt.xlabel("Mean |SHAP value|")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

# 繪圖
feat_names = get_feature_names_from_column_transformer(best_model.named_steps['preproc'])
shap.summary_plot(shap_values, X_val_pre, feature_names=feat_names)
# 儲存至 Excel
shap_df.to_excel("feature_importance_shap.xlsx", index=False)
print("✅ SHAP特徵重要性表格已儲存為 'feature_importance_shap.xlsx'")
