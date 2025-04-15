import re
from typing import List

def extract_section_designations(text, designations_list, section_titles: List[str]) -> List[str]:
    des = []
    for section_title in section_titles:
        match = re.search(
            rf"(?:{re.escape(section_title)})(.*?)(?:\n[A-Z\s]{3,}:|\n[A-Z\s]{3,}\n|EDUCATION|PROJECTS|SKILLS|SUMMARY|$)",
            text, re.IGNORECASE | re.DOTALL
        )
        section_text = match.group(1).strip() if match else ""
        temp = [des for des in designations_list if re.search(rf"\b{re.escape(des)}\b", section_text, re.IGNORECASE)]
        des = list(set(temp + des))
    return des