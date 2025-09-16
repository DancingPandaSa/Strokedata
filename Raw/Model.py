import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# SQLAlchemy
from sqlalchemy import create_engine

# Scikit-learn & other libraries
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
import shap

# 1. Connect to the MySQL database
# Replace 'root' and '1234' with your actual username and password
try:
    engine = create_engine("mysql+pymysql://root:6363@localhost:3306/stroke")
    conn = engine.connect()

    # Read data from the 'int_strokedata' table
    query = "SELECT * FROM int_strokedata;"
    df = pd.read_sql(query, conn)
    conn.close()

    print("Successfully read data from MySQL. DataFrame shape:", df.shape)

except Exception as e:
    print(f"Database connection error or query failed: {e}")
    df = pd.DataFrame() # Create an empty DataFrame to prevent script from crashing
    exit()

# 2. Data Preparation
# Convert boolean/string columns to integer/numeric types if needed
# (pd.read_sql usually does a good job of this, but it's a good practice to double-check)
df['stroke'] = df['stroke'].astype(int)

# Define features and target
TARGET = 'stroke'
cat_features = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status', 'age_group', 'bmi_category', 'glucose_level_category']
num_features = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']

X = df.drop(columns=[TARGET])
y = df[TARGET]

# Filter out features not present in the DataFrame
cat_features = [c for c in cat_features if c in X.columns]
num_features = [c for c in num_features if c in X.columns]

# 3. Build Preprocessing Pipeline
num_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

cat_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, num_features),
    ('cat', cat_transformer, cat_features)
])

# 4. Split data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# 5. Define Models
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

# 6. Train and Compare Models
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

print(f"\nBest model: {best_name} (AUC={best_auc:.4f})")

# 7. Model Evaluation (plots)
# (Same as your original code)
y_prob = best_model.predict_proba(X_val)[:, 1]

# ROC Curve
fpr, tpr, _ = roc_curve(y_val, y_prob)
plt.plot(fpr, tpr, label=f"{best_name} (AUC={best_auc:.3f})")
plt.plot([0,1],[0,1],'k--')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()

# Precision-Recall Curve
prec, rec, _ = precision_recall_curve(y_val, y_prob)
plt.plot(rec, prec, label=best_name)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.show()

# Confusion Matrix
y_pred = (y_prob >= 0.5).astype(int)
cm = confusion_matrix(y_val, y_pred)
ConfusionMatrixDisplay(cm).plot()
plt.show()

# 8. Save the best model
joblib.dump(best_model, 'best_stroke_model.pkl')
print("Best model saved to 'best_stroke_model.pkl'")