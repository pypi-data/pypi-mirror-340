from setuptools import setup

setup(
    name="custom-terminal",
    version="0.1.0",
    packages=["custom_terminal"],
    install_requires=["requests"],
    entry_points={
        'console_scripts': ['cterm=custom_terminal.main:main'],
    },
)