from setuptools import setup, find_packages


VERSION = '0.1.3'
URL = 'https://github.com/cospectrum/pylinal.git'

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='pylinal',
    version=VERSION,
    license='MIT',
    url=URL,
    description='Generic Linear Algebra in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alexey Severin',
    install_requires=requirements,
    packages=find_packages(),
    keywords=['python'],
)


