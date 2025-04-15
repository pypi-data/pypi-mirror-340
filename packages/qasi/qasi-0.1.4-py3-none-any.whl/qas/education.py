import re
from typing import List, Dict

def extract_education(text) -> Dict[str, List[str]]:
    degree_pattern = r"(?i)(?:B\.Tech|B\.E|B\.Sc|B\.A|B\.Com|M\.Tech|M\.E|M\.Sc|M\.A|Ph\.D|Diploma|Bachelors|Master(?:'s)?|Bachelor(?:'s)?|HSC|SSC)\s*(?:\w+\s*)*\w+\s*\d*"
    degree_matches = re.findall(degree_pattern, text)
    education = [re.sub(r'\d', '', m).replace('\n', '').strip() for m in degree_matches]
    
    pattern = re.compile(
        r"([A-Z][\w’'.\-& ]{0,100}?(College|University|Institute)[\w’'.\-& ]{0,100})",
        re.IGNORECASE
    )

    matches = pattern.findall(text)
    
    college_names = [match[0].strip() for match in matches]
    
    return {
        "degree": education,
        "college_names": college_names
    }