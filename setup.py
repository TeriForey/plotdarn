#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy>=1.16',
    'pvlib>=0.6',
    'pydarn @ git+https://github.com/SuperDarn/pydarn@1f68f47#egg=pydarn',
    'matplotlib',
    'aacgmv2>=2.6',
    'bokeh',
    'shapely',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Teri Forey",
    author_email='trf5@leicester.ac.uk',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="plotdarn provides methods to plot SuperDARN data using Bokeh",
    entry_points={
        'console_scripts': [
            'plotdarn=plotdarn.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='plotdarn',
    name='plotdarn',
    packages=find_packages(include=['plotdarn', 'plotdarn.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/TeriForey/plotdarn',
    version='0.1.0',
    zip_safe=False,
)
