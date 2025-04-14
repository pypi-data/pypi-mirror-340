from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ChemInformant",
    version="1.1.0", 
    author="Ang",
    author_email="ang@hezhiang.com",
    # Updated description
    description="A Python library to easily retrieve chemical compound information from PubChem.",
    long_description=long_description, # Use the content read from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/HzaCode/ChemInformant", # Make sure this URL is correct
    packages=find_packages(where="src"), # Finds your package in src/
    package_dir={"": "src"}, # Specifies that packages are under src/
    install_requires=[
        "requests>=2.31.0" # Dependency needed for making API calls
    ],
    python_requires=">=3.6", # Minimum Python version requirement
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License", # Your chosen license
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # Updated keywords
    keywords="chemistry pubchem api cheminformatics chemical compound information",
)