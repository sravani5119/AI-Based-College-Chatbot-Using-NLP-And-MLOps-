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
