
from setuptools import setup, find_packages

setup(
    name="orange-mcp-email-client",
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
    install_requires=['asyncio>=3.4.3', 'imapclient>=3.0.1', 'mcp[cli]>=1.3.0', 'pydantic>=2.10.6'],
    keywords=["orange"] + [],
)
