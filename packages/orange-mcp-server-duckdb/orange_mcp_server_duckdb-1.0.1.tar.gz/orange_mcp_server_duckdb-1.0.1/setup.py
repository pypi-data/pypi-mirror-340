
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-duckdb",
    version="1.0.1",
    description="A DuckDB MCP server",
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
    install_requires=['duckdb>=1.1.3', 'mcp>=1.0.0'],
    keywords=["orange"] + [],
)
