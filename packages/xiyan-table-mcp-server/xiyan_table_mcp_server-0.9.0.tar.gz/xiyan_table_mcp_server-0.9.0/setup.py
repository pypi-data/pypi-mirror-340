# setup.py
from setuptools import setup, find_packages

setup(
    name="xiyan_table_mcp_server",
    version="0.9.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "httpx>=0.28.1",
        "mcp[cli]>=1.2.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0.0",
        "openai",
        "dashscope"
    ],
    entry_points={
        "console_scripts": [
            "server=xiyan_table_mcp_server.server:main",
        ],
    },
    author="Shixiaorong",
    author_email="shixiaorong.sxr@alibaba-inc.com",
    description="A Model Context Protocol (MCP) server that allows AI assistants to display table contents and perform natural language queries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xiyan_table_mcp_server",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
)
