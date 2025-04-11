from setuptools import setup, find_packages

setup(
    name="promptlibrary_client",
    version="0.0.1",
    author="Pouya Nafisi",
    author_email="pouya@promptlibrary.com",
    description="Reserved namespace for PromptLibrary Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)