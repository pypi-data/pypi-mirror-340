from setuptools import setup, find_packages

setup(
    name='rmvrarith1',
    version='0.1.0',
    author="V Ramachandran",
    author_email='rmvrpmu@gmail.com',
    description='A simple math package for basic arithmetic',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
)
