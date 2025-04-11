from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qnt_funcs",
    version="0.1.2", 
    author="Mozahidul Islam",
    author_email="mirivan722@gmail.com",
    description="Advanced tools for Python error handling and syntax correction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mi-rivan/qnt_funcs.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Changed to a valid license classifier
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",  # Fixed to a valid development status
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="error handling, syntax correction, debugging, development tools",
)