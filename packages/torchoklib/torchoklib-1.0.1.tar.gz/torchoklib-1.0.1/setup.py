from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="torchoklib",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=2.1.3'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)