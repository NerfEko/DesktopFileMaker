"""Setup configuration for desktop-file-maker."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="desktop-file-maker",
    version="0.1.0",
    author="Ethan Kovach",
    description="A modern Linux TUI application for creating and managing .desktop files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NerfEko/DesktopFileMaker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "textual>=0.47.0",
        "requests>=2.31.0",
        "duckduckgo-search>=4.0.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "desktop-file-maker=src.main:main",
        ],
    },
)
