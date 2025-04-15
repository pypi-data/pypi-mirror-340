
from setuptools import setup, find_packages

setup(
    name="orange-unsplash-mcp-server",
    version="0.1.0",
    description="Add your description here",
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
    install_requires=['fastmcp>=0.4.1', 'httpx>=0.26.0', 'python-dotenv>=1.0.1'],
    keywords=["orange"] + [],
)
