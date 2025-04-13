from setuptools import setup, find_packages

setup(
    name='rjfinance',
    version='0.1.0',
    description='A package for stock pattern extraction and matching using cosine similarity',
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
