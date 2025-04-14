"""
COBOL Parser setup script.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legacylens_cobol_parser",
    version="0.1.1",
    author="Samuel Dion",
    author_email="sam94dion@gmail.com",
    description="A tool to extract information from COBOL programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam94dion/cobol-parser",
    packages=find_packages(),
    package_dir={"cobol_parser": "cobol_parser"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing-extensions>=3.7.4",
    ],
    entry_points={
        'console_scripts': [
            'legacylens_cobol_parser=cobol_parser.cli:main',
        ],
    },
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'black>=20.8b1',
            'flake8>=3.8.0',
        ],
    },
)