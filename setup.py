from setuptools import setup, find_packages

setup(name='support_modules',
    version='1.0.3',
    description='support module with utility functions',
    author='Manuel Camargo',
    url='https://github.com/Mcamargo85/support_modules',
    packages=['utils', 'readers', 'tests'],
    install_requires=[
        'numpy',
        'networkx',
        'pm4py',
        'pandas',
        'matplotlib']
)
