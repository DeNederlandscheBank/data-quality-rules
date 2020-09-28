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

* (Statistical) validation rules for Solvency 2

* Source code to extract csv-, Pandas pickles- and html-files from XBRL instance files

* Source code to evaluate validation rules on Pandas pickle-files

* Notebook tutorials to get you started


Installation
============

Online installation
-------------------

Clone the project::

  git clone https://github.com/DeNederlandscheBank/data-quality-rules.git

Then start with a clean environment::

  conda create -n your_env_name python=3.6

And activate the environment::

  conda activate your_env_name

Make sure you are in the root of the cloned project. Install the code and the required packages::

  pip install -e .

Offline installation
--------------------

We included all the required packages in the project, so you should be able to do an offline installation. Make sure you have at least Anaconda 5.3.1 installed.

Install data-quality-rules repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract the zip file from the data-quality-rules repository to the desired location.

Then start with a clean and empty environment::

  conda create -n your_env_name --offline

And activate the environment::

  conda activate your_env_name

Install the following packages::

  conda install pkgs/vc-14-0.tar.bz2

  conda install pkgs/vs2015_runtime-14.0.25420-0.tar.bz2

Then install the following packages::

  conda install pkgs/python-3.6.6-he025d50_0.tar.bz2

  conda install pkgs/pip-18.1-py36_1000.tar.bz2

  conda install pkgs/setuptools-40.6.3-py36_0.tar.bz2

(if you get an error you need to copy the required packages from Internet)

Make sure you are in the root of the cloned project. Then install the project with the packages in pkgs/.::

  pip install -e . --no-index --find-links pkgs/


Contributing
============

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/DeNederlandscheBank/data-quality-rules/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/DeNederlandscheBank/data-quality-rules/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.


Credits
=======

Development Lead
----------------

| Willem Jan Willemse <w.j.willemse@dnb.nl>
| Expert Centre on Data Analysis & Operational Management
| Division Insurance Supervision
| De Nederlandsche Bank (DNB)

Contributors
------------

* Annick van Ool (DNB)
* Richard Lieverse (DNB)
* Jan Huiskes (DNB)

Your name could be here, see how to contribute in the text above.
