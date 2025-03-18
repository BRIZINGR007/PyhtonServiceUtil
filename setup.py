from setuptools import setup, find_packages

# Read requirements from the file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Read the README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="zoldics_service_utils",
    version="0.1.15",
    author="Nabarka_Deb",
    description="A most utile package for the governance of pythonic micro-services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/BRIZINGR007/PyhtonServiceUtil",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    install_requires=requirements,
    extra_require={"dev": ["pytest>=7.0", "twine>=4.0.2"]},
    python_requires=">=3.11",
)
