from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='rjfinance',
    version='0.1.1',
    description='A package for stock pattern extraction and matching using cosine similarity',
    long_description=long_description,
    long_description_content_type='text/markdown',  # important for markdown support on PyPI
    author='Rayjada Jyotiradityasing',
    author_email='rjyotiraditya@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
