
from setuptools import setup, find_packages

setup(
    name="orange-mcp-wikidata",
    version="0.1.0",
    description="MCP Wikidata Server",
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
    install_requires=['mcp[cli]>=1.4.1', 'httpx>=0.28.1'],
    keywords=["orange"] + [],
)
