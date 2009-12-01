Cephalo
=======

By Pedro Alcocer.

Cephalo is software for the fast and easy processing of MEG data. Cephalo eliminates a lot of the grudge work out of getting MEG data from its raw form to a state that is useful for analysis.

Tools
-----

* `sqd2h5`: converts MEG160 .sqd files to HDF5 .h5 files.
* `cephalo`: processes MEG data

Requirements
------------

In order to run, Cephalo requires the `numpy`, `scipy`, and PyTables libraries. These are all included in the Enthought Python Distribution (EPD), which is free for academic use. The EPD comes as a single installer which makes the installation of these libraries very simple. Cephalo also requires the PyYAML library in order to parse the configuration file.

* Enthought Python Distribution v5.1.1 or greater
    * `http://www.enthought.com/products/edudownload.php`
* PyYAML 3.0 or greater
    * `http://pyyaml.org/`
    
Install
-------

Cephalo is installed in the usual way that Python packages are installed.
    
    > cd cephalo
    > sudo python setup.py install
    
License
-------

This software is distributed under the terms of the GNU General Public License. See the `COPYING` file for more information.

Website
-------

`http://pealco.net/cephalo`