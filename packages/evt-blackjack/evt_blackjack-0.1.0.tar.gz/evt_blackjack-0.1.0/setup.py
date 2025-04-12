from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="evt-blackjack",
    version="0.1.0",
    py_modules=["bj"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "bj = bj:main",
        ],
    },
    author="Ethan Votran",
    description="A terminal-based Blackjack trainer",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
