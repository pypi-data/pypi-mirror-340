
from setuptools import setup, find_packages

setup(
    name="orange-yahoo-finance-mcp",
    version="0.1.0",
    description="MCP server implementation for yahoo finance integration",
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
    install_requires=['mcp[cli]>=1.6.0', 'yfinance>=0.2.55'],
    keywords=["orange"] + [],
)
