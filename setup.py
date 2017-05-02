from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pandoc-imagine',
    packages = ['pandoc-imagine'],
    version = '0.1.0',
    description = 'A filter to process codeblocks into images or ascii art',
    long_description = long_description,
    author = 'hertogp',
    author_email = 'git.hertogp@gmail.com',
    url = 'https://github.com/hertogp/imagine',
    download_url = 'https://github.com/hertogp/imagine/archive/0.1.tar.gz',
    keywords = ['pandoc', 'filter', 'codeblock', 'image', 'ascii-art'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters'
  ],
)
