from setuptools import setup, find_packages
import os

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="custom-terminal",
    version="0.1.6",
    author="Harmandeep Singh",
    author_email="haricomputer4216@gmail.com",
    description="A custom terminal with weather commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HarmandeepSinghDhillon/Custom-terminal",
    packages=find_packages(include=['custom_terminal', 'custom_terminal.*']),
    package_data={
        'custom_terminal': ['*'],
        'custom_terminal.commands': ['*']
    },
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'cterm=custom_terminal.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)