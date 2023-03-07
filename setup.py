# import
from setuptools import setup

# setup
setup(
    name='mt5_scraper',
    version='0.9.5',
    url='https://github.com/XO30/MT5Scraper',
    author='Stefan Siegler',
    author_email='dev@siegler.one',
    py_modules=['mt5_scraper'],
    classifiers=[
        'Intended Audience :: Data Scientists',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    install_requires=[
        'anytree',
        'pandas',
        'tqdm',
        'MetaTrader5',
        'pytz',
        'numpy==1.24.0'
    ],
    python_requires='>3.5, <4',
)
