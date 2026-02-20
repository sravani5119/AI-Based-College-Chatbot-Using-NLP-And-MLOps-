# pipeline/responder.py

class Responder:

    def format_response(self, text, confidence):
        if confidence < 0.15:
            return "I'm not confident about the answer. Please rephrase your question."

        return text
