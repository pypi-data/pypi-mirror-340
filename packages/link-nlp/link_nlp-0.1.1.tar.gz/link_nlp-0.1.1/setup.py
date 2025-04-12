from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    
setup(
    name="link_nlp",
    version="0.1.1",
    author="Unibo NLP Group",
    author_email="nlp@disi.unibo.it",  
    description="A Python package for legal text processing and information retrieval",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/disi-unibo-nlp/link_nlp", 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
) 