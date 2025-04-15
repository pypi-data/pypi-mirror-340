
from setuptools import setup, find_packages

setup(
    name="orange-mcp-multilspy",
    version="0.1.0",
    description="MCP server that exposes Language Server Protocol functionality via multilspy",
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
    install_requires=['mcp[cli]>=1.4.1', 'multilspy>=0.0.14'],
    keywords=["orange"] + [],
)
