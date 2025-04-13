from setuptools import setup, find_packages

setup(
    name="AC12066UNO",
    version="0.1.0",
    author="Martín",
    author_email="martin.a.ac@outlook.com",  
    description="Una librería para resolver sistemas de ecuaciones lineales y no lineales en Python.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ale-0293/AC12066UNO",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    python_requires='>=3.8',
)
