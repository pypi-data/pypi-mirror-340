import re
from typing import List, Union, Dict

def extract_section_skills(text, skills_list, section_titles: List[str]) -> List[str]:
    skills = []
    for section_title in section_titles:
        start = text.find(section_title.upper())
        if start == -1:
            continue
        section_text = text[start:]
        temp = [skill for skill in skills_list if re.search(rf"\b{re.escape(skill)}\b", section_text, re.IGNORECASE)]
        skills = list(set(skills + temp))
    return skills

def extract_skills(text, skills_list, section_titles) -> List[str]:
    skills = [skill for skill in skills_list if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]
    other_skills = extract_section_skills(text, skills_list, section_titles)
    
    return list(set(skills + other_skills))
