
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-ipinfo",
    version="0.1.0",
    description="IP Geolocation Server for MCP",
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
    install_requires=['ipinfo>=5.1.1', 'mcp>=1.2.1', 'pydantic>=2.10.6'],
    keywords=["orange"] + [],
)
