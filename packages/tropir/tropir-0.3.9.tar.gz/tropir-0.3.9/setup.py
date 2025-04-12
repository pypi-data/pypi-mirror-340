from setuptools import setup, find_packages

setup(
    name="tropir",
    version="0.3.9",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "tropir=tropir.cli:main",
        ],
    },
    author="Tropir",
    author_email="info@tropir.ai",
    description="A thin client for tracking OpenAI API calls",
    long_description=open("README.md").read() if open("README.md", "a").close() or True else "",
    long_description_content_type="text/markdown",
    url="https://tropir.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 