from setuptools import setup, find_packages

setup(
    name="click-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "user-agents>=2.2.0",
        "requests>=2.26.0"
    ],
    author="Mohamed Meksi",
    author_email="mohamedmeksi37@gmail.com",
    description="Une bibliothèque pour tracker les clics et collecter des informations sur les visiteurs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/votre-repo/click-tracker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)