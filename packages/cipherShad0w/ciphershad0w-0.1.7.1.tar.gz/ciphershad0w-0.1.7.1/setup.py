from setuptools import setup, find_packages

setup(
    name="cipherShad0w",
    version="0.1.7.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cipherShad0w=cipherShad0w.cli:main",
        ],
    },
    author="cipher-shad0w",
    author_email="Jannis.krija@icloud.com",
    description="Utilities by Jannis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cipher-shad0w/sorting_visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
