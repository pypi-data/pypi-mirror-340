from setuptools import setup, find_packages

setup(
    name="analytics_tools",
    version="0.3.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to calculate WoE and IV",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "numpy",
        "ipython"
    ],
)
