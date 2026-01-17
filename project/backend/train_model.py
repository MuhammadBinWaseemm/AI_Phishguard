import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score, precision_recall_curve
import re
import warnings
warnings.filterwarnings('ignore')
from imblearn.over_sampling import SMOTE

print("="*60)
print("AI-PhishGuard: Model Training Pipeline")
print("="*60)

CSV_PATH = "Combined.csv"
MODEL_DIR = "models"

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("\n[1/8] Loading dataset...")
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8", on_bad_lines='skip')
except:
    df = pd.read_csv(CSV_PATH, encoding="latin1", on_bad_lines='skip')

print(f"✓ Dataset loaded: {df.shape[0]} emails")

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print("\n[2/8] Feature Engineering...")

df['subject'] = df['subject'].astype(str).fillna('')
df['body'] = df['body'].astype(str).fillna('')
df['sender'] = df['sender'].astype(str).fillna('unknown')
df['receiver'] = df['receiver'].astype(str).fillna('unknown')

df['subject_length'] = df['subject'].str.len()
df['body_length'] = df['body'].str.len()
df['sender_length'] = df['sender'].str.len()

df['has_url'] = df['body'].str.contains(r'http[s]?://', na=False).astype(int)
df['url_count'] = df['body'].str.count(r'http[s]?://')
df['suspicious_url'] = df['body'].str.contains(r'(bit\.ly|goo\.gl|tinyurl|click|redirect)', case=False).astype(int)

df['special_char_ratio'] = df['body'].apply(lambda x: len(re.findall(r'[^\w\s]', str(x))) / max(len(str(x)), 1))
df['digit_ratio'] = df['body'].apply(lambda x: len(re.findall(r'\d', str(x))) / max(len(str(x)), 1))
df['uppercase_ratio'] = df['body'].apply(lambda x: len(re.findall(r'[A-Z]', str(x))) / max(len(str(x)), 1))

df['word_count'] = df['body'].apply(lambda x: len(str(x).split()))
df['avg_word_length'] = df['body'].apply(lambda x: np.mean([len(word) for word in str(x).split()]) if len(str(x).split()) > 0 else 0)
df['subject_word_count'] = df['subject'].apply(lambda x: len(str(x).split()))

phishing_keywords = [
    'urgent', 'verify', 'account', 'security', 'bank', 'login', 'click',
    'update', 'alert', 'suspend', 'password', 'confirm', 'winner', 'prize',
    'free', 'limited', 'offer', 'congratulations', 'important',
    'action required', 'immediately', 'unauthorized', 'billing', 'invoice'
]

for word in phishing_keywords:
    df[f'has_{word}'] = df['body'].str.lower().str.contains(word, regex=False).astype(int)

df['suspicious_sender'] = (
    df['sender'].str.contains(r'[\d]{5,}', regex=True) |
    df['sender'].str.contains(r'[!$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', regex=True)
).astype(int)

df['generic_greeting'] = df['body'].str.contains(r'^(dear|customer|user|valued)', case=False, regex=True).astype(int)

if 'date' in df.columns:
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['hour'] = df['date'].dt.hour.fillna(12)
        df['day_of_week'] = df['date'].dt.dayofweek.fillna(0)
    except:
        df['hour'] = 12
        df['day_of_week'] = 0
else:
    df['hour'] = 12
    df['day_of_week'] = 0

print("✓ Features engineered successfully")

print("\n[3/8] Preparing feature set...")

autoencoder_features = [
    'subject_length', 'body_length', 'sender_length',
    'word_count', 'avg_word_length', 'subject_word_count',
    'special_char_ratio', 'digit_ratio', 'uppercase_ratio',
    'hour', 'day_of_week'
]

keyword_features = [f'has_{word}' for word in phishing_keywords]
autoencoder_features.extend(keyword_features)

url_features = ['has_url', 'url_count', 'suspicious_url']
autoencoder_features.extend(url_features)

structural_features = ['suspicious_sender', 'generic_greeting']
autoencoder_features.extend(structural_features)

if "label" not in df.columns:
    raise ValueError("ERROR: Dataset must contain a 'label' column.")

df["label"] = pd.to_numeric(df["label"], errors="coerce")
df.dropna(subset=["label"], inplace=True)
df["label"] = df["label"].astype(int)

X_autoencoder = df[autoencoder_features].fillna(0)

constant_features = X_autoencoder.columns[X_autoencoder.nunique() <= 1]
if len(constant_features) > 0:
    X_autoencoder = X_autoencoder.drop(columns=constant_features)
    autoencoder_features = [f for f in autoencoder_features if f not in constant_features]

y = df["label"]

print(f"✓ Feature set ready: {len(autoencoder_features)} features")
print(f"  Class distribution: {dict(y.value_counts().sort_index())}")

print("\n[4/8] Train-test split & scaling...")

X_train, X_test, y_train, y_test = train_test_split(
    X_autoencoder, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("\n[4.1] Applying SMOTE Oversampling...")

sm = SMOTE(random_state=42)

X_train_res, y_train_res = sm.fit_resample(
    X_train_scaled,
    y_train
)

y_train_res = y_train_res.astype(int)



print("✓ Oversampling complete")
print("  New class distribution:",
      dict(pd.Series(y_train_res).value_counts().sort_index()))

print(f"✓ Train: {X_train_scaled.shape} | Test: {X_test_scaled.shape}")

print("\n[5/8] Training Autoencoder...")

X_train_safe = X_train_scaled[y_train == 0]

autoencoder = MLPRegressor(
    hidden_layer_sizes=(64, 32, 16, 32, 64),
    activation='relu',
    random_state=42,
    max_iter=500,
    alpha=0.001,
    learning_rate='adaptive',
    early_stopping=True,
    validation_fraction=0.1
)

autoencoder.fit(X_train_safe, X_train_safe)
print("✓ Autoencoder trained")

print("\n[6/8] Computing reconstruction errors...")

train_reconstructions = autoencoder.predict(X_train_scaled)
train_mse = np.mean((X_train_scaled - train_reconstructions) ** 2, axis=1)

test_reconstructions = autoencoder.predict(X_test_scaled)
test_mse = np.mean((X_test_scaled - test_reconstructions) ** 2, axis=1)

precisions, recalls, thresholds = precision_recall_curve(y_test, test_mse)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls)
best_idx = np.nanargmax(f1_scores)
best_threshold = thresholds[best_idx]

print(f"✓ Anomaly threshold: {best_threshold:.4f}")

print("\n[7/8] Training Random Forest...")

X_train_enhanced = np.column_stack((
    X_train_scaled,
    train_mse,
    train_mse ** 2,
    np.sqrt(train_mse)
))

X_test_enhanced = np.column_stack((
    X_test_scaled,
    test_mse,
    test_mse ** 2,
    np.sqrt(test_mse)
))

rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight='balanced',
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt'
)

rf_model.fit(X_train_enhanced, y_train)

y_pred_rf = rf_model.predict(X_test_enhanced)
y_pred_proba = rf_model.predict_proba(X_test_enhanced)[:, 1]

print("✓ Random Forest trained")

print("\n[8/8] Model Evaluation...")

accuracy = accuracy_score(y_test, y_pred_rf)
precision = precision_score(y_test, y_pred_rf)
recall = recall_score(y_test, y_pred_rf)
f1 = f1_score(y_test, y_pred_rf)
auc_roc = roc_auc_score(y_test, y_pred_proba)
cm = confusion_matrix(y_test, y_pred_rf)
tn, fp, fn, tp = cm.ravel()

print(f"\n📊 Model Performance:")
print(f"   Accuracy:  {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall:    {recall:.4f}")
print(f"   F1-Score:  {f1:.4f}")
print(f"   ROC AUC:   {auc_roc:.4f}")
print(f"\n   Confusion Matrix:")
print(f"   True Negatives:  {tn}")
print(f"   False Positives: {fp}")
print(f"   False Negatives: {fn}")
print(f"   True Positives:  {tp}")

print("\n" + "="*60)
print("Saving models...")
print("="*60)

model_config = {
    'autoencoder_features': autoencoder_features,
    'anomaly_threshold': float(best_threshold),
    'feature_count': len(autoencoder_features),
    'phishing_keywords': phishing_keywords
}

with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)
    print("✓ scaler.pkl saved")

with open(os.path.join(MODEL_DIR, 'autoencoder.pkl'), 'wb') as f:
    pickle.dump(autoencoder, f)
    print("✓ autoencoder.pkl saved")

with open(os.path.join(MODEL_DIR, 'random_forest.pkl'), 'wb') as f:
    pickle.dump(rf_model, f)
    print("✓ random_forest.pkl saved")

with open(os.path.join(MODEL_DIR, 'config.pkl'), 'wb') as f:
    pickle.dump(model_config, f)
    print("✓ config.pkl saved")

print("\n" + "="*60)
print("✓ Training Complete!")
print("="*60)
print(f"\nModels saved in: {MODEL_DIR}/")
print("\nReady to start the FastAPI server!")
