#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

__author__ = 'Pedro Alcocer, pealco@gmail.com'
 
 
from setuptools import setup, find_packages
 
 
setup(
    name="Cephalo",
    version="0.1",
    description="Cephalo is a framework for the fast prototyping of MEG data analyses.",
    license="GPL",
    keywords="MEG, neuroscience, data analysis, scientific computing",
    url="http://pealco.net",
    packages=find_packages(exclude=['examples', 'docs']),
    include_package_data=True,
    install_requires=['numpy','tables']
    #test_suite='pybrain.tests.runtests.make_test_suite',
)