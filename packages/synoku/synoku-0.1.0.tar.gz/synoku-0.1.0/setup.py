from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="synoku",
    version="0.1.0",
    description="Synoku CLI and SDK for managing secrets across environments.",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="Synoku",
    author_email="support@synoku.com",
    url="https://synoku.com",  # o GitHub si preferís ahora
    license="BUSL-1.1",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
