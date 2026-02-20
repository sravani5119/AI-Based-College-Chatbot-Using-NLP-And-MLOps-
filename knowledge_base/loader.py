import json
import os


def load_knowledge_base():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kb_path = os.path.join(base_path, "data", "structured", "knowledge_base.json")

    if not os.path.exists(kb_path):
        return {}

    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_placements():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    placements_path = os.path.join(base_path, "data", "structured", "placements.json")

    if not os.path.exists(placements_path):
        return {}

    with open(placements_path, "r", encoding="utf-8") as f:
        return json.load(f)



def load_rnd():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rnd_path = os.path.join(base_path, "data", "structured", "rnd.json")

    if os.path.exists(rnd_path):
        with open(rnd_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_clubs():
    file_path = os.path.join(BASE_DIR, "data", "structured", "student_clubs.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
