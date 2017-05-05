from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pandoc-imagine',
    version = '0.1.4',

    # packages = ['pandoc-imagine'],

    description = 'A filter to process codeblocks into images or ascii art',
    long_description = long_description,

    author = 'hertogp',
    author_email = 'git.hertogp@gmail.com',

    url = 'https://github.com/hertogp/imagine',
    # download_url = 'https://github.com/hertogp/imagine/archive/0.1.0.tar.gz',

    keywords = ['pandoc', 'filter', 'codeblock', 'image', 'ascii-art'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Filters',
        'Natural Language :: English',
    ],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=["pandoc_imagine"],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pandoc-imagine = pandoc_imagine:main',
        ],
    },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pandocfilters>=1.4'],


    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},
)
