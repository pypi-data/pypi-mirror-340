from pdfminer.high_level import extract_text
import spacy


from .basic_details import extract_contact_number, extract_name, extract_email
from .skills import extract_skills
from .education import extract_education
from .company_name import extract_company_names, extract_total_experience
from .designation import extract_section_designations
from .constants import skills_list, designations_list, company_suffixes

# spacy pdfminer.six

class ResumeParser:
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.text = extract_text(self.resume_path)
        self.nlp = spacy.load('en_core_web_sm')
        self.skills_list = skills_list
        self.designations_list = designations_list
        self.company_suffixes = company_suffixes
    
    def extract_all(self):
        return {
            "name": extract_name(self.nlp, self.text),
            "contact_number": extract_contact_number(self.text),
            "email": extract_email(self.text),
            "skills": extract_skills(self.text, self.skills_list, ["EXPERIENCE", "PROJECTS"]),
            "degree": extract_education(self.text).get("degree"),
            "college_names": extract_education(self.text).get("college_names"),
            "companies": extract_company_names(self.text, self.designations_list, self.company_suffixes, ["EXPERIENCE", "WORK EXPERIENCE"]),
            "designations": extract_section_designations(self.text, self.designations_list, ["EXPERIENCE", "WORK EXPERIENCE"]),
            "total_experience": extract_total_experience(self.text, ["EXPERIENCE", "WORK EXPERIENCE"])
        }

# TODO: Extract the current work location of the user