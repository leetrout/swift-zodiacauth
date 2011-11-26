from setuptools import setup, find_packages

name = 'zodiacauth'
version = '0.1'

setup(
    name=name,
    version=version,
    description='Zodiac based auth middleware for Swift',
    license='Apache License (2.0)',
    author='Lee Trout',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)',
        ],
    install_requires=['swauth'],
    entry_points={
        'paste.filter_factory': [
            'zodiacauth=zodiacauth:filter_factory',
            ],
        },
    )