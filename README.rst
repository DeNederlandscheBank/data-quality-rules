==================
data-quality-rules
==================

.. image:: https://img.shields.io/github/release/DeNederlandscheBank/data-quality-rules.svg
           :target: https://github.com/DeNederlandscheBank/data-quality-rules/releases/
           :alt: Github release
.. image:: https://readthedocs.org/projects/data-quality-rules/badge/?version=master
        :target: https://data-quality-rules.readthedocs.io/en/latest/?badge=master
        :alt: Documentation Status
.. image:: https://img.shields.io/badge/License-MIT/X-blue.svg
        :target: https://github.com/DeNederlandscheBank/data-quality-rules/blob/master/LICENSE
        :alt: License

This is Data Quality Rules repository for the Solvency 2 and the Financial Assessment Framework (FTK) quantitative reporting templates (QRTs). In this repository De Nederlandsche Bank (DNB) publishes additional validation rules to improve the data quality of the QRTs. This repository can be used by entities who submit supervisory reports to DNB.

The use of the validation rules published in this repository is not mandatory. You may choose to submit supervisory reports without prior evaluation of these validation rules. If you choose to use the validation rules published in this repository then you cannot derive any rights from this.

The documentation can be found `here <https://data-quality-rules.readthedocs.io/en/latest/?badge=latest>`_.

License
=======

The Data Quality Rule repository is free software under `MIT/X license <https://github.com/DeNederlandscheBank/data-quality-rules/blob/master/LICENSE>`_.

Features
========

Here is what the package contains:

* (Statistical) validation rules for Solvency 2 and FTK

* Source code to extract csv- and Pandas pickle-files from XBRL instance files

* Source code to evaluate validation rules on Pandas pickle-files

* Command line interfaces and notebook tutorials to get you started

Currently, the patterns and rules published here contain a limited number of EIOPA-validation rules and the code to evaluate the complete set of EIOPA-validation rules is not yet included.
