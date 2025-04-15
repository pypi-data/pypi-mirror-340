
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-aws-resources",
    version="0.1.0",
    description="MCP server for AWS resources using boto3",
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
    install_requires=['boto3', 'mcp', 'pydantic', 'pytz'],
    keywords=["orange"] + [],
)
