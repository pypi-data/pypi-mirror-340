from setuptools import setup, find_packages

setup(
    name='easybmp',
    version='0.0.2',
    description='A Python library which can easily read / modify / compare / and other functions with .bmp files',
    installed_requires=['struct','argparse','sys'],
    entry_points={
        'console_scripts': [
            'easybmp = easybmp:cli',
        ],
    },
)
