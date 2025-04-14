from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="module-5mlet-package",
    version="2.0.0",
    packages=find_packages(),
    description="Descrição da biblioteca Module 5MLET",
    author="Ricardo O. Trovato",
    author_email="devrictrovato@gmail.com",
    url="https://github.com/devrictrovato/postech-5mlet",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
