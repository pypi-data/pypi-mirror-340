from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="valuevec",
    version="0.1.0",
    author="Ronald Doku",
    author_email="ronjeffdoku@gmail.com",
    description="Value-driven word embeddings that incorporate external continuous values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdoku/valuevec",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torch>=1.7.0",
        "pandas>=1.0.0",
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "scikit-learn>=0.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "flake8>=3.8.0",
            "black>=20.8b1",
            "isort>=5.0.0",
            "sphinx>=3.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "twine>=3.2.0",
            "build>=0.3.0",
        ],
    },
)