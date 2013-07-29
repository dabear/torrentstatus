#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from ez_setup import use_setuptools

use_setuptools()
from setuptools import find_packages

setup(name='Torrentstatus',
      version='0.1',
      description='Python package for handling actions when torrent status changes',
      author='Bjørn Berg',
      author_email='bjorninge-torrentstatus-doc@bjorninge.no',
      url='http://bjorninge.no',
      packages=find_packages()
)