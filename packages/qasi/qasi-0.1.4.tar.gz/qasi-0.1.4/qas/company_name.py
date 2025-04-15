import re
from typing import List
from datetime import datetime

def extract_company_names(text, designations_list, company_suffixes, section_titles: List[str]):
    for section_title in section_titles:
        match = re.search(
            rf"(?:{re.escape(section_title)})(.*?)(?:\n[A-Z\s]{3,}:|\n[A-Z\s]{3,}\n|EDUCATION|PROJECTS|SKILLS|SUMMARY|$)",
            text, re.IGNORECASE | re.DOTALL
        )
        section_text = match.group(1).strip() if match else ""
        # Looks for lines starting with a designation followed by company name
        lines = section_text.splitlines()
        companies = []
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip if line starts with designation
            if any(line.startswith(word) for word in designations_list):
                continue

            # Check if it ends with a company suffix
            if any(suffix.lower() in line.lower() for suffix in company_suffixes):
                companies.append(line)

        return list(set(companies))
    
def extract_total_experience(text, section_titles: List[str]):
    for section_title in section_titles:
        match = re.search(
            rf"(?:{re.escape(section_title)})(.*?)(?:\n[A-Z\s]{3,}:|\n[A-Z\s]{3,}\n|EDUCATION|PROJECTS|SKILLS|SUMMARY|$)",
            text, re.IGNORECASE | re.DOTALL
        )
        section_text = match.group(1).strip() if match else ""
        date_patterns = re.findall(
            r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|'
            r'Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}|[01]?\d/\d{4})',
            section_text, re.IGNORECASE
        )
        parsed_dates = []
        for d in date_patterns:
            try:
                if '/' in d:
                    parsed_dates.append(datetime.strptime(d, "%m/%Y"))
                else:
                    try:
                        parsed_dates.append(datetime.strptime(d, "%B %Y"))  # Full month
                    except:
                        parsed_dates.append(datetime.strptime(d, "%b %Y"))  # Abbreviated
            except:
                continue

        if not parsed_dates:
            return "0"
        
        end = datetime.now() if "present" in section_text.lower() else max(parsed_dates)
        start = min(parsed_dates)

        total_months = (end.year - start.year) * 12 + (end.month - start.month)
        years = total_months // 12
        months = total_months % 12

        return f"{years}.{months}"