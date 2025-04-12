from setuptools import setup, find_packages

setup(
    name="aderonke-data-structures",
    version="0.1.1",
    description="This package provides a concise overview of the custom implementations for common data structures in Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Aderonke Ajefolakemi",
    author_email="aajefolakemi@aimsammi.org",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6",
    install_requires=[],
)
