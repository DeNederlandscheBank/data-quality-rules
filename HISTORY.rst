=======
History
=======

0.1.0 (2020-09-07)
------------------

* Development release.

0.2.0 (2020-09-30)
------------------

* Package requirements added to setup.py (all required packages are now on Python Package Index (pypi.org))
* Unittests added for transforming XBRL to CSV (Solvency 2 and FTK) (in tests/)
* TravisCI and tox installed for automatic testing (only online distribution)
* Tutorial for transforming XBRL to CSV adapted to read taxonomies as zip-files instead of extracted files
* FTK script added to download automatically FTK taxonomy and test instances
* FTK bug fix: index column names include FTK. prefix
* Source code for downloading taxonomies moved to src
* README.rst adapted to reflect changes

0.3.0 (2020-10-19)
------------------

* Updated and simplified tutorial Evaluate DNBs Additional Validation Rules
* Added Tutorial to evaluate FTK validation rules
* Added Solvency 2 S.06 (assets) validation rules and updated S.08 (derivatives) validation rules
* Added FTK K208 (assets) and FTK K210 (derivatives) validation rules
* Deleted code to convert XBRL to HTML from Tutorial
* Added code to construct one large Dataframe with all templates with closed axes to Tutorial
* Added description of Data format requirements to README.rst
* README.rst adapted to reflect changes

0.4.0 (2020-11-16)
------------------

* Added Solvency 2 statistical validation rules to evaluate two periods for ARS and QRS
* Added FTK statistical validation rules between to evaluate two periods for FTK-JS and FTK-BEL
* Added tutorials for statistical validation rules
* Added datapoints for Solvency 2 group reports (ARG and QRG)
* Added taxonomies for Solvency 2 (versions 2.5.0, 2.4.0 and 2.3.0) and FTK (versions 2.1.0, 2.0.0, 1.0.3, 1.0.2, 1.0.1, 1.0.0, 0.9.0)
* README.rst adapted to reflect changes

0.4.1 (2020-11-16)
------------------

* Bug fix for evaluation of additional rules for group reports

0.4.2 (2020-11-26)
------------------

* Bug fix for tutorial to evaluate two periods
