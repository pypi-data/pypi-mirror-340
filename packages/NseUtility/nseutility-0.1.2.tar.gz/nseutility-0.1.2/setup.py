from setuptools import setup, find_packages

setup(
    name="NseUtility",
    version="0.1.2",
    author="Prasad",
    description="A utility to fetch NSE India data",
    packages=find_packages(),
    install_requires=["pandas", "requests", "numpy", "feedparser", "urllib3"],
    python_requires=">=3.8",
)