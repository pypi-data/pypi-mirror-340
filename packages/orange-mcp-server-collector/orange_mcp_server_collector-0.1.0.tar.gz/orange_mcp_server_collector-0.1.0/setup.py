
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-collector",
    version="0.1.0",
    description="A MCP Server used to collect MCP Servers over the internet.",
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
    install_requires=['aiohttp>=3.11.10', 'mcp>=1.1.0', 'openai>=1.57.0', 'python-dotenv>=1.0.1', 'requests>=2.32.3'],
    keywords=["orange"] + [],
)
