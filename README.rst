==================
data-quality-rules
==================

.. image:: https://img.shields.io/github/release/DeNederlandscheBank/solvency2-rules.svg
           :target: https://github.com/DeNederlandscheBank/data-quality-rules/releases/
           :alt: Github release
.. image:: https://img.shields.io/badge/License-MIT/X-blue.svg
        :target: https://github.com/DeNederlandscheBank/data-quality-rules/blob/master/LICENSE
        :alt: License

This is Data Quality Rules repository for the Solvency 2 and the Financial Assessment Framework (FTK) quantitative reporting templates (QRTs). In this repository De Nederlandsche Bank publishes additional validation rules to improve the data quality of the QRTs.

This repository is part of the iForum pilot 'Data Quality Rules'. Want to know more? Please contact P.M.Willems@dnb.nl

* Free software: MIT/X license

Features
========

Here is what the package contains:

* (Statistical) validation rules for Solvency 2 and FTK QRTs

Martijn Source code to extract csv-, Pandas pickles- and html-files from XBRL instance files

* Source code to evaluate validation rules on Pandas pickle-files

* Notebook tutorials to get you started

Repository overview
===================

The directory structure of this repository is as follows: 

├── LICENSE
├── README.md          <- The top-level README for users of the this project
├── requirements.txt   <- The requirements file for reproducing the environment
│
├── data
│   ├── taxonomy       <- XBRL Taxonomies used by the repository
│   ├── instances      <- Example XBRL-instances and extracted files
│   └── ...            <- 
│
├── docs               <- Documentation
│
├── notebooks          <- Jupyter notebooks with tutorials
│
├── solvency2-rules    <- (Statistical) validation rules for Solvency 2 QRTSs
│
├── ftk-rules          <- (Statistical) validation rules for FTK QRTs
│
├── tests              <- Unittests of the source code provided
│
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    │
    └── arelle         <- Scripts to create exploratory and results oriented visualizations

.. include:: INSTALLATION.rst

.. include:: AUTHORS.rst

.. include:: CONTRIBUTING.rst

.. include:: HISTORY.rst
