# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup

directory = os.path.dirname(os.path.abspath(__file__))


README_PATH = os.path.join(directory, 'README.rst')


setup(
    name='sphinx-simplepdf',
    version='1.3.0',
    url='https://github.com/useblocks/sphinx-simplepdf',
    license='Commercial',
    author='team useblocks',
    author_email='info@useblocks.com',
    description='A specific theme for Sphinx-Needs',
    long_description=open(README_PATH, encoding='utf-8').read(),
    zip_safe=False,
    packages=['builders', 'themes/sphinx_simplepdf'],
    package_data={'themes/sphinx_simplepdf': [
        'theme.conf',
        '*.html',
        'static/styles/*.css',
        'static/js/*.js',
        'static/fonts/*.*'
    ]},
    include_package_data=True,
    # See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points={
        'sphinx.html_themes': [
            'sphinx_simplepdf = themes.sphinx_simplepdf',
        ],
        'sphinx.builders': [
            'simplepdf = builders.simplepdf'
        ]
    },
    install_requires=[
        'sphinx',
        'weasyprint',       # the used PDF builder
        'libsass'           # needed to generate css on the fly
        'beautifulsoup4'    # needed for HTML manipulations
    ],
    classifiers=[
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Theme',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
)
