from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="r3alai",
    version="0.1.1",
    description="A Python library for Random Set Neural Networks with uncertainty estimation",
    author="Arshia",
    author_email="arshia@r3al.ai",
    packages=find_packages(),  # This will find the r3alai directory and all its subdirectories
    install_requires=[
        "torch>=1.7.0",
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
    ],
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)