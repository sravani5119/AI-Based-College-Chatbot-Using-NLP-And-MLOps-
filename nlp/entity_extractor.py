# nlp/entity_extractor.py

import re

def extract_entities(text: str):
    entities = {}

    regulation = re.findall(r"r\d{2}", text.lower())
    if regulation:
        entities["regulation"] = regulation[0].upper()

    year = re.findall(r"\b20\d{2}\b", text)
    if year:
        entities["year"] = year[0]

    branches = ["cse", "ece", "eee", "mech", "civil"]
    for branch in branches:
        if branch in text.lower():
            entities["branch"] = branch.upper()

    return entities



# nlp/entity_extractor.py

import re

def extract_entities(text: str):

    text_lower = text.lower()
    entities = {}

    # -------------------------
    # Regulation (R22, R18)
    # -------------------------
    regulation = re.findall(r"r\d{2}", text_lower)
    if regulation:
        entities["regulation"] = regulation[0].upper()

    # -------------------------
    # Academic Year (2025)
    # -------------------------
    year = re.findall(r"\b20\d{2}\b", text)
    if year:
        entities["year"] = year[0]

    # -------------------------
    # Branch
    # -------------------------
    branches = ["cse", "ece", "eee", "mech", "civil"]
    for branch in branches:
        if branch in text_lower:
            entities["branch"] = branch.upper()

    # -------------------------
    # Study Year Detection
    # -------------------------

    # Roman numeral pattern used in calendar titles
    if re.search(r"\bi\s*year\b", text_lower):
        entities["study_year"] = 1

    elif re.search(r"\bii\s*year\b", text_lower):
        entities["study_year"] = 2

    elif re.search(r"\biii\s*year\b", text_lower):
        entities["study_year"] = 3

    elif re.search(r"\biv\s*year\b", text_lower):
        entities["study_year"] = 4

    # Numeric forms users may type
    elif re.search(r"\b1(st)?\s*year\b|\bfirst\s*year\b|\b1\s*year\b", text_lower):
        entities["study_year"] = 1

    elif re.search(r"\b2(nd)?\s*year\b|\bsecond\s*year\b|\b2\s*year\b", text_lower):
        entities["study_year"] = 2

    elif re.search(r"\b3(rd)?\s*year\b|\bthird\s*year\b|\b3\s*year\b", text_lower):
        entities["study_year"] = 3

    elif re.search(r"\b4(th)?\s*year\b|\bfourth\s*year\b|\b4\s*year\b", text_lower):
        entities["study_year"] = 4

    # -------------------------
    # Semester
    # -------------------------
    sem_patterns = [
        (r"\b1\s*sem\b|\bsem\s*1\b|\b1-1\b|\b2-1\b|\b3-1\b|\b4-1\b", 1),
        (r"\b2\s*sem\b|\bsem\s*2\b|\b1-2\b|\b2-2\b|\b3-2\b|\b4-2\b", 2),
    ]

    for pattern, value in sem_patterns:
        if re.search(pattern, text_lower):
            entities["semester"] = value
            break

    return entities