
from setuptools import setup, find_packages

setup(
    name="orange-raccoonai-mcp-server",
    version="0.0.1",
    description="A MCP server for Raccoon AI LAM API",
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
    install_requires=['mcp[cli]>=1.3.0', 'raccoonai>=0.1.0a10'],
    keywords=["orange"] + [],
)
