from setuptools import setup, find_packages

setup(
    name="qasi",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["requests", "transformers", "spacy", "pdfminer.six"],
    author="Prasanna Gramopadhye",
    author_email="gramopadhye37@gmail.com",
    description="AI assistant for answering job application questions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Job-automation/qas.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
