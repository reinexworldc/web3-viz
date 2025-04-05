from setuptools import setup, find_packages

setup(
    name="web3viz",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "networkx",
        "requests",
    ],
    author="reinex",
    description="Library for Ethereum blockchain data visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/reinexworldc/web3viz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
