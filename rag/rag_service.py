from pathlib import Path

ROOT = Path(__file__).resolve().parent

KB_FILE = ROOT / "knowledge_base.txt"


def retrieve_information(attack_name):

    with open(KB_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    sections = content.split("---------------------------------------------------")

    for section in sections:

        if attack_name in section:
            return section.strip()

    return "No information available."