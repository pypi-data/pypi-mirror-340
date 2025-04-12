from setuptools import setup, find_packages

setup(
    name="tropir",
    version="0.4.4",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "openai>=1.0.0",
        "anthropic>=0.35.0",
        "tiktoken>=1.35.0",
        "loguru>=0.6.0",
        "jsonschema>=4.17.3",
        "jsonpatch>=1.32",
        "jsonpointer>=2.3",
        
    ],
    entry_points={
        "console_scripts": [
            "tropir=tropir.cli:main",
        ],
    },
    author="Tropir",
    author_email="founders@tropir.com",
    description="A thin client for tracing LLM calls",
    long_description=open("README.md").read() if open("README.md", "a").close() or True else "",
    long_description_content_type="text/markdown",
    url="https://tropir.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 