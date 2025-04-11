from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='data-structures-py-jordankbm',
    version='0.1.0',
    description='Implementation of various data structures in Python from scratch',
    author='Jordan Kevin Buwa Mbouobda',
    author_email='jmbouobda@aimsammi.org',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy==2.2.4',
        'networkx==3.4.2',
        'matplotlib==3.10.1',
    ],
    classifiers= [
        "Programming Language :: Python :: 3",
    ],
    long_description = description,
    long_description_content_type= 'text/markdown',
    url = "https://github.com/Jordan-buwa/data-structures-python",
    python_requres = ">=3.8"
)
