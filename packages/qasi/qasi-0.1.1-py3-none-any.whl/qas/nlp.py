from transformers import pipeline
from typing import List

class QuestionAnsweringNLP:
    _qa_pipeline = None  # Class variable to store the pipeline

    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        self.model_name = model_name

    def _load_model(self):
        if not QuestionAnsweringNLP._qa_pipeline:
            QuestionAnsweringNLP._qa_pipeline = pipeline("question-answering", model=self.model_name)

    def answer(self, context: str, questions: List[str]) -> List[str]:
        self._load_model()
        answers = []
        for question in questions:
            result = QuestionAnsweringNLP._qa_pipeline(question=question, context=context)
            answers.append(result['answer'])
        return answers