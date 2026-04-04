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

        query = user_input.lower()

        # -------------------------
        # Query Normalization Layer
        # -------------------------
        synonyms = {
            "academic": "academics",
            "dept": "department",
            "depart": "department",
            "placements": "placement",
            "clubs": "club",
            "faculty": "staff",
            "eligibity": "eligibility",
            "eligible": "eligibility",
        }

        # -------------------------
        # Short Query Handling
        # -------------------------
        words = query.split()

        if len(words) <= 2:
            if any(dept in query for dept in ["cse", "aiml", "cyber", "data science", "freshman"]):
                intent = "departments"
                confidence = 1.0

            elif "placement" in query:
                intent = "placements"
                confidence = 1.0

            elif "club" in query:
                intent = "student_clubs"
                confidence = 1.0

            elif "calendar" in query or "academics" in query:
                intent = "academics"
                confidence = 1.0

            else:
                intent = None

        for key, value in synonyms.items():
            query = query.replace(key, value)

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
        if query in ["hi", "hello", "hey", "good morning", "good evening"]:
            return {
                "intent": "greeting",
                "entities": {},
                "confidence": 1.0,
                "response": "Hello! 👋 How can I help you today?\n\nYou can ask about:\n• Admissions\n• Placements\n• Academic Calendar\n• Departments\n• Student Clubs"
            }
        
        if "help" in query:
            return {
                "intent": "help",
                "entities": {},
                "confidence": 1.0,
                "response": (
                    "You can ask me about:\n\n"
                    "• Admissions\n"
                    "• Placements\n"
                    "• Departments (CSE, AIML, etc.)\n"
                    "• Academic Calendar\n"
                    "• Student Clubs\n"
                    "• Contact Details"
                )
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


        
        # -------------------------
        # Keyword Intent Overrides (HIGH PRIORITY)
        # -------------------------
        # -------------------------
        # Keyword Intent Overrides (FIX ORDER ONLY)
        # -------------------------

        # 🔥 departments FIRST (very important)
        if "hod" in query or "department" in query or "achievement" in query:
            intent = "departments"
            confidence = 1.0

        elif "placement" in query:
            intent = "placements"
            confidence = 1.0

        elif "club" in query:
            intent = "student_clubs"
            confidence = 1.0

        elif "calendar" in query or "academics" in query:
            intent = "academics"
            confidence = 1.0

        elif "contact" in query or "principal" in query:
            intent = "contact"
            confidence = 1.0

        elif "eligibility" in query or "eligible" in query or "eligib" in query:
            intent = "admissions"
            confidence = 1.0

        elif "admission" in query:
            intent = "admissions"
            confidence = 1.0

        elif "research" in query or "r&d" in query:
            intent = "research"
            confidence = 1.0
            
        if intent is None:
            intent, confidence = self.intent_classifier.predict(user_input)

        # -------------------------
        # Low Confidence Fallback
        # -------------------------
        if confidence < 0.4:
            if "cse" in query or "aiml" in query:
                intent = "departments"
                confidence = 0.6

            elif "placement" in query:
                intent = "placements"
                confidence = 0.6

            elif "club" in query:
                intent = "student_clubs"
                confidence = 0.6

        entities = extract_entities(user_input)

        try:
            result = self.retriever.retrieve(intent, entities, user_input)
        except Exception as e:
            import traceback
            traceback.print_exc()   # 🔥 THIS WILL SHOW FULL ERROR
            result = "Something went wrong. Please try again."

        final_response = self.responder.format_response(result, confidence)
        print("User Query:", query)
        print("Intent:", intent)
        print("Entities:", entities)
        print("Confidence:", confidence)
        return {
            "intent": intent,
            "entities": entities,
            "confidence": confidence,
            "response": final_response
        }


        