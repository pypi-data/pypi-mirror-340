
from setuptools import setup, find_packages

setup(
    name="orange-ghost-mcp",
    version="0.1.0",
    description="Ghost blog integration MCP server",
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
    install_requires=['httpx', 'pyjwt', 'mcp[cli]>=1.2.1', 'pytz'],
    keywords=["orange"] + [],
)
