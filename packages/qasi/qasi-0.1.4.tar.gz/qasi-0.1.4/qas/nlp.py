from transformers import pipeline
from typing import List
from get_context import ResumeParser
from pydantic import BaseModel

class basicDetailsBaseClass(BaseModel):
    industry: str
    preferred_location: str
    location: str
class QuestionAnsweringNLP:
    _qa_pipeline = None  # Class variable to store the pipeline

    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        self.model_name = model_name

    def _load_model(self):
        if not QuestionAnsweringNLP._qa_pipeline:
            QuestionAnsweringNLP._qa_pipeline = pipeline("question-answering", model=self.model_name)

    def create_context(self, resume_details: dict, basicDetails: dict):
        experience_lines = ", ".join(
            f"I have {resume_details['total_experience']} of experience in {skill}"
            for skill in resume_details["skills"]
        )
        
        context = f"""
        I am a {resume_details['designations'][0]} in {resume_details['companies'][0]}. 
        I have worked before in {", ".join(resume_details['companies'])}.
        I have the following degrees: {", ".join(resume_details['degree'])}.
        I have studied in colleges like {", ".join(resume_details['college_names'])}.
        {experience_lines}.
        Legally authorized to work in India - Yes.
        I have {resume_details['total_experience']} of experience in the {basicDetails['industry']}.
        My current work location is {basicDetails['current_work_location']}.
        My preferred work location is {basicDetails['preferred_location']}.
        Can you start immediately? - yes.
        """
        
        return context

    def answer(self, resume_path: str, basicDetails, questions: List[str]) -> List[str]:
        parser = ResumeParser(resume_path)
        context = self.create_context(parser.extract_all(), basicDetails)
        self._load_model()
        answers = []
        for question in questions:
            result = QuestionAnsweringNLP._qa_pipeline(question=question, context=context)
            answers.append(result['answer'])
        return answers