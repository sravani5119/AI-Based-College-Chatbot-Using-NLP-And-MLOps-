from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import extract_entities
from pipeline.retriever import Retriever
from pipeline.responder import Responder


class ChatbotEngine:

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.intent_classifier.load_model()
        self.retriever = Retriever()
        self.responder = Responder()

    def get_response(self, user_input):

        intent, confidence = self.intent_classifier.predict(user_input)
        entities = extract_entities(user_input)

        # Pass user_input to retriever
        result = self.retriever.retrieve(intent, entities, user_input)


        final_response = self.responder.format_response(result, confidence)

        return {
            "intent": intent,
            "entities": entities,
            "confidence": round(confidence, 2),
            "response": final_response
        }
