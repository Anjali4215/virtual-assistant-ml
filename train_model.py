import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# Load dataset
df = pd.read_csv("intents.csv")

# Vectorization
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['intent']

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model and vectorizer
os.makedirs("models", exist_ok=True)
pickle.dump(model, open("models/trained_model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("✅ Model training completed and files saved!")