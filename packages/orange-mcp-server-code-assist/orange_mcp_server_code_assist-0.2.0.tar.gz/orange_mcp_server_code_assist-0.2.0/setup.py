
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-code-assist",
    version="0.2.0",
    description="MCP Code Assist Server",
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
    install_requires=['aiofiles>=24.0.0', 'gitpython>=3.1.40', 'pydantic>=2.0.0', 'click>=8.1.7', 'mcp>=1.2.0', 'xmlschema>=3.4.3'],
    keywords=["orange"] + [],
)
