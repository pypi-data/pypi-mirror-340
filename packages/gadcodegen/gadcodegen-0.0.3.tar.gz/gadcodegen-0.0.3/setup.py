from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gadcodegen",
    version="0.0.3",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gadcodegen=gadcodegen.cli:app",
        ],
    },
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="A fast code generator CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gadcodegen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)