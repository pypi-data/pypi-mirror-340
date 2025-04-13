from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="CARAG",
    description="""CARAG is a python library developed to help the AI application developers, students, etc to extract the unstructured text from external sources
    for storing and searching document embeddings in a Qdrant vector database using hybrid embedding techniques. This library creates semantic cache (memory) 
    on the disk for quick retrieval. It uses open source state-of-the-art embedding models for retrieval and re-ranking""",
    version="0.0.1",
    author="Mohamed Rizwan",
    author_email="rizdelhi@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    license="GPL",
    url="https://github.com/rizwandel/Build-standard-RAG-with-Qdrant",
    python_requires='>=3.9',
)
