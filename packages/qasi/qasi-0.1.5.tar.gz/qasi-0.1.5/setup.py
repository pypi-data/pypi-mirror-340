from setuptools import setup, find_packages

setup(
    name="qasi",
    version="0.1.5",
    packages=find_packages(),
    install_requires=["requests==2.32.3", "transformers==4.51.3", "spacy==3.8.5", "pdfminer.six==20250327", "tf_keras==2.19.0", "tensorflow==2.19.0", "torch==2.6.0"],
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
