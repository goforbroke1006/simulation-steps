#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='simulationsteps',
      packages=find_packages(include=['simulationsteps', ]),
      version='0.0.17',
      description='Behave steps to reproduce bugs',
      author='Sergey Cherkesov',
      author_email='go.for.broke1006@gmail.com',
      url='https://github.com/goforbroke1006/simulationsteps',
      license='MIT',
      #
      install_requires=[],
      setup_requires=['pytest-runner'],
      tests_require=['pytest==4.4.1'],
      test_suite='tests',
      )
