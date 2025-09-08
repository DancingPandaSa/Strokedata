# 📦 导入所需库
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, chi2_contingency
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# 📂 读取数据
df = pd.read_csv("healthcare-dataset-stroke-data.csv")

# 🧼 数据清理
df.dropna(subset=["bmi"], inplace=True)
df["bmi"] = df["bmi"].astype(float)

# 🔤 编码分类变量
label_cols = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
df[label_cols] = df[label_cols].apply(lambda col: LabelEncoder().fit_transform(col.astype(str)))

# 📊 可视化：年龄 vs 中风
plt.figure(figsize=(8, 5))
sns.boxplot(x="stroke", y="age", data=df)
plt.title("Age vs Stroke")
plt.show()

# 📊 可视化：婚姻状况 vs 中风率
married_stroke = df.groupby('ever_married')['stroke'].mean().reset_index()
married_stroke['ever_married'] = married_stroke['ever_married'].map({0: 'No', 1: 'Yes'})

sns.barplot(data=married_stroke, x='ever_married', y='stroke')
plt.title("Stroke Rate by Marital Status")
plt.ylabel("Stroke Rate")
plt.show()

# 🧪 t-test: 年龄 vs 中风
stroke_age = df[df['stroke'] == 1]['age']
nonstroke_age = df[df['stroke'] == 0]['age']
t_stat_age, p_val_age = ttest_ind(stroke_age, nonstroke_age)
print(f"T-test (age): p-value = {p_val_age:.5f}")

# 🧪 卡方检验：婚姻 vs 中风
contingency_married = pd.crosstab(df['ever_married'], df['stroke'])
chi2_married, p_married, _, _ = chi2_contingency(contingency_married)
print(f"Chi-square (married): p-value = {p_married:.5f}")

# 🤖 随机森林建模
X = df.drop(columns=["id", "stroke"])
y = df["stroke"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# 🔍 特征重要性
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x="Importance", y="Feature")
plt.title("Feature Importance from Random Forest")
plt.show()

# 🧾 分类结果报告
print(classification_report(y_test, y_pred))
