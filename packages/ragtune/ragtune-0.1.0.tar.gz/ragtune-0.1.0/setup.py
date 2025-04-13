from setuptools import setup, find_packages

setup(
    name="ragtune",
    version="0.1.0",
    description="A Pseudo-Finetuning RAG Framework",
    author="Joshikaran K",
    author_email="joshikaran2002@gmail.com",
    url="https://github.com/Joshikarank/ragtune",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "sentence-transformers",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "ragtune = ragtune.core:cli_entry"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
