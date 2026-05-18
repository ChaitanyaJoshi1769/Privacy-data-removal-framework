#!/usr/bin/env python3
"""
setup.py - Python package configuration for Footprint Ops
"""

from setuptools import setup, find_packages

setup(
    name="footprint-ops",
    version="0.1.0",
    description="Digital footprint remediation and privacy minimization toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Privacy Operations",
    url="https://github.com/ChaitanyaJoshi1769/footprint-ops",
    license="MIT",
    
    packages=find_packages(exclude=["tests", "*.tests", "tests.*"]),
    include_package_data=True,
    
    install_requires=[
        "playwright>=1.40.0",
        "beautifulsoup4>=4.12.0",
        "scrapy>=2.11.0",
        "requests>=2.31.0",
        "httpx>=0.25.0",
        "click>=8.1.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.0",
        "networkx>=3.2.0",
        "pandas>=2.1.0",
        "cryptography>=41.0.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "structlog>=23.2.0",
    ],
    
    entry_points={
        "console_scripts": [
            "footprint-ops=footprint_ops:cli",
        ],
    },
    
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
