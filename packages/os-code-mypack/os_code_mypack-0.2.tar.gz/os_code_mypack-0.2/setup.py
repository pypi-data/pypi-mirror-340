# setup.py

from setuptools import setup, find_packages

setup(
    name = 'os_code_mypack',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # none
    ],
    entry_points={
        "console-scripts":[
            "os_code_mypack-hello = os_code_mypack:hello",
            ],
    },
)