from setuptools import setup, find_packages

setup(
    name="contraction-fix",
    version="0.1.0",
    description="A fast and efficient library for fixing contractions in text",
    author="Sean Gao",
    author_email="seangaoxy@gmail.com",
    packages=find_packages(),
    package_data={
        "contraction_fix": [
            "data/standard_contractions.json",
            "data/informal_contractions.json",
            "data/internet_slang.json"
        ],
    },
    install_requires=[],
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Text Processing :: Linguistic",
    ],
) 