# from qas.core import get_answers_from_model

# industry = "IT/Software"
# tech_experience = 5
# react_experience = 4
# node_experience = 3
# python_experience = 4
# tools_known = "Docker, Git, Postman"
# languages_known = "JavaScript, TypeScript, Python"
# databases_known = "MongoDB, Postgres"
# frontend_libraries = "Zustand, Redux, Material UI, Mantine"
# backend_libraries = "Express, FastAPI, Django"
# degree = "Bachelor's Degree"
# major = "Computer Science"
# university_name = "XYZ University"
# certifications = "AWS Certified Developer, MongoDB Certified Developer"
# location = "Bangalore, India"
# preferred_location = "Pune, India"
# relocation_comfortable = "comfortable"
# authorization_status = "legally"
# country = "India"
# visa_sponsorship_required = "do not"
# languages_spoken = "English and Hindi"
# availability = "immediately"

# context_text = f"""
# I am a Full-stack Developer. 
# I have {tech_experience} years of experience in {industry} Industry.
# I know languages like {languages_known}.
# I know tools like {tools_known}.
# I know databases like {databases_known}.
# I know frontend libraries like {frontend_libraries}.
# I know backend libraries like {backend_libraries}.
# I know tools like {tools_known}.
# I have a {degree} in {major} from {university_name} University.
# I have {react_experience} years of experience in React.
# I have {node_experience} years of experience in Node.
# I have {python_experience} years of experience in Python.
# My current work location is {location}.
# My preferred work location is {preferred_location}.
# I am {availability} available.
# I am fluent in {languages_spoken}.
# """
# questions = [
# #   "How many years of work experience do you have using React?",
# #   "How many years of experience do you have in IT?",
# #   "Do you have experience with Go?",
#   "What is your level of proficiency in React?",
#   "Do you have the following license or certification: AWS Certification?",
#   "Have you completed the following level of education: Bachelor's Degree?",
#   "Are you legally authorized to work in India?",
# #   "Will you now or in the future require sponsorship for employment visa status (e.g., H-1B visa status)?",
# #   "We must fill this position urgently. Can you start immediately?",
# #   "What is your level of proficiency in Javascript?",
# #   "Are you comfortable commuting to this job's location?",
# #   "How much years of experience do you have in React?",
# #   "What backend technologies do you know?",
# #   "What databases are you familiar with?",
# #   "How many years of experience do you have in tech?"
# ]
# url = "http://localhost:1234/v1/chat/completions"
# model = "deepseek-r1-distill-qwen-1.5b"

# answers = get_answers_from_model(context_text, questions, url, model)
# print(answers)
# for q, a in zip(questions, answers):
#     print(f"Q: {q}\nA: {a}\n")