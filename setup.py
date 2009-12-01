#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

from distutils.core import setup
#from setuptools import setup
 
setup(
    name            = "Cephalo",
    version         = "0.2.2",
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
    ],
    scripts         = ["src/sqd2h5", "src/cephalo"],
    packages        = ["cephalo_tools"],
    package_dir = {'cephalo_tools':'src/cephalo_tools'},
    install_requires=['pyyaml']
    #test_suite='pybrain.tests.runtests.make_test_suite',
)