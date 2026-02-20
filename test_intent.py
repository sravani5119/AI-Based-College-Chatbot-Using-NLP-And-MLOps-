# test_intent.py

from nlp.intent_classifier import IntentClassifier

clf = IntentClassifier()
clf.load_model()

while True:
    user_input = input("You: ")
    intent, confidence = clf.predict(user_input)
    print(f"Predicted Intent: {intent}")
    print(f"Confidence: {confidence:.2f}")
