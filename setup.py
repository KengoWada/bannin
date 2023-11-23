from setuptools import setup

setup(
    name="bannin",
    version="0.1.0",
    packages=["bannin"],
    entry_points={"console_scripts": "bannin = bannin.__main__:main"},
)
