from html import entities
from knowledge_base.loader import (
    load_knowledge_base,
    load_placements,
    load_rnd,
    load_clubs
)


class Retriever:

    def __init__(self):
        self.kb = load_knowledge_base()

    def retrieve(self, intent, entities, user_input=None):

        if user_input:
            query = user_input.lower()
        else:
            query = ""

        # SAFETY: if entities is None, convert to empty dict
        if not entities:
            entities = {}

        if intent == "research" and "branch" in entities:
            print("OVERRIDE ACTIVATED → switching to departments")
            intent = "departments"

        print("FINAL INTENT:", intent)

        # ----------------------------------------
        # CONTACT
        # ----------------------------------------
        if intent == "contact":
            data = self.kb.get("contact", {})
            phones = data.get("phone", [])
            emails = data.get("email", [])
            address = data.get("address", "")

            if not phones and not emails and not address:
                return "Contact information not available."

            phone_text = ", ".join(phones)
            email_text = ", ".join(emails)

            return f"Phone: {phone_text} | Email: {email_text} | Address: {address}"

        # ----------------------------------------
        # ADMISSIONS
        # ----------------------------------------
        if intent == "admissions":
            data = self.kb.get("admissions", {})

            # COURSES OFFERED
            if "course" in query:
                courses = data.get("courses_offered")

                if not courses:
                    return "Courses information not available."

                # If structured dictionary (new improved scraping)
                if isinstance(courses, dict):
                    response_lines = []

                    for degree, branches in courses.items():
                        response_lines.append(f"{degree}")

                        if isinstance(branches, list):
                            for branch in branches:
                                response_lines.append(f" - {branch}")

                        response_lines.append("")

                    return "\n".join(response_lines).strip()

                # If still old string format
                return courses

            # ELIGIBILITY
            if "eligibility" in query:
                return data.get("eligibility", "Eligibility information not available.")

            # FEE / PAYMENTS
            if "payment" in query or "fee" in query:
                return data.get("epayments", "Payment information not available.")

            # DEFAULT → PROCEDURE
            return data.get("procedure", "Admission procedure not available.")

        # ----------------------------------------
        # DEPARTMENTS
        # ----------------------------------------
        if intent == "departments":

            departments = self.kb.get("departments", {})

            dept_map = {
                "cse": "computer_science_and_engineering",
                "ai": "cse_ai_ml",
                "artificial intelligence": "cse_ai_ml",
                "cyber": "cse_cyber_security",
                "data science": "cse_data_science",
                "freshman": "freshman_engineering",
                "school of computing": "school_of_computing"
            }

            selected_dept = None

            for keyword, dept_key in dept_map.items():
                if keyword in query:
                    selected_dept = dept_key
                    break

            if not selected_dept:
                return "Please specify department name."

            dept_data = departments.get(selected_dept, {})

            if "hod" in query:
                return self.clean_response(dept_data.get("hod-message"))

            if "vision" in query or "mission" in query:
                return self.clean_response(dept_data.get("vision-mission"))

            if "faculty" in query or "staff" in query:
                return self.clean_response(dept_data.get("teaching-staff"))

            if "achievement" in query:
                return self.clean_response(dept_data.get("achivements"))

            # FIX: If branch mentioned with research → treat as department
            if intent == "research" and entities.get("branch"):
                intent = "departments"
                print("FINAL INTENT:", intent)

            if "research" in query:
                return self.clean_response(dept_data.get("research-and-consultancy"))

            return self.clean_response(dept_data.get("about"))

        # ----------------------------------------
        # PLACEMENTS
        # ----------------------------------------
        if intent == "placements":

            placements_data = load_placements()

            if not placements_data:
                return "Placements information not available."

            if "recruit" in query:
                return placements_data.get("recruiters", [])

            elif "year" in query:
                return placements_data.get("year_wise", {})

            elif "contact" in query:
                return placements_data.get(
                    "contacts",
                    "Placement contact information not available."
                )

            else:
                return self.clean_response(
                    placements_data.get(
                        "about",
                        "Placements information not available."
                    )
                )

        # ----------------------------------------
        # RESEARCH & DEVELOPMENT
        # ----------------------------------------
        if intent == "research":

            rnd_data = load_rnd()

            if not rnd_data:
                return "R&D information not available."

            if "newgen" in query or "iedc" in query:
                return self.clean_response(rnd_data.get("newgen_iedc"))

            elif "excellence" in query:
                return self.clean_response(rnd_data.get("centre_of_excellence"))

            elif "idea lab" in query or "aicte" in query:
                return self.clean_response(rnd_data.get("aicte_idea_lab"))

            else:
                return self.clean_response(rnd_data.get("rd_cell"))

        # ----------------------------------------
        # STUDENT CLUBS
        # ----------------------------------------
        if intent == "student_clubs":

            query_lower = user_input.lower()
            clubs_json = load_clubs()

            clubs_list = clubs_json.get("clubs_list", [])
            clubs_data = clubs_json.get("clubs_data", {})

            # 1️⃣ If asking generally about clubs → return only names
            if "about clubs" in query_lower or "list" in query_lower or "what clubs" in query_lower:
                return "\n".join(clubs_list)

            # 2️⃣ If asking specific club
            if "radio" in query_lower:
                return self.clean_response(clubs_data.get("radio_club"))

            elif "coder" in query_lower:
                return self.clean_response(clubs_data.get("coders_club"))

            elif "creator" in query_lower:
                return self.clean_response(clubs_data.get("creators_club"))

            elif "cultural" in query_lower:
                return self.clean_response(clubs_data.get("cultural_club"))

            elif "eco" in query_lower:
                return self.clean_response(clubs_data.get("eco_club"))

            elif "fitness" in query_lower:
                return self.clean_response(clubs_data.get("fitness_club"))

            elif "gamer" in query_lower:
                return self.clean_response(clubs_data.get("gamers_club"))

            elif "handler" in query_lower or "robo" in query_lower:
                return self.clean_response(clubs_data.get("handlers_club"))

            elif "literary" in query_lower or "fine arts" in query_lower:
                return self.clean_response(clubs_data.get("literary_club"))

            elif "multimedia" in query_lower or "trinetra" in query_lower:
                return self.clean_response(clubs_data.get("multimedia_club"))

            elif "nss" in query_lower:
                return self.clean_response(clubs_data.get("nss_club"))

            elif "sport" in query_lower:
                return self.clean_response(clubs_data.get("sports_club"))

            elif "women" in query_lower or "sheinspires" in query_lower:
                return self.clean_response(clubs_data.get("womens_club"))

            return "Please specify which club you want information about."

        # ----------------------------------------
        # DEFAULT
        # ----------------------------------------
        return "Sorry, I could not find relevant information."

    def clean_response(self, text):

        if not text:
            return "Information not available."

        unwanted_phrases = [
            "SPHN ||",
            "An Autonomous Institution",
            "SHHN Location on Google Maps",
            "Facebook",
            "Instagram",
            "YouTube",
            "Linkedin",
            "SPHN in Media",
            "SPHN Gallery",
            "Mandatory Disclosures",
            "Download Brochure",
            "Full Name",
            "Email Id",
            "Mobile",
            "Submit",
            "Enquiry",
            "Alumni"
        ]

        for phrase in unwanted_phrases:
            text = text.replace(phrase, "")

        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)