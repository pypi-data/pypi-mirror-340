from setuptools import setup, find_packages

setup(
    name='SB14009UNO',
    version='0.1.1',
    packages=find_packages(),  
    install_requires=[
        'numpy',  
    ],
    include_package_data=True,  
    license='MIT',  
    description='Librería para resolver sistemas de ecuaciones',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Oscar Santos',
    author_email='sb14009@ues.edu.sv',
)
