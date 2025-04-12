from setuptools import setup, find_packages

setup(
    name="MM23084UNO",
    version="1.0.1",
    author="Ricardo Mora",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "scipy"
    ]
)

