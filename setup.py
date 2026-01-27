from setuptools import setup, find_packages
import os

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup( name="mlops project",
       version=.01,
       author="Manoj Joseph",
       packages=find_packages(),
         install_requires=required,
         )
