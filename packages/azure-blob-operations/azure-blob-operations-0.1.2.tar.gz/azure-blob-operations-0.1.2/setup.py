from setuptools import setup, find_packages

setup(
    name="azure-blob-operations",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "azure-storage-blob>=12.23.1",
    ],
    author="Uday Pallati",
    author_email="udaypallati123@gmail.com",
    description="A utility package for generic Azure Blob Storage operations",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.5",
)