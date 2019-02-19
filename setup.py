#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    SITools2 client for Python
#    Copyright (C) 2013 - Institut d'astrophysique spatiale
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = "Pablo ALINGERY,Jean-Christophe Malapert, Elie Soubrie"
__date__ = "$8 mai 2013 04:03:39$"

try:
    from setuptools import setup, find_packages
except:
    messageError = "Import failed, module 'setuptools' is required.\n" \
    "To install it on Ubuntu linux distribution type in terminal:\n" \
    "'sudo apt-get install python-setuptools'"
    print(messageError)

else:
    setup(
        name='pySitools2',
        packages=find_packages(),
        version="0.0.2",
        # Declare your packages' dependencies here, for eg:
        install_requires=['simplejson', 'future', 'pip'],

        # Fill in these to make your Egg ready for upload to
        # PyPI
        author='Pablo ALINGERY',
        author_email='pablo.alingery@ias.u-psud.fr',
        description='A generic python Sitools2 client with some specific clients (GAIA, SDO)',
        url='http://sitools2.github.com/pySitools2_1.0/',
        license='GPLv3',
        long_description=open("README.md").read(),

        # could also include long_description, download_url, classifiers, etc.
        # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Programming Language :: Python',
            'Operating System :: OS Independent',
            'Environment :: Web Environment', 
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        ],
        download_url='https://github.com/MedocIAS/pySitools2_1.0/archive/master.zip',
        test_suite="tests")
