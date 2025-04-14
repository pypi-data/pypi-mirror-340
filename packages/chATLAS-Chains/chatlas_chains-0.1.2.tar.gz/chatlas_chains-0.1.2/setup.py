from setuptools import setup, find_packages

setup(
    name="chATLAS_Chains",
    version="0.1.2",
    description="A modular Python package for implementing Retrieval Augmented Generation chains for the chATLAS project.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Joe Egan",
    author_email="joseph.caimin.egan@cern.ch",
    url="https://gitlab.cern.ch/belliot/chatlas-packages/",
    project_urls={
        "Documentation": "https://chatlas-packages.docs.cern.ch/chATLAS_Chain/"
    },
    packages=find_packages(),
    install_requires=[
        "chATLAS_Benchmark",
        "chATLAS_Embed>=0.1.14",
        "langchain~=0.3.3",
        "langchain_core",
        "langchain_openai",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
