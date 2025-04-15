
from setuptools import setup, find_packages

setup(
    name="orange-claude-tools",
    version="0.1.0",
    description="Multi-tool MCP integration for Claude",
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
    install_requires=['httpx>=0.28.1', 'mcp>=0.1.0'],
    keywords=["orange"] + [],
)
