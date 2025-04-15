
from setuptools import setup, find_packages

setup(
    name="orange-mcp-obsidian",
    version="0.2.1",
    description="MCP server to work with Obsidian via the remote REST plugin",
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
    install_requires=['mcp>=1.1.0', 'python-dotenv>=1.0.1', 'requests>=2.32.3'],
    keywords=["orange"] + [],
)
