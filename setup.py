#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0', 'watchdog', 'requests', 'lxml',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='subtitlesplease',
    version='0.1.0',
    description="Watches filesystem for video files (avi, mkv and mp4) and automatically downloads the subtiles ",
    long_description=readme + '\n\n' + history,
    author="Rainaldo F Crosbourne",
    author_email='rcrosbourne@gmail.com',
    url='https://github.com/rcrosbourne/subtitlesplease',
    packages=[
        'subtitlesplease',
    ],
    package_dir={'subtitlesplease':
                 'subtitlesplease'},
    entry_points={
        'console_scripts': [
            'subtitlesplease=subtitlesplease.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='subtitlesplease',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
