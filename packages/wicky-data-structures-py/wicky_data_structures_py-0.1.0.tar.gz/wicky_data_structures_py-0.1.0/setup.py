from setuptools import setup, find_packages

setup(
    name="wicky-data-structures-py",
    version="0.1.0",
    description="A pedagogical Python package implementing core data structures from scratch",
    author="Wycliffe Nzomo",
    author_email="wycliffenzomo@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(where=".", include=["data_structures*"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
