from setuptools import setup, find_packages

setup(
    name="datalitex",  # Your package name on PyPI
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Datalitex: A smart data assistant for data analysts and scientists — clean, transform, visualize and analyze datasets with ease.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/datalitex",  # Replace with your repo URL
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.0.0",
        "seaborn>=0.10.0",
        "scikit-learn>=0.22.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
)
