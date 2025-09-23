# Save this as: backend/train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib # Used for saving our trained model

# 1. Load your dataset
print("Loading dataset...")
df = pd.read_csv("malicious_phish.csv")

# Create a simplified label: 1 for malicious (phishing/defacement), 0 for benign
df['label'] = df['type'].apply(lambda x: 1 if x in ['phishing', 'defacement'] else 0)

# Separate features (URLs) and labels
urls = df['url']
labels = df['label']

# 2. Create the TF-IDF Vectorizer
# This learns how to turn any URL into a set of numbers.
# We use 'char' analyzer to look at characters, which is effective for URLs.
print("Creating vectorizer...")
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 5))

# 3. Vectorize the URL data
print("Vectorizing data...")
X = vectorizer.fit_transform(urls)

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# 4. Train the Machine Learning Model
print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate the model (optional, but good practice)
accuracy = model.score(X_test, y_test)
print(f"Model trained with an accuracy of: {accuracy * 100:.2f}%")

# 6. Save the trained model and vectorizer to files
print("Saving model and vectorizer to files...")
joblib.dump(model, 'url_model.joblib')
joblib.dump(vectorizer, 'url_vectorizer.joblib')

print("Training complete. Model saved as url_model.joblib.")