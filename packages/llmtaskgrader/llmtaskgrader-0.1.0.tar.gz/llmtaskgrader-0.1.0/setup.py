"""
安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="llmtaskgrader",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "httpx>=0.23.0",
        "click>=8.0.0",
        "pydantic>=1.9.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "llmtaskgrader=llmtaskgrader.cli.commands:main",
            "llmtg=llmtaskgrader.cli.commands:main",
        ],
    },
)
