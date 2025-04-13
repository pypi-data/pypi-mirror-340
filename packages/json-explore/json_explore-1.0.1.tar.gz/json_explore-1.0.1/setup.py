from setuptools import setup, find_packages

setup(
    name="json-explore",
    version="1.0.1",
    author="Matthew Raburn",
    description="A package for searching through JSONs via CLI",
    packages=find_packages(),
    py_modules=["json_cli"],  # The name of the Python file without .py
    install_requires=[],  # Add dependencies here if needed
    entry_points={
        "console_scripts": [
            "json-explore=json_cli:json_explore",  # CLI command
        ],
    },
    python_requires='>=3.6',
)