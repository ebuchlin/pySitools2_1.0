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
__author__="Jean-Christophe Malapert"
__date__ ="$8 mai 2013 04:03:39$"

from setuptools import setup,find_packages

setup (
  name = 'pySitools2_1.0',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['simplejson'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'Pablo ALINGERY',
  author_email = 'pablo.alingery@ias.u-psud.fr',

  summary = 'A generic python Sitools2 client with some specific clients (GAIA, SDO)',
  url = 'http://sitools2.github.com/pySitools2_1.0/',
  license = 'GPLv3',
  long_description = open("README.md").read(),

  # could also include long_description, download_url, classifiers, etc.
  # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers = [
  'Development Status :: 2 - Pre-Alpha',
  'Environment :: Web Environment',
  'Framework :: SITools2 :: 1.0',
  'Intended Audience :: Developers',
  'Intended Audience :: Science/Research',
  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
  ],
  download_url = 'https://github.com/SITools2/pySitools2_1.0/archive/master.zip',
  test_suite="tests",
)