
from setuptools import setup, find_packages

setup(
    name="orange-mcp-clickhouse",
    version="0.1.5",
    description="An MCP server for ClickHouse.",
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
    install_requires=['mcp[cli]>=1.3.0', 'python-dotenv>=1.0.1', 'uvicorn>=0.34.0', 'clickhouse-connect>=0.8.0', 'pip-system-certs>=4.0'],
    keywords=["orange"] + [],
)
