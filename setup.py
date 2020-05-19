"""Support to set up nodejsscan."""
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name="nodejsscan",
    description='Static security code scanner (SAST) for Node.js applications',
    version="3.7",
    author="Ajin Abraham",
    author_email="ajin25@gmail.com",
    license='GPLv3',
    packages=find_packages(include=[
        "core",
        "core.*",
    ]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3'
    ],
    entry_points={
        'console_scripts': [
            "nodejsscan = core.cli:main",
        ]
    },
    include_package_data=True,
    url="https://github.com/ajinabraham/nodejsscan",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "jsbeautifier==1.10.3",
        "defusedxml==0.6.0",
    ],
)
