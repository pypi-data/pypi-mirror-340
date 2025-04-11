from setuptools import find_packages, setup

setup(
    name="llmprint",
    version="0.1.2",
    author="Raj Shekhar",
    description="CLI tool to print directory structure and file contents for LLM context generation",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rsh3khar/llmprint",
    packages=find_packages(),
    install_requires=[
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "llmprint=llmprint.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Text Processing :: General",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Homepage": "https://github.com/rsh3khar/llmprint",
        "Bug Tracker": "https://github.com/rsh3khar/llmprint/issues",
    },
    keywords="llm ai chatgpt claude directory-tree file-contents clipboard utility development tool",
    python_requires=">=3.6",
)
