
from setuptools import setup, find_packages

setup(
    name="agentverse-ai",
    version="0.3.0",
    author="Emmanuel Ebekue",
    author_email="ebekue525@gmail.com",
    description="A lightweight but powerful library for building (AI) multimodal agents with memory, tools, and knowledge.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://agentversai.app/",
    packages=find_packages(),
    install_requires=[
        "openai",
        "duckduckgo-search",
        "lancedb",
        "tantivy",
        "pypdf",
        "yfinance"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
