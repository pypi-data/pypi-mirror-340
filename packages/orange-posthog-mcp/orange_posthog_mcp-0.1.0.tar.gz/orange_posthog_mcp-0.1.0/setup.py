
from setuptools import setup, find_packages

setup(
    name="orange-posthog-mcp",
    version="0.1.0",
    description="PostHog MCP tools for annotations and project management",
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.3.0', 'python-dotenv>=1.0.1'],
    keywords=["orange"] + [],
)
