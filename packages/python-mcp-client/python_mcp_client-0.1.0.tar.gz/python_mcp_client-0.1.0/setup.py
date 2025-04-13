from setuptools import setup, find_packages

setup(
    name="python-mcp-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=0.0.1",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.1",
        "langchain-mcp-adapters>=0.0.1",
        "langgraph>=0.0.1",
        "flask>=2.0.0",
    ],
)

