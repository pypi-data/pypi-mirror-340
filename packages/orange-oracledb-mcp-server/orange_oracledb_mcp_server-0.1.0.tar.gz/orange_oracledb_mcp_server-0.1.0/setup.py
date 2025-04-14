
from setuptools import setup, find_packages

setup(
    name="orange-oracledb-mcp-server",
    version="0.1.0",
    description="MCP Server For Oracle Database",
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
    install_requires=['mcp[cli]>=1.5.0', 'oracledb>=3.0.0', 'pandas>=2.2.3', 'python-dotenv>=1.0.1', 'sqlalchemy>=2.0.39'],
    keywords=["orange"] + [],
)
