from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Relase Notes
release_notes = """
# Relase Notes

## 2.0.0 (Current)
- now works in the command line
- improved setup.py for pypi discriptions
- added more detailed README
"""

# Combine README and release notes
full_description = long_description + "\n\n" + release_notes

setup(
    name="json-explore",
    version="2.0.1",
    author="Matthew Raburn",
    description="A lightweight CLI tool for interactively exploring JSON files and dictionaries.",
    long_description=full_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlraburn/json-CLI",
    project_urls={
        "Source Code": "https://github.com/mlraburn/json_CLI",
    },
    packages=find_packages(),
    py_modules=["json_explore"],  # The name of the Python file without .py
    install_requires=[],  # Add dependencies here if needed
    entry_points={
        "console_scripts": [
            "json-explore=json_explore:json_explore",  # CLI command
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)