from setuptools import setup, find_packages

setup(
    name="easy-db3",
    version="1.1.0",
    description="A simple category-based key-value database using plain text files.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="imAnesYT Dev",
    author_email="imanesytdev.contact@gmail.com",
    url="https://github.com/imAnesYT/easydb",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
)