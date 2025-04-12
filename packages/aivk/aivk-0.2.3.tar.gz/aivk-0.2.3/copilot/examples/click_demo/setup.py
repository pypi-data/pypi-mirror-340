from setuptools import setup, find_packages

setup(
    name="click-demo",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "click-demo=click_demo:main",
        ],
    },
)