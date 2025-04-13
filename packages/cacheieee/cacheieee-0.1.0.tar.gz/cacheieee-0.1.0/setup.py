from setuptools import setup, find_packages

setup(
    name='cacheieee', 
    version='0.1.0',  
    packages=find_packages(),  
    install_requires=[],  
    author='Mradul Natani',  
    author_email='mradulnatani0@gmail.com',  
    description='A simple Python client for cacheieee server',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    url='https://github.com/mradulnatani/cacheieee',  # Your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
)
