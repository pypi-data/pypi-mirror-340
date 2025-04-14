from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join("apostrofo_models_sdk", "__init__.py"), encoding="utf-8") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

# Read long description from README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="apostrofo-models-sdk",
    version=version,
    description="Python SDK for the Apostrofo Models API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Apostrofo AI",
    author_email="apostrofoai@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="ai, api, sdk, machine learning, nlp, apostrofo",
)