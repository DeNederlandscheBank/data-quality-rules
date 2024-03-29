.. highlight:: shell

============
Installation
============

We provide two installation methods: online and offline installation. For the online installation you need a connection to internet to download the required packages. For the offline installation you need to download a limited number of files (specified below) and then you can install everything without a connection to internet. After installation of the repository, you need to download the taxonomies and examples files you want to work with. We provided a script to download these files and put them in the correct location.

For both methods we recommend to have Anaconda (> 5.3.1) installed.

Online installation
===================

Clone the project::

  git clone https://github.com/DeNederlandscheBank/data-quality-rules.git

Then start with a clean environment::

  conda create -n your_env_name python=3.6

And activate the environment::

  conda activate your_env_name

Make sure you are in the root of the cloned project. Install the code and the required packages::

  pip install -e .

Offline installation
====================

We included all the required packages in the project, so you should be able to do an offline installation.

To do an offline installation you need some files from the internet downloaded in advance: 

* the zip file with the data-quality-rules repository from https://github.com/DeNederlandscheBank/data-quality-rules.git;

* the zip files with the taxonomy and example instances from the EIOPA website (https://dev.eiopa.europa.eu/Taxonomy/Full/2.7.0/S2/EIOPA_SolvencyII_XBRL_Taxonomy_2.7.0_hotfix_with_External_Files.zip; and https://dev.eiopa.europa.eu/Taxonomy/Full/2.7.0/S2/EIOPA_SolvencyII_XBRL_Instance_documents_2.7.0.zip)

* the zip files with the taxonomy and example instances from the DNB website (https://www.dnb.nl/media/fivpjdpj/vns_taxonomy_1-1-0.zip; and https://www.dnb.nl/media/o10oswji/vns_sample_instances_1-1-0.zip)


Install data-quality-rules repository
-------------------------------------

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

(if you get an error you need to copy the required packages from internet)

Make sure you are in the root of the cloned project. Then install the project with the packages in pkgs/.::

  pip install -e . --no-index --find-links pkgs/


Copy taxonomy and instance files
--------------------------------

Copy the Solvency 2 and VNS XBRL taxonomy file and the Solvency 2 and VNS XBRL instance examples (both zip files) to the directory data/downloaded files.


Taxonomy and example instance files
===================================

For Solvency 2 and VNS execute (in the root of the project)::

  python src/solvency2_data.py

This downloads the Solvency 2 and VNS XBRL taxonomy and the corresponding example instance files and extracts them in the proper directories.

For FTK, execute (in the root of the project)::

  python src/ftk_data.py

This downloads the FTK taxonomy and the corresponding example instance files and extracts them in the proper directories.

