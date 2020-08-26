===============
Solvency2-rules
===============

.. image:: https://img.shields.io/github/release/DeNederlandscheBank/solvency2-rules.svg
           :target: https://github.com/DeNederlandscheBank/solvency2-rules/releases/
           :alt: Github release
.. image:: https://img.shields.io/badge/License-MIT/X-blue.svg
        :target: https://github.com/DeNederlandscheBank/dsolvency2-rules/blob/master/LICENSE
        :alt: License

This is the Data Quality Rules repository for the Solvency 2 quantitative reporting templates (QRTs). In this repository De Nederlandsche Bank publishes additional validation rules to improve the data quality of the QRTs.

This repository is part of the iForum pilot 'Data Quality Rules'.

Want to know more? Please contact P.M.Willems@dnb.nl

*The repository is currently under construction.*

Installation
============

Online installation
-------------------

Clone the project::

    git clone https://github.com/DeNederlandscheBank/solvency2-rules.git

Then start with a clean environment::
    
    conda create -n your_env_name python=3.6

And activate the environment::

    conda activate your_env_name

Make sure you are in the root of the cloned project. Install the required packages::

    pip install -r requirements.txt

Then install the Arelle package::

    pip install -e git+https://git@github.com/arelle/arelle.git@master#egg=Arelle --user

For now we included the taxonomy in the package, so you do not have to download this from the EIOPA website.

Changes to the Arelle package
-----------------------------

None at this time.

Offline installation
-------------------

We included all the required packages in the project, so you should be able to do an offline installation.

Make sure you have at least Anaconda 5.3.1 installed. 

Make sure you have the zip file from https://github.com/DeNederlandscheBank/solvency2-rules.git. Extract the zip file to the desired location.

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

Then install the data_patterns package.

Make the corrections in Arelle described in the online installation procedure.

Taxonomy location
-----------------

The taxonomy should be in a specific location, otherwise it won't work. 

You can download the taxonomy that you want to use from the EIOPA-website (https://www.eiopa.europa.eu/tools-and-data/supervisory-reporting-dpm-and-xbrl_en#XBRLTaxonomyReleases).

For now, we included the zip file in the repository (in subdirectory data/taxonomy)

Unzip the taxonomy in data/taxonomy/arelle/cache/http

After unzipping this directory should contain::

	dev.eiopa.europa.eu/

	eiopa.europa.eu/

	META-INF/

	www.eurofiling.info/

	www.xbrl.org/

	MDMetricDetails.xml
