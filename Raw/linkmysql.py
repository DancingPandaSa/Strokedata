import pandas as pd
from sqlalchemy import create_engine

# 创建连接 (请替换你的用户名、密码、数据库名)
engine = create_engine("mysql+pymysql://root:6363@localhost:3306/stroke")

# 从 MySQL 读取数据
query = "SELECT * FROM strokedata;"
strokedata = pd.read_sql(query, engine)

print(strokedata.head())
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# 目标变量
y = strokedata['stroke']

# 特征变量（去掉 id 和 stroke）
X = strokedata.drop(columns=['stroke', 'id'])

# 对类别型特征做编码
for col in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 随机森林
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 计算特征重要性
importances = model.feature_importances_
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
})
importance_df['Percentage'] = (importance_df['Importance'] / importance_df['Importance'].sum()) * 100
importance_df = importance_df.sort_values(by='Percentage', ascending=False)

print(importance_df)
