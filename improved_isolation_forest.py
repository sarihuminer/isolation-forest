# פתרונות לשיפור המודל

# 1. שינוי contamination parameter
model = IsolationForest(
    n_estimators=300,
    contamination=0.025,  # שנה מ-0.05 ל-0.025 (יותר קרוב לאחוז האמיתי)
    max_samples='auto',
    random_state=42,
    n_jobs=-1
)

# 2. הוספת feature engineering
# צור פיצ'רים חדשים שמדגישים התנהגות חריגה:
df_train['print_burn_ratio'] = df_train['num_print_commands'] / (df_train['num_burn_requests'] + 1)
df_train['off_hours_activity'] = df_train['num_print_commands_off_hours'] + df_train['num_burn_requests_off_hours']
df_train['high_classification_ratio'] = df_train['avg_request_classification'] / df_train['num_burn_requests'].clip(lower=1)

# 3. שימוש בסף מותאם אישית במקום contamination קבוע
from sklearn.metrics import precision_recall_curve

# אמן את המודל
model.fit(X_train)
scores = model.decision_function(X_train)

# מצא סף אופטימלי
precision, recall, thresholds = precision_recall_curve(y_train, -scores)
f1_scores = 2 * (precision * recall) / (precision + recall)
optimal_threshold = thresholds[np.argmax(f1_scores)]

# השתמש בסף המותאם
predictions = (scores < optimal_threshold).astype(int)

# 4. נסה Local Outlier Factor במקום Isolation Forest
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(
    n_neighbors=20,
    contamination=0.025,
    novelty=True
)

# 5. Ensemble של מספר מודלים
from sklearn.ensemble import VotingClassifier
from sklearn.svm import OneClassSVM

# צור ensemble
ensemble = VotingClassifier([
    ('isolation', IsolationForest(contamination=0.025, random_state=42)),
    ('lof', LocalOutlierFactor(contamination=0.025, novelty=True)),
    ('svm', OneClassSVM(nu=0.025))
], voting='hard')