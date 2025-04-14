
from setuptools import setup, find_packages

setup(
    name="orange-shotgrid-mcp-server",
    version="0.2.5",
    description="A Model Context Protocol (MCP) server implementation using fastmcp",
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
    install_requires=['fastmcp>=0.4.1', 'mcp>=1.2.0', 'uvicorn>=0.22.0', 'pydantic>=2.0.0', 'python-dotenv>=1.0.0', 'platformdirs>=4.1.0', 'aiohttp>=3.9.0', 'requests>=2.31.0', 'shotgun-api3>=3.5'],
    keywords=["orange"] + ['shotgrid', 'mcp', 'server', 'api', 'Flow Production Tracking'],
)
