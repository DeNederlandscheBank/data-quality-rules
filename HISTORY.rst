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
