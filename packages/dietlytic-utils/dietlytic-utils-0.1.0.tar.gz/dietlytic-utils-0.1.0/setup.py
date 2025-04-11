from setuptools import setup, find_packages

setup(
    name="dietlytic-utils",
    version="0.1.0",
    description="A sample package with a _utils folder",
    author="gayatri",
    author_email="gayatri@email.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kotapavankalyanreddy/mypackage",  
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
