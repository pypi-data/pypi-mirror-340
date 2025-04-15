
from setuptools import setup, find_packages

setup(
    name="orange-dappier-mcp",
    version="0.2.4",
    description="An MCP server for interacting with Dappier's RAG models",
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
    install_requires=['dappier>=0.3.3', 'mcp[cli]>=1.2.1', 'pydantic>=2.10.2'],
    keywords=["orange"] + ['http', 'mcp', 'llm'],
)
