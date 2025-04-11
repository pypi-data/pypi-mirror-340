from setuptools import setup, find_packages

# Read the README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pdf_highlight_extractor",  
    version="0.1.1",
    description="Extract and summarize highlights from PDF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anish Bala Sachin",
    author_email="sachinabs.js@gmail.com",
    url="https://github.com/sachinabs/pdf_highlight_extractor",  # Optional: update with real GitHub URL
    packages=find_packages(),
    install_requires=[
        "PyMuPDF>=1.22.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    keywords="pdf highlights extraction annotation pymupdf research notes text",
    python_requires=">=3.7",
    include_package_data=True,
)
