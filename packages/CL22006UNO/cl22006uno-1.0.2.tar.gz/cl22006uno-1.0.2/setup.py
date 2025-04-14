from setuptools import setup

import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent


setup(
    name='CL22006UNO',
    version='1.0.2',
    author='Josue Israel Colocho Lopez',
    author_email='CL22006@ues.edu.sv',
    description='Liberia para resolver ecuaciones lineales y no lineales sin usar librerias aparte',
    long_description=(HERE / "README.md").read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/JosueCLopez/CDA135-GT02-CL22006UNO',
    license='MIT',
    packages=['CL22006UNO'],
    package_dir={'CL22006UNO': 'CL22006UNO'},
    entry_points={
        'console_scripts': [
            'ver = CL22006UNO.ver:main',
        ],
    },
)