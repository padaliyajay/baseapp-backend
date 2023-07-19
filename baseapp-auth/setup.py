from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="baseapp-auth",
    packages=find_packages(),
    version="0.3",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
