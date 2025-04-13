from setuptools import setup, find_packages

setup(
    name="mcp_radiation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "python-dateutil>=2.8.2",
    ],
    author="俞海",
    author_email="yuhai_8203@126.com",
    description="A package for retrieving solar radiation data using NASA's POWER API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yuhai8203/mcp_radiation",
    keywords="solar radiation, NASA POWER, weather data, renewable energy",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/yuhai8203/mcp_radiation/issues",
        "Source": "https://github.com/yuhai8203/mcp_radiation",
    },
) 