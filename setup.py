from setuptools import setup, find_packages

setup(name='support_module',
    version='1.0.0',
    description='support module with utility functions',
    author='Manuel Camargo',
    url='https://github.com/Mcamargo85/support_module',
    packages=['support'],
    install_requires=[
        'numpy',
        'platform',
        'networkx'
    ]
)
