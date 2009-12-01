#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import setup
from cephalo import __version__

 
setup(
    name            = "Cephalo",
    version         = __version__,
    description     = "Cephalo is a framework for the fast prototyping of MEG data analyses.",
    keywords        = "MEG, neuroscience, data analysis, scientific computing",
    license         = "GPL3",
    author          = "Pedro Alcocer",
    author_email    = "pealco@gmail.com",
    url             = "http://pealco.net/cephalo",
    
    classifiers     = [ 
                'Development Status :: 1 - Alpha',
                'Intended Audience :: End Users/Desktop',
                'Intended Audience :: Science/Research',
                'Natural Language :: English',
                'Operating System :: POSIX',
                'Programming Language :: Python'
    ]
    packages        = ["sqd2h5", "cephalo"]
    scripts         = ["sqd2h5", "cephalo"]
    
    packages        = find_packages(exclude=['examples', 'docs']),
    include_package_data=True,
    install_requires=['numpy','tables']
    #test_suite='pybrain.tests.runtests.make_test_suite',
)