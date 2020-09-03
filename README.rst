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

Make sure you are in the root of the cloned project. Install the required packages::

  pip install -r requirements.txt

Then install the Arelle package::

  pip install -e git+https://git@github.com/arelle/arelle.git@master#egg=Arelle --user

If this doesn't work, unzip the file pkgs/arelle-1.0.0.zip to the subdirectory src, such that src contains the subdirectory with the name arelle. Then install the package by going to the root of the arelle project, where the setup.py file is, and execute::

  pip install -e . --user

Then install the data-patterns package::

  pip install data-patterns

*Continue at 'Changes to the Arelle package' -->*

Offline installation
--------------------

We included all the required packages in the project, so you should be able to do an offline installation. Make sure you have at least Anaconda 5.3.1 installed.

To do an offline installation you need some files from the internet downloaded in advance: 

* the zip file with the data-quality-rules repository from https://github.com/DeNederlandscheBank/data-quality-rules.git;

* the zip file with the data-patterns repository from https://github.com/DeNederlandscheBank/data-patterns.git; and 

* the zip files with the taxonomy and example instances from the EIOPA website
    https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_with_external_hotfix.zip; and
    https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0.zip

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

Make sure you are in the root of the cloned project. Then install the remaining packages in pkgs/.::

  pip install -r requirements.txt --no-index --find-links pkgs/

Then unzip the file pkgs/arelle-1.0.0.zip to the subdirectory src, such that src contains the subdirectory with the name arelle.

And install the package by going to the root of the arelle project, where the setup.py file is, and execute::

  pip install -e . --user

Install data-patterns repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then install the data_patterns package. Make sure you have the zip file from https://github.com/DeNederlandscheBank/data-patterns.git. Extract the zip file to the desired location, go to the root of the repo and execute::

  pip install -e .

Copy taxonomy and instance files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copy the Solvency 2 XBRL taxonomy file and the Solvency 2 XBRL instance examples (both zip files) to the directory data/downloaded files.

Changes to the Arelle package
=============================

To improve performance change in src/arelle/arelle/FormulaEvaluator.py the function factsPartitions(xpCtx, facts, aspects) to::

  def factsPartitions(xpCtx, facts, aspects):
      contexts_dict = dict()
      for fact in facts:
          if fact.context not in contexts_dict.keys():
              contexts_dict[fact.context] = [fact]
          else:
              contexts_dict[fact.context].append(fact)
      return list(contexts_dict.values())

*This only works for EIOPA taxonomies, but not in general!*

Installing taxonomy and example instance files
==============================================

Go to submap data/ and execute::

  python solvency2_data.py

This downloads the Solvency 2 XBRL taxonomy 2.4 and the corresponding example instance files and extracts them in the proper directories.

The FTK taxonomy is not yet automatically downloaded, but you can download the zip-file and extract it, and then copy the files to data/taxonomy/arelle/cache/http. You can use both taxonomies at the same time. Some files in the FTK taxonomy already exists in the Solvency 2 taxonomy; you do not need to replace these.

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

Your name could be here, see how to `contribute <https://github.com/DeNederlandscheBank/data-quality-rules/blob/master/CONTRIBUTING.rst>`_
