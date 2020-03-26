===============
Solvency2-rules
===============

.. image:: https://img.shields.io/github/release/DeNederlandscheBank/solvency2-rules.svg
           :target: https://github.com/DeNederlandscheBank/solvency2-rules/releases/
           :alt: Github release
.. image:: https://img.shields.io/badge/License-MIT/X-blue.svg
        :target: https://github.com/DeNederlandscheBank/dsolvency2-rules/blob/master/LICENSE
        :alt: License


Installation
============

Online installation
-------------------

Clone the project::

    git clone https://github.com/DeNederlandscheBank/solvency2-rules.git

Then start with a clean environment::
    
    conda create -n your_env_name python=3.5

And activate the environment::

    conda activate your_env_name

Make sure you are in the root of the cloned project. Install the required packages::

    pip install -r requirements.txt

Then install the Arelle package::

    pip install -e git+https://git@github.com/arelle/arelle.git@master#egg=Arelle --user

For now we included the taxonomy in the package, so you do not have to download this from the EIOPA website.

You have to make two changes to the Arelle package:

In src/arelle/arelle/ModelXbrl.py, line 969-970, replace::

            codeEffective = (messageCode and
                             (not logger.messageCodeFilter or logger.messageCodeFilter.match(messageCode))) 

by::

            codeEffective = (messageCode) 

And lines 1145-1147::

        elif (messageCode and
              (not logger.messageCodeFilter or logger.messageCodeFilter.match(messageCode)) and
              (not logger.messageLevelFilter or logger.messageLevelFilter.match(level.lower()))):

by::

        elif (messageCode):

(if you have a better quick fix, please let me know)
