
from setuptools import setup, find_packages

setup(
    name="orange-shopify-py-mcp",
    version="0.1.0",
    description="A MCP server project",
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
    install_requires=['mcp>=1.3.0', 'ShopifyAPI>=1.0.0'],
    keywords=["orange"] + [],
)
