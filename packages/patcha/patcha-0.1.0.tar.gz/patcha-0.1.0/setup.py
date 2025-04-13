from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="patcha",
    version="0.1.0",
    author="adarsh",
    author_email="adarsh.bulusu2015@gmail.com",
    description="A comprehensive security scanner for code repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adarshbulusu/patcha",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "semgrep",
        "bandit",
        "trufflehog",
    ],
    entry_points={
        "console_scripts": [
            "patcha=patcha.cli:main",
        ],
    },
) 