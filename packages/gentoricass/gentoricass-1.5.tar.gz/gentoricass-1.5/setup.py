from setuptools import setup, find_packages

setup(
    # Package name (must be unique on PyPI)
    name="gentoricass",
    
    # Package version (increment as you make updates)
    version="1.5",
    
    # Brief description of your package
    description="A beginner-friendly programming language built on Python",
    
    # Long description (displayed on PyPI)
    long_description = open("README.md", encoding="utf-8").read(),  # Uses README.md for PyPI description
    long_description_content_type="text/markdown",  # Specifies Markdown format for README.md
    
    # Author name and contact (replace with your details)
    author="Dickily",
    author_email="dickilyyiu@gmail.com",  # Optional
    
    # License information
    license="MIT",
    
    # Packages to include (find_packages automatically detects subdirectories)
    packages=find_packages(),
    
    # Classifiers to categorize your library
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    # Minimum Python version required
    python_requires=">=3.8",
)
