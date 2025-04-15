from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mycalculator121",  # Unique name
    version="0.2.0",
    author="Aman Kumar",
    author_email="amankumar536894@example.com",
    description="A simple calculator package for demonstration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amankumar536894/mycalculator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.21.0",  # Example dependency
    ],
    python_requires=">=3.6"
)

