from setuptools import setup, find_packages

setup(
    name="nodejsscan",
    version="2.6",
    author="Ajin Abraham",
    author_email="ajin25@gmail.com",
    packages=find_packages(include=[
        "core",
        "core.*",
    ]),
    entry_points={
        'console_scripts': [
            "nodejsscan = core.cli:main",
        ]
    },

    # Include additional files into the package
    include_package_data=True,
    data_files=[('core', ['core/rules.xml'])],

    # Details
    url="http://pypi.python.org/pypi/nodejsscan/",

    description="Static Code Analyzer for Node.js Applications",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "jsbeautifier==1.7.5",
    ],
)
