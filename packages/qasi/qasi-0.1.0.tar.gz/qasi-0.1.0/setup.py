from setuptools import setup, find_packages

setup(
    name="qasi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Prasanna Gramopadhye",
    author_email="gramopadhye37@gmail.com",
    description="AI assistant for answering job application questions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gramo37/qas",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
