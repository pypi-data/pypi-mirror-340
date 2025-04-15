
from setuptools import setup, find_packages

setup(
    name="orange-mcp-llm-bridge",
    version="0.1.0",
    description="Bridge between MCP protocol and LLM clients",
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
    install_requires=['mcp>=1.0.0', 'openai>=1.0.0', 'python-dotenv>=0.19.0', 'pydantic>=2.0.0', 'asyncio>=3.4.3', 'aiohttp>=3.8.0', 'typing-extensions>=4.0.0', 'colorlog>=6.9.0'],
    keywords=["orange"] + [],
)
