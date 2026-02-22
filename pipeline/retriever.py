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
        
         # --- Override for placement contact queries ---
        if "placement" in query and "contact" in query:
            intent = "placements"

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
            return self.format_admission_procedure(data.get("procedure"))
        
        
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
                return self.trim_response(dept_data.get("hod-message"))

            if "vision" in query or "mission" in query:
                return self.trim_response(dept_data.get("vision-mission"))

            if "faculty" in query or "staff" in query:
                return self.clean_response(dept_data.get("teaching-staff"))

            if "achievement" in query:
                return self.trim_response(dept_data.get("achivements"))

            # FIX: If branch mentioned with research → treat as department
            if intent == "research" and entities.get("branch"):
                intent = "departments"
                print("FINAL INTENT:", intent)

            if "research" in query:
                return self.trim_response(dept_data.get("research-and-consultancy"))

            return self.trim_response(dept_data.get("about"))

        # ----------------------------------------
        # PLACEMENTS
        # ----------------------------------------
        if intent == "placements":

            placements_data = load_placements()

            if not placements_data:
                return "Placements information not available."

            if "recruit" in query:
                recruiters = placements_data.get("recruiters", [])

                if not recruiters:
                    return "Recruiters information not available."

                return "🏢 Major Recruiters:\n\n" + ", ".join(recruiters)

            elif "year" in query:
                return self.format_yearwise_placements(
                    placements_data.get("year_wise")
                )

            elif "contact" in query:
                return self.format_placement_contacts(
                    placements_data.get("contacts")
                )

            else:
                return self.trim_response(
                    placements_data.get("about")
                )

        # ----------------------------------------
        # RESEARCH & DEVELOPMENT
        # ----------------------------------------
        if intent == "research":

            rnd_data = load_rnd()

            if not rnd_data:
                return "R&D information not available."

            if "newgen" in query or "iedc" in query:
                return self.trim_response(rnd_data.get("newgen_iedc"))

            elif "excellence" in query:
                return self.trim_response(rnd_data.get("centre_of_excellence"))

            elif "idea lab" in query or "aicte" in query:
                return self.trim_response(rnd_data.get("aicte_idea_lab"))

            else:
                return self.trim_response(rnd_data.get("rd_cell"))

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
                return self.format_club_response(clubs_data.get("radio_club"))

            elif "coder" in query_lower:
                return self.format_club_response(clubs_data.get("coders_club"))

            elif "creator" in query_lower:
                return self.format_club_response(clubs_data.get("creators_club"))

            elif "cultural" in query_lower:
                return self.format_club_response(clubs_data.get("cultural_club"))

            elif "eco" in query_lower:
                return self.format_club_response(clubs_data.get("eco_club"))

            elif "fitness" in query_lower:
                return self.format_club_response(clubs_data.get("fitness_club"))

            elif "gamer" in query_lower:
                return self.format_club_response(clubs_data.get("gamers_club"))

            elif "handler" in query_lower or "robo" in query_lower:
                return self.format_club_response(clubs_data.get("handlers_club"))

            elif "literary" in query_lower or "fine arts" in query_lower:
                return self.format_club_response(clubs_data.get("literary_club"))

            elif "multimedia" in query_lower or "trinetra" in query_lower:
                return self.format_club_response(clubs_data.get("multimedia_club"))

            elif "nss" in query_lower:
                return self.format_club_response(clubs_data.get("nss_club"))

            elif "sport" in query_lower:
                return self.format_club_response(clubs_data.get("sports_club"))

            elif "women" in query_lower or "sheinspires" in query_lower:
                return self.format_club_response(clubs_data.get("womens_club"))

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

    

    def trim_response(self, text, max_lines=3):

        if not text:
            return "Information not available."

        # First clean junk
        text = self.clean_response(text)

        lines = text.split("\n")
        meaningful_lines = []

        for line in lines:
            line = line.strip()

            # Ignore short headers like "About Department"
            if len(line) < 40:
                continue

            # Ignore navigation-like junk
            lower_line = line.lower()
            if (
                "academicsadmissions" in lower_line or
                "privacy policy" in lower_line or
                "nptel" in lower_line or
                "naac" in lower_line or
                "nirf" in lower_line or
                "today" in lower_line or
                "yesterday" in lower_line or
                "download brochure" in lower_line or
                "full name" in lower_line or
                "submit" in lower_line or
                "gallery" in lower_line or
                "enquiry" in lower_line
            ):
                continue

            meaningful_lines.append(line)

        if not meaningful_lines:
            return text

        return "\n\n".join(meaningful_lines[:max_lines])
    


    def format_admission_procedure(self, text):

        if not text:
            return "Admission procedure not available."

        # Clean navigation junk first
        text = self.clean_response(text)

        # Split based on numbering "2."
        parts = text.split("2.")

        # If both parts exist (Regular + Lateral Entry)
        if len(parts) >= 2:

            regular = parts[0].strip()
            lateral = "2." + parts[1].strip()

            return (
                "🔹 B.Tech Admission (4-Year Program):\n\n"
                f"{regular}\n\n"
                "🔹 Lateral Entry (Diploma Holders):\n\n"
                f"{lateral}"
            )

        # Fallback
        return text



    def format_yearwise_placements(self, year_data):

        if not year_data:
            return "Year-wise placement data not available."

        table = year_data.get("table_1", {})
        rows = table.get("rows", [])

        if not rows:
            return "Year-wise placement data not available."

        response = "📊 Year-wise Placement Offers:\n\n"

        for row in rows:
            year = row[1]
            offers = row[2]
            response += f"• {year} → {offers}\n"

        return response
    


    def format_placement_contacts(self, text):

        if not text:
            return "Placement contact information not available."

        text = self.clean_response(text)
        lines = text.split("\n")

        response = "📞 Training & Placement Contacts\n\n"

        i = 0
        total = len(lines)

        # -------------------------
        # 1️⃣ Core Officers
        # -------------------------
        response += "🔹 Core Officers:\n\n"

        while i < total:

            if (
                "Head - Corporate Relations" in lines[i]
                or "Training & Placement Officer" in lines[i]
            ):

                try:
                    name = lines[i - 2]
                    department = lines[i - 1]
                    designation = lines[i]
                    mobile = lines[i + 1]
                    email = lines[i + 2]

                    response += (
                        f"Name: {name}\n"
                        f"Designation: {designation}\n"
                        f"Mobile: {mobile}\n"
                        f"Email: {email}\n\n"
                    )

                except IndexError:
                    pass

            i += 1


        # -------------------------
        # 2️⃣ Placement Team Members
        # -------------------------
        response += "🔹 Placement Team Members:\n\n"

        i = 0
        while i < total:

            if "Member" in lines[i] or "Placement Assistant" in lines[i]:

                try:
                    name = lines[i - 2]
                    designation = lines[i]
                    mobile = lines[i + 1]
                    email = lines[i + 2]

                    response += (
                        f"Name: {name}\n"
                        f"Role: {designation}\n"
                        f"Mobile: {mobile}\n"
                        f"Email: {email}\n\n"
                    )

                except IndexError:
                    pass

            i += 1


        # -------------------------
        # 3️⃣ Student Coordinators
        # -------------------------
        response += "🔹 Student Coordinators:\n\n"

        i = 0
        while i < total:

            # Detect student rows by Roll Number pattern
            if lines[i].startswith("23N81A"):

                try:
                    roll = lines[i]
                    name = lines[i + 1]
                    mobile = lines[i + 2]
                    branch = lines[i + 3]
                    email = lines[i + 4]

                    response += (
                        f"Name: {name} ({branch})\n"
                        f"Mobile: {mobile}\n"
                        f"Email: {email}\n\n"
                    )

                except IndexError:
                    pass

            i += 1

        return response
    



    def format_club_response(self, text):

        if not text:
            return "Information not available."

        text = self.clean_response(text)
        lines = text.split("\n")

        cleaned = []

        junk_keywords = [
            "Student Clubs",
            "Accredited by",
            "+91",
            "NCC",
            "AICTE Idea Lab",
            "Home -",
            "Download Brochure",
            "Full Name",
            "Submit",
            "Enquiry",
            "Alumni"
        ]

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Remove junk header lines
            if any(junk in line for junk in junk_keywords):
                continue

            # Remove extremely short meaningless lines
            if len(line) < 3:
                continue

            cleaned.append(line)

        # Remove duplicate consecutive lines
        final_output = []
        prev = ""
        for line in cleaned:
            if line != prev:
                final_output.append(line)
            prev = line

        # Limit output to first 60 meaningful lines
        return "\n".join(final_output[:60])