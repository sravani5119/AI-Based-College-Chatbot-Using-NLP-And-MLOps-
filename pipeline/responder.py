# pipeline/responder.py

class Responder:

    def format_response(self, text, confidence):
        if confidence < 0.3:
                return (
                    "I'm not sure I understood correctly.\n\n"
                    "You can try asking:\n"
                    "• CSE HOD\n"
                    "• Placement contacts\n"
                    "• Academic calendar\n"
                    "• Student clubs"
                )

        return text
