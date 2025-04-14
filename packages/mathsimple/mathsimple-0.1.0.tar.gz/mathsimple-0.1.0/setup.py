from setuptools import setup, find_packages

setup(
    name='mathsimple',
    version='0.1.0',
    author="rama",
    author_email='rama5864@gmail.com',
    description='A simple math package for basic arithmetic',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
)

