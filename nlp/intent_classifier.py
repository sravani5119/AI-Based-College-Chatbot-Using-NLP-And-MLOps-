# nlp/intent_classifier.py

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from nlp.training_data import TRAINING_DATA
from nlp.preprocessing import clean_text


class IntentClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))
        self.model = LogisticRegression(max_iter=1000)

    def prepare_data(self):
        texts = []
        labels = []

        for intent, examples in TRAINING_DATA.items():
            for sentence in examples:
                texts.append(clean_text(sentence))
                labels.append(intent)

        return texts, labels

    def train(self):
        texts, labels = self.prepare_data()

        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )

        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        self.model.fit(X_train_vec, y_train)

        predictions = self.model.predict(X_test_vec)

        print("\nModel Evaluation:\n")
        print(classification_report(y_test, predictions))

    def save_model(self):
        joblib.dump(self.model, "models/intent_model.pkl")
        joblib.dump(self.vectorizer, "models/vectorizer.pkl")

    def load_model(self):
        self.model = joblib.load("models/intent_model.pkl")
        self.vectorizer = joblib.load("models/vectorizer.pkl")

    def predict(self, text: str):
        cleaned = clean_text(text)
        vec = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(vec)[0]
        confidence = max(self.model.predict_proba(vec)[0])
        return prediction, confidence
