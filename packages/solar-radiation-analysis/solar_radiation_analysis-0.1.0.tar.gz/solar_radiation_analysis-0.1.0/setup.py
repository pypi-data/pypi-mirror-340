from setuptools import setup, find_packages

setup(
    name="solar-radiation-analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "numpy",
    ],
    author="Yu Hai",
    author_email="yuhai_8203@126.com",
    description="A Python package for analyzing solar radiation and wind speed data from NASA POWER API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yuhai8203/solar-radiation-analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 