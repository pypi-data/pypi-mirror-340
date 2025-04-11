from setuptools import setup, find_packages

setup(
    name="sculblog",
    version="0.1.17",
    packages=find_packages(),
    install_requires=[
        "markdown",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "sculblog=sculblog.main:main",  # Changed from cli:main to main:main
        ],
    },
    author="Diego Cabello",
    description="Super Cool Utility Lightweight Blog - A minimalist blogging framework",
    python_requires=">=3.6",
)
