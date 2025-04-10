import requests
import re
from typing import List

def get_answers_from_model(context: str, questions: List[str], url: str, model_name: str, answer_length = '2-3') -> List[str]:
    headers = {
        "Content-Type": "application/json"
    }
    
    question_block = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent job applying assistant helping a candidate apply for jobs."
                "Given a context about a candidate and a list of questions in order."
                f"Context:\n{context}\n\n"
                f"Respond concisely in {answer_length} words per answer, with numbered responses."
                "If you don't find answer to a question answer with a positive response."
                "If no information is provided answer with a out of context information."
                "return ONLY short, direct answers as a numbered list. "
                "Do NOT include any explanation, do NOT repeat the question, and do NOT show thinking process. "
                "Output format must be:\n"
                "1. <answer to question 1>\n2. <answer to question 2>\n..."
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Questions:\n{question_block}\n\n"
                "Please return the answers in the following format ONLY:\n"
                "1. Guido van Rossum\n2. 1991\n3. Yes\n\n"
                "Do not repeat the questions. Do not include any explanations or reasoning."
            )
        }
    ]
    
    results = []
    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        raw_text = clean_raw_text(answer.strip())
        
        answer_lines = raw_text.split("\n")
        # Converting raw_text into an array
        answers = []
        for line in answer_lines:
            match = re.match(r"^\s*\d+\.\s*(.*)", line)
            if match:
                answers.append(match.group(1).strip())

        return clean_answers(answers)
    
    except Exception as e:
        results.append(f"Error: {e}")
    
    return results

def clean_answers(raw_answers: List[str]) -> List[str]:
    cleaned = []
    for ans in raw_answers:
        # Remove <answer> tags if they exist
        match = re.search(r"<answer>(.*?)</answer>", ans, re.DOTALL | re.IGNORECASE)
        if match:
            ans = match.group(1)
        
        ans = ans.strip()
        cleaned.append(ans)
    return cleaned

def clean_raw_text(raw_text: str) -> str:
    return re.sub(r"<think>.*?</think>\s*", "", raw_text, flags=re.DOTALL | re.IGNORECASE)