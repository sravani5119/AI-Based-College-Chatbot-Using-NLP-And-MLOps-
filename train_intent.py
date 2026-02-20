from nlp.intent_classifier import IntentClassifier

if __name__ == "__main__":
    classifier = IntentClassifier()
    classifier.train()
    classifier.save_model()
    print("\nIntent model trained and saved successfully.")
