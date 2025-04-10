from setuptools import setup, find_packages

setup(
    name="ljainlib",  # should be unique on PyPI
    version="0.1.0",
    description="Utility library with math, string, and file helpers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lakshay Jain",
    author_email="ljainWG@gmail.com",
    # url="https://github.com/yourname/ljain-math",  # optional
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.12',
)
