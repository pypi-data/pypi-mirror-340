import sys

from setuptools import setup, find_packages

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

setup(
    name="suss",
    version="0.2.0",
    description="AI-powered bug finder that knows your codebase",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    url="https://github.com/shobrook/suss",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "cohere",
        "json-repair",
        "litellm==1.61.19",
        "rich",
        "saplings",
        "sortedcollections",
        "tree-sitter==0.21.3",
        "tree-sitter-languages==1.10.2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
    ],
    # long_description=open("README.md").read(),
    keywords="code-review bug-finder ai debugger agent llm codebase code-assistant",
    entry_points={
        "console_scripts": [
            "suss=suss.suss:main",
        ],
    },
)
