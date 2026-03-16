from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import extract_entities
from pipeline.retriever import Retriever
from pipeline.responder import Responder
from nlp.spell_corrector import correct_spelling


class ChatbotEngine:

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.intent_classifier.load_model()
        self.retriever = Retriever()
        self.responder = Responder()


        

    def get_response(self, user_input):

        corrected_input = correct_spelling(user_input)
        query = corrected_input.lower()

        # -------------------------
        # About SPHN / College
        # -------------------------
        if (
            "sphn" in query
            or "sphoorthy" in query
            or "sphoorthy engineering college" in query
            or "about sphoorthy" in query
            or "about the college" in query
            or "tell me about the college" in query
        ):
            return {
                "intent": "about_college",
                "entities": {},
                "confidence": 1.0,
                "response": """Sphoorthy Engineering College, since its inception in 2004, has been setting new milestones and maintaining a consistent and disciplined growth in all the areas of functionality. This has resulted into an array of star performers who are not only excelling in their academic endeavours, but also contributing significantly as professionals in the companies of high repute in India. The college ranks 8th in research and capabilities in TS and AP Times Engineering Survey 2022 and 11th rank in AP and TS. The institution continues to maintain its position among the top-notch, over the years.

        Over the last 18 years, SPHN has evolved as the corridor of excellence in all its service deliverables and has set a bench mark for excellence in providing high quality education, research and innovation in emerging technological domains.

        SPHN synchronizes its efforts and members complement each other with a common objective of meeting student’s aspirations and helps them realize their goals."""
            }

        # Greeting override
        if query in ["hi", "hello", "hey"]:
            return {
                "intent": "greeting",
                "entities": {},
                "confidence": 1.0,
                "response": "Hello! 👋 How can I help you today?\n\nYou can ask about:\n• Admissions\n• Placements\n• Academic Calendar\n• Departments\n• Student Clubs"
            }
        
        # -------------------------
        # Bot identity
        # -------------------------
        if "who are you" in query or "what are you" in query or "about you" in query:
            return {
                "intent": "about_bot",
                "entities": {},
                "confidence": 1.0,
                "response": "I am the Sphoorthy Engineering College chatbot. I help students and visitors find information about admissions, placements, departments, academic calendar, student clubs, and other college services."
            }


        # quick overrides for name queries
        if "principal" in query:
            intent = "contact"
            confidence = 1.0

        elif "hod" in query:
            intent = "departments"
            confidence = 1.0

        else:
            intent, confidence = self.intent_classifier.predict(corrected_input)

        entities = extract_entities(corrected_input)

        result = self.retriever.retrieve(intent, entities, corrected_input)

        final_response = self.responder.format_response(result, confidence)

        return {
            "intent": intent,
            "entities": entities,
            "confidence": confidence,
            "response": final_response
        }


        