# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="textops_api_v1",
    version='0.1.85',
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Python client for TextOps transcription API",
    long_description=long_description,
    long_description_content_type="text/markdown",  # חשוב!
    keywords="transcription, speech-to-text, api",
    url="https://your-company-website.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)


