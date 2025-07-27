"""
Setup script for JAEGIS Claude Code Integration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jaegis-claude-code",
    version="1.0.0",
    author="JAEGIS Core Team",
    author_email="team@jaegis-method.com",
    description="JAEGIS Method integration for Claude Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaegis-method/claude-code-integration",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "server": [
            "aiohttp>=3.8.0",
            "uvloop>=0.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jaegis-mcp=jaegis_claude_code.cli:main",
            "jaegis-mcp-server=jaegis_claude_code.server:start_server",
        ],
    },
    include_package_data=True,
    package_data={
        "jaegis_claude_code": [
            "templates/*.yaml",
            "templates/*.md",
            "config/*.json",
        ],
    },
)
