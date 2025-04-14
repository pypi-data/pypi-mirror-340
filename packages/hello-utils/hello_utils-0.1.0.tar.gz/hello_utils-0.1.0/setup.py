from setuptools import setup, find_packages

setup(
    name="hello-utils",  # must be unique on PyPI
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="A simple hello world utility package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hello-utils",  # Optional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
