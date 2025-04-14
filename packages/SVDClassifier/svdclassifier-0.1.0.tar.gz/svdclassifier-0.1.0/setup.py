from setuptools import setup, find_packages

setup(
    name="SVDClassifier",  
    version="0.1.0",  
    packages=find_packages(where="SVDC"),
    install_requires=[
        "numpy",          
        "torch",     
        "cma",    
    ],
    author="Jay Nash",
    author_email="jnash1@conncoll.edu",
    description="A package for SVD-based classification tasks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ConnAALL/SVDC",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
