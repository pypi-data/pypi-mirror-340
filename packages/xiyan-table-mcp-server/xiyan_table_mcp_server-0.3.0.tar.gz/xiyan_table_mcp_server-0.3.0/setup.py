from setuptools import setup, find_packages

setup(
    name="xiyan_table_mcp_server",
    version="0.3.0",
    description="A Model Context Protocol (MCP) server that allows AI assistants to display table contents and perform natural language queries.",
    author="Xiyan Team",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.28.1",
        "mcp[cli]>=1.2.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0.0",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 