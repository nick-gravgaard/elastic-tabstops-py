from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

setup(name='ElasticTabstops',
    version=version,
    description='Converts text indented/aligned with elastic tabstops',
    long_description=open('README.md').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Markup',
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Nick Gravgaard',
    author_email='nick@nickgravgaard.com',
    url='https://github.com/nickgravgaard/elastic-tabstops-py',
    license='MIT/X11',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
    )
