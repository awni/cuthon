from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

desc = ("A simple tool to select the first "
        "available GPU(s) and run Python")
setup(
    name='cuthon',
    version='0.5',
    description=desc,
    long_description=long_description,

    url='https://github.com/awni/cuthon',
    author='Awni Hannun',
    author_email='awni@stanford.edu',
    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='gpu development cuda',

    py_modules=["cuthon"],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cuthon=cuthon:main',
        ],
    }
)
