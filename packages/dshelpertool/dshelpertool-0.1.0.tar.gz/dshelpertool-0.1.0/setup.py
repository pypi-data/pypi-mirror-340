from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dshelpertool",
    version="0.1.0",
    author="Utkarsh Shashinandan Pandey",
    author_email="utkarshpandey8977@gmail.com",
    description="A lightweight helper package for data science and analysis tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/utkarsh820/dshelpertool",
    project_urls={
        "Bug Tracker": "https://github.com/utkarsh820/dshelpertool/issues",
        "Documentation": "https://github.com/utkarsh820/dshelpertool#readme",
        "Source Code": "https://github.com/utkarsh820/dshelpertool",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.1.0",
        "scipy>=1.4.0",
        "seaborn>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "flake8>=3.8.0",
            "isort>=5.0.0",
        ],
        "docs": [
            "sphinx>=3.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "nbsphinx>=0.8.0",
        ],
    },
    tests_require=[
        "pytest>=6.0.0",
        "pytest-cov>=2.10.0",
    ],
    entry_points={
        "console_scripts": [
            "dshelpertool=dshelpertool.cli:main",
        ],
    },
    keywords="data-science helper pandas numpy eda",
    license="MIT",
)
