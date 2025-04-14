from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mongo_easy",
    version="0.1.1",
    author="Prakhar Doneria",
    author_email="prakhardoneria3@gmail.com",
    description="A simple and intuitive MongoDB helper library for everyone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prakhardoneria/mongo_easy",  
    project_urls={
        "Documentation": "https://github.com/prakhardoneria/mongo_easy/docs",
        "Source": "https://github.com/prakhardoneria/mongo_easy",
        "Tracker": "https://github.com/prakhardoneria/mongo_easy/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pymongo>=3.12.0",
    ],
    entry_points={
        "console_scripts": [
            "mongo-easy=mongo_easy.cli.__main__:main",
        ],
    },
)
