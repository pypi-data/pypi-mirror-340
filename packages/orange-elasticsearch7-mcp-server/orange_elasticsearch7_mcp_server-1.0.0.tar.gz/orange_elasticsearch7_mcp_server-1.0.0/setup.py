
from setuptools import setup, find_packages

setup(
    name="orange-elasticsearch7-mcp-server",
    version="1.0.0",
    description="MCP Server for interacting with Elasticsearch 7.x",
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
    install_requires=['elasticsearch>=7.0.0,<8.0.0', 'mcp>=1.0.0', 'python-dotenv>=1.0.0', 'fastmcp>=0.4.0'],
    keywords=["orange"] + [],
)
