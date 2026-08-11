from setuptools import setup,find_packages

with open('requirements.txt') as f:
    requirements=f.read().split()


setup(
    name='Brain-breast-cancer',
    author='Zaheer',
    version='dmt',
    packages=find_packages(),
    install_requires=requirements
)