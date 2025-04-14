from setuptools import setup, find_packages
import os

# Read the contents of README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Get version from __init__.py
with open(os.path.join('linko_mcp', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break
    else:
        version = '0.2.0'  

setup(
    name="linko-mcp",
    version=version,
    author="Tianqi",
    author_email="tianqijiang.dec@gmail.com",
    description="Linko MCP - Access your Linko study notes and resources through LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tianqijiang/linko_mcp",
    project_urls={
        "Bug Tracker": "https://github.com/tianqijiang/linko_mcp/issues",
        "Documentation": "https://github.com/tianqijiang/linko_mcp",
        "Source Code": "https://github.com/tianqijiang/linko_mcp",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "."},
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "mcp[cli]>=1.6.0",
        "requests>=2.31.0",
        "httpx>=0.24.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-linko=linko_mcp.linko_mcp:main",
            "mcp-server-linko-for-ai=linko_mcp.linko_for_AI:main",
        ],
    },
) 