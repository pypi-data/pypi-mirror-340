from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Get requirements from requirements.txt
with open(here / "requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pandaplotdocs",
    version="0.1.0",
    description="Generates a PDF reference for essential Pandas and Matplotlib functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Anonymous",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="pandas, matplotlib, documentation, pdf, reference",
    package_dir={"": "."},  # Tell setuptools packages are under the root directory
    packages=find_packages(where="."),  # Find packages automatically
    python_requires=">=3.8, <4",
    install_requires=requirements,  # This will include all dependencies from requirements.txt
)