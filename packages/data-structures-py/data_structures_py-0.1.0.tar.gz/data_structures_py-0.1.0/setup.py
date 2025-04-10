from setuptools import setup, find_packages

setup(
    name="data-structures-py",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A pedagogical Python package implementing core data structures from scratch",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AudreyTiodo/data-structures-python",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)