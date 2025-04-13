from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='easybmp',
    version='0.0.4',
    description='A Python library which can easily read / modify / compare / and other functions with .bmp files',
    installed_requires=['struct','argparse','sys'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'easybmp = easybmp:cli',
        ],
    },
)
