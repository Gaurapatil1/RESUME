import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
df = pd.read_csv("resume_dataset.csv")

# Select useful features
features = df[['Skills', 'Experience (Years)', 'Certifications', 'Projects Count', 'AI Score (0-100)']]
target = df['Job Role']

# Combine text + numbers by converting 'Skills' to vector (text → numbers)
tfidf = TfidfVectorizer(max_features=300)
X_text = tfidf.fit_transform(features['Skills'].fillna("")).toarray()

# Combine with other numeric features
X = pd.concat([
    pd.DataFrame(X_text),
    features[['Experience (Years)', 'Certifications', 'Projects Count', 'AI Score (0-100)']].reset_index(drop=True)
], axis=1)

# Encode target label
le = LabelEncoder()
y = le.fit_transform(target)

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train ML model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))