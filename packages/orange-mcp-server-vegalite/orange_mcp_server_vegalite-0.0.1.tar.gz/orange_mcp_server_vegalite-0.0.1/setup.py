
from setuptools import setup, find_packages

setup(
    name="orange-mcp-server-vegalite",
    version="0.0.1",
    description="A simple Data Visualization MCP server using Vega-Lite",
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
    install_requires=['mcp>=1.0.0', 'vl-convert-python'],
    keywords=["orange"] + [],
)
