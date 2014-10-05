#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from ez_setup import use_setuptools

use_setuptools()
from setuptools import find_packages

setup(name='Torrentstatus',
      version='1.0',
      description='Python package for handling actions when torrent status changes',
      author='Bjørn Berg',
      author_email='bjorninge-torrentstatus-doc@bjorninge.no',
      url='http://bjorninge.no',
      packages=find_packages(),
      install_requires = ["yapsy", "appdirs"],
      package_data = {
        '': ["plugins/*.py", "plugins/*.plugin-manifest"]
      },
      zip_safe = False


)