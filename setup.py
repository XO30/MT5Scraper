# import
from setuptools import setup

# setup
setup(
    name='mt5_scraper',
    version='0.9.3',
    url='https://github.com/XO30/MT5Scraper',
    author='Stefan Siegler',
    author_email='dev@siegler.one',
    py_modules=['mt5_scraper'],
    classifiers=[
        'Intended Audience :: Data Scientists',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'anytree',
        'pandas',
        'tqdm',
        'MetaTrader5',
    ]
)
