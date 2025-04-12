from setuptools import setup, find_packages

setup(
    name="tursor",
    version="0.1",
    description="cursor ka bhai",
    author="Krishav",
    py_modules=["tursor"],
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "tursor=tursor:cli",
        ],
    },
)