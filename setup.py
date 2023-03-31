from setuptools import setup, find_packages

setup(name='support_modules',
      version='1.0.12',
      description='support module with utility functions',
      author='Manuel Camargo',
      url='https://github.com/Mcamargo85/support_modules',
      package_dir={"": "src"},
      packages=['utils', 'readers', 'analyzers'],
      install_requires=[
        'numpy',
        'networkx',
        'pm4py>=2.6.1',
        'pandas',
        'matplotlib',
        'jellyfish',
        'scipy']
      )
