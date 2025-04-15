
from setuptools import setup, find_packages

setup(
    name="orange-biomart-mcp",
    version="0.1.0",
    description="A MCP server for Biomart",
    author="orange",
    author_email="support@orange.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp[cli]>=1.3.0', 'pybiomart>=0.2.0'],
    keywords=["orange"] + [],
)
