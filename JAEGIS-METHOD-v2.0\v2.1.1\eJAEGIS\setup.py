"""
Setup script for JAEGIS
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = [
    "click>=8.0.0",
    "watchdog>=2.1.0",
    "neo4j>=5.0.0",
    "fastapi>=0.68.0",
    "uvicorn>=0.15.0",
    "aiohttp>=3.8.0",
    "pyyaml>=6.0",
    "python-dateutil>=2.8.0",
    "asyncio>=3.4.3",
    "pathlib>=1.0.1",
]

dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
    "mypy>=0.991",
    "isort>=5.10.0",
]

setup(
    name="eJaegis-agent",
    version="1.0.0",
    author="JAEGIS Community",
    author_email="team@JAEGIS-method.com",
    description="Enhanced Multi-agent Architecture & Dependency Specialist - Perpetual codebase monitoring and dependency analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JAEGIS-method/eJaegis-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Version Control",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "neo4j": ["neo4j>=5.0.0"],
        "llm": ["openai>=1.0.0", "anthropic>=0.3.0"],
    },
    entry_points={
        "console_scripts": [
            "eJaegis=cli.eJaegis_cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "eJaegis": [
            "templates/*.json",
            "templates/*.yaml",
            "config/*.json",
        ],
    },
    keywords=[
        "dependency-analysis",
        "code-monitoring",
        "architecture",
        "multi-agent",
        "development-tools",
        "codebase-analysis",
        "impact-analysis",
        "JAEGIS-method"
    ],
    project_urls={
        "Bug Reports": "https://github.com/JAEGIS-method/eJaegis-agent/issues",
        "Source": "https://github.com/JAEGIS-method/eJaegis-agent",
        "Documentation": "https://JAEGIS-method.com/docs/eJaegis",
        "JAEGIS Method": "https://JAEGIS-method.com",
    },
)
