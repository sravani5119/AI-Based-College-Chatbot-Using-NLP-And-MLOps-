from html import entities
from knowledge_base.loader import (
    load_knowledge_base,
    load_placements,
    load_rnd,
    load_clubs,
    load_academics
)


class Retriever:

    def __init__(self):
        self.kb = load_knowledge_base()

    def retrieve(self, intent, entities, user_input=None):

        query = user_input.lower().strip() if user_input else ""

        # -------------------------
        # Block conditions (FIXED)
        # -------------------------
        is_placement_query = "placement" in query or "recruit" in query
        is_club_query = "club" in query
        is_academic_query = "calendar" in query or "academic" in query
        is_admission_query = "admission" in query
        is_research_query = "research" in query or "r&d" in query

        # SAFETY: if entities is None, convert to empty dict
        if not entities:
            entities = {}
        
         # --- Override for placement contact queries ---
        if "placement" in query and "contact" in query:
            intent = "placements"

        if intent == "research" and entities.get("branch") and "research" in query:
            intent = "departments"

        print("FINAL INTENT:", intent)
        # Principal name request
        if "principal" in query and ("who" in query or "name" in query):

            principal = self.kb.get("principal")

            if principal:
                return f"Principal: {principal}"

            return "Principal information not available."
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

        

            phone_lines = "\n".join(phones)
            email_lines = "\n".join(emails)

            return (
                "📞 Contact Details\n\n"
                f"📱 Phone:\n{phone_lines}\n\n"
                f"📧 Email:\n{email_lines}\n\n"
                f"📍 Address:\n{address}"
)

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

                # -------------------------
                # FILTER BASED ON QUERY
                # -------------------------

                if isinstance(courses, dict):

                    response_lines = []

                    # 🎯 B.TECH ONLY
                    if "b.tech" in query or "btech" in query or "b tech" in query:
                        branches = courses.get("B.Tech", [])

                        response_lines.append("🎓 B.Tech Courses:\n")

                        for branch in branches:
                            response_lines.append(f"• {branch}")

                        return "\n".join(response_lines)

                    # 🎯 M.TECH ONLY
                    elif "m.tech" in query or "mtech" in query or "m tech" in query:
                        branches = courses.get("M.Tech", [])

                        response_lines.append("🎓 M.Tech Courses:\n")

                        for branch in branches:
                            response_lines.append(f"• {branch}")

                        return "\n".join(response_lines)

                    # 🎯 BOTH
                    else:
                        for degree, branches in courses.items():
                            response_lines.append(f"🎓 {degree}:\n")

                            for branch in branches:
                                response_lines.append(f"• {branch}")

                                response_lines.append("")

                        return "\n".join(response_lines).strip()

                return courses

        
        
        

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
                return "📊 Placement Details:\n\n" + self.trim_response(placements_data.get("about"))

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

            

            # -------------------------
            # 1️⃣ SPECIFIC CLUBS FIRST
            # -------------------------

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

            # -------------------------
            # 2️⃣ GENERAL CLUB LIST LAST
            # -------------------------
            elif "club" in query_lower or "clubs" in query_lower:
                return "🎯 Student Clubs:\n\n" + "\n".join(clubs_list)

            return "Please specify which club you want information about."

        # ----------------------------------------
        # ACADEMICS
        # ----------------------------------------
        if intent == "academics":

            academics_data = load_academics()

            if not academics_data:
                return "Academic information not available."

            # Academic Council
            if "council" in query:

                council_text = academics_data.get("academic_council")

                if not council_text:
                    return "Academic council information not available."

                return self.clean_response(council_text)

            # Academic Calendar
            if "calendar" in query or "academic" in query:

                calendars = academics_data.get("academic_calendars", [])

                if not calendars:
                    return "Academic calendar information not available."

                study_year = entities.get("study_year")
                requested_year = entities.get("year")

                # -----------------------------------
                # Step 1: Determine academic year
                # -----------------------------------
                if requested_year:
                    target_calendars = [
                        cal for cal in calendars
                        if requested_year in cal.get("academic_year", "")
                    ]
                else:
                    latest_year = calendars[0]["academic_year"]
                    target_calendars = [
                        cal for cal in calendars
                        if cal.get("academic_year") == latest_year
                    ]

                if not target_calendars:
                    return "Requested academic year calendar not available."

                # -----------------------------------
                # Step 2: Match study year
                # -----------------------------------
                if study_year:

                    year_map = {
                        1: "i year",
                        2: "ii year",
                        3: "iii year",
                        4: "iv year"
                    }

                    year_text = year_map.get(study_year)

                    for cal in target_calendars:

                        title = cal.get("title", "").lower()

                        if year_text in title:
                            return (
                                f"📅 {cal['title']}\n\n"
                                f"Academic Year: {cal['academic_year']}\n\n"
                                f"🔗 Calendar Link:\n{cal['link']}"
                            )

                # fallback
                cal = target_calendars[0]

                return (
                    f"📅 {cal['title']}\n\n"
                    f"Academic Year: {cal['academic_year']}\n\n"
                    f"{cal['link']}"
                )      


       
        # ----------------------------------------
        # DEPARTMENTS (FINAL FIXED)
        # ----------------------------------------
        if intent == "departments":

            departments = self.kb.get("departments", {})

            # -------------------------
            # FIND DEPARTMENT
            # -------------------------
            selected_dept = None

            if "cse" in query:
                selected_dept = "computer_science_and_engineering"

            elif "aiml" in query or "ai" in query:
                selected_dept = "cse_ai_ml"

            elif "cyber" in query or "security" in query:
                selected_dept = "cse_cyber_security"

            elif "data science" in query or "ds" in query or "data" in query:
                selected_dept = "cse_data_science"

            elif "freshman" in query:
                selected_dept = "freshman_engineering"

            elif "school of computing" in query:
                selected_dept = "school_of_computing"

            if not selected_dept:
                return "Please specify department (e.g., CSE, AIML, Data Science)."

            dept_data = departments.get(selected_dept)

            if not dept_data:
                return "Department information not available."

            # -------------------------
            # FLOW (ORDERED)
            # -------------------------

            # HOD
            if "hod" in query:
                hod = dept_data.get("hod-message")

                if not hod:
                    return "HOD information not available."

                return "👨‍🏫 HOD:\n" + hod.split("\n")[0]

            # ACHIEVEMENTS
            elif "achievement" in query:

                achievements = dept_data.get("achievements") or dept_data.get("achivements")

                if not achievements:
                    return "Achievements information not available."

                text = str(achievements)

                # -------------------------
                # SPLIT SECTIONS
                # -------------------------
                if "Student Achievements" in text:
                    faculty_part = text.split("Student Achievements")[0]
                    student_part = text.split("Student Achievements")[1]
                else:
                    faculty_part = text
                    student_part = ""

                # -------------------------
                # FORMAT OUTPUT
                # -------------------------
                response = "🏆 Department Achievements\n\n"

                # Faculty
                response += "👨‍🏫 Faculty Achievements:\n"
                faculty_lines = [l.strip() for l in faculty_part.split("\n") if len(l.strip()) > 10]

                for line in faculty_lines[:5]:
                    response += f"• {line}\n"

                # Students
                if student_part:
                    response += "\n🎓 Student Achievements:\n"
                    student_lines = [l.strip() for l in student_part.split("\n") if len(l.strip()) > 10]

                    for line in student_lines[:5]:
                        response += f"• {line}\n"

                return response

            # VISION
            elif "vision" in query or "mission" in query:
                vision = dept_data.get("vision-mission")

                if not vision:
                    return "Vision not available."

                return self.trim_response(vision)

            # FACULTY
            elif "faculty" in query or "staff" in query:

                faculty = (
                    dept_data.get("teaching-staff") or
                    dept_data.get("teaching staff") or
                    dept_data.get("faculty") or
                    dept_data.get("staff")
                )

                if not faculty:
                    return "Faculty information not available."

                # -------------------------
                # SAFE HANDLING (FIX)
                # -------------------------
                if isinstance(faculty, list):
                    lines = faculty
                else:
                    text = str(faculty)
                    lines = text.split("\n")

                clean_lines = []

                for line in lines:
                    line = str(line).strip()

                    if not line:
                        continue

                    # ❌ REMOVE JUNK LINES
                    unwanted_keywords = [
                        "academics", "admissions", "placements", "transport",
                        "gallery", "ncc", "nptel", "swayam", "naac", "nirf",
                        "infrastructure", "privacy", "policy", "today", "yesterday",
                        "sphoorthy", "sp hn", "local chapter"
                    ]

                    if any(word in line.lower() for word in unwanted_keywords):
                        continue

                    # ❌ REMOVE department titles
                    if "engineering" in line.lower():
                        continue

                    # ❌ REMOVE very long weird lines
                    if len(line) > 80:
                        continue

                    # ✅ KEEP VALID NAMES
                    clean_lines.append("• " + line)
                return "👨‍🏫 Teaching Staff:\n\n" + "\n".join(clean_lines)

            # RESEARCH
            elif "research" in query:

                research = dept_data.get("research-and-consultancy")

                if not research:
                    return "Research information not available."

                text = str(research)

                # REMOVE TABLE HEADERS
                lines = text.split("\n")
                clean_lines = []

                for line in lines:
                    line = line.strip()

                    if not line:
                        continue

                    if "Academic Year" in line:
                        continue

                    clean_lines.append(line)

                response = "🔬 Research & Consultancy:\n\n"

                for line in clean_lines[:8]:
                    response += f"• {line}\n"

                return response

            # DEFAULT → ABOUT
            else:
                about = dept_data.get("about")

                if not about:
                    return "Department information not available."

                return self.trim_response(about)

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
            if len(line) < 10:
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
    



    def format_club_response(self, club_data):

        if not club_data:
            return "Club information not available."

        text = str(club_data)

        # -------------------------
        # REMOVE JUNK LINES
        # -------------------------
        unwanted = [
            "Student Clubs", "NAAC", "SHHN", "Google Maps",
            "Alumni", "Enquiry", "Facebook", "Instagram",
            "YouTube", "Linkedin", "Gallery", "Download Brochure",
            "Submit", "Home", "Location"
        ]

        lines = text.split("\n")
        clean_lines = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if any(word.lower() in line.lower() for word in unwanted):
                continue

            clean_lines.append(line)

        text = "\n".join(clean_lines)

        # -------------------------
        # EXTRACT SECTIONS PROPERLY
        # -------------------------

        def extract_between(start, end):
            if start in text:
                part = text.split(start)[1]
                if end in part:
                    part = part.split(end)[0]
                return part.strip()
            return ""

        about = extract_between("About", "Vision")
        vision = extract_between("Vision", "Mission")
        mission = extract_between("Mission", "Objectives")

        # -------------------------
        # FORMAT OUTPUT (BALANCED)
        # -------------------------

        response = "🎯 Club Details\n\n"

        # About (clean & medium length)
        if about:
            about_lines = about.split("\n")
            clean_about = []

            for line in about_lines:
                if len(line) > 30:
                    clean_about.append(line)

            response += "📌 About:\n"
            for line in clean_about[:2]:   # only 2 good lines
                response += f"• {line}\n"
            response += "\n"

        # Vision
        if vision:
            response += "📌 Vision:\n"
            response += f"• {vision[:200]}...\n\n"

        # Mission
        if mission:
            response += "📌 Mission:\n"
            mission_lines = mission.split("\n")

            count = 0
            for line in mission_lines:
                if line.strip():
                    response += f"• {line.strip()}\n"
                    count += 1
                if count == 3:
                    break

        return response