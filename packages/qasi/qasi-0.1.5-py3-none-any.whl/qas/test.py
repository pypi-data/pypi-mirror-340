from nlp import QuestionAnsweringNLP

t = QuestionAnsweringNLP()

questions = [
  "How many years of work experience do you have using React?",
  "How many years of experience do you have in IT?",
  "Do you have experience with Go?",
  "What is your level of proficiency in React?",
  "Do you have the following license or certification: AWS Certification?",
  "Have you completed the following level of education: Bachelor's Degree?",
  "Are you legally authorized to work in India?",
  "Will you now or in the future require sponsorship for employment visa status (e.g., H-1B visa status)?",
  "We must fill this position urgently. Can you start immediately?",
  "What is your level of proficiency in Javascript?",
  "Are you comfortable commuting to this job's location?",
  "How much years of experience do you have in React?",
  "What backend technologies do you know?",
  "What databases are you familiar with?",
  "How many years of experience do you have in tech?"
]

temp = {
    "industry": "Software Industry",
    "preferred_location": "Pune",
    "current_work_location": "Chennai"
}

answers = t.answer("sample2.pdf", temp, questions)

for q, a in zip(questions, answers):
    print(f"Q: {q}\nA: {a}\n")