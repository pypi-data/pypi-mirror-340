from setuptools import setup, find_packages

setup(
    name="pdf_highlight_extractor",  
    version="0.1.0",
    description="Extract and summarize highlights from PDF files.",
    author="Anish Bala Sachin",
    author_email="sachinabs.js@gmail.com",
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
    python_requires=">=3.7",
    include_package_data=True,
)
