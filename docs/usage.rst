=====
Usage
=====

The Data Quality Rules repository allows you to evaluate the data quality of Solvency 2 supervisory reports and FTK supervisory reports before you submit them to DNB. You can either apply the rules directly to the XBRL-instance that you want to submit to DNB, or you can apply the rules at an earlier stage in your reporting process.

If you want to apply the rules on internal data sets, then you have to make sure that the format of the data satisfies the data format requirement set out in :ref:`Data format requirements`.

If you want to apply the rules to the XBRL-instance you first need to convert the instance to Pandas files (see :ref:`Converting XBRL instances to Pandas and CSV`). The resulting files will be in the correct data format. We recommend to start with this option. 

Evaluation of the rule sets is done by a simple command line interface. We added Jupyter notebooks with a step-by-step description of all parts of the code, in case you want to understand the separate steps and include some steps in your internal reporting process.

Currently we have three rules sets available:

- Additional rules for Solvency 2 reports published by DNB (see :ref:`Evaluating additional Rules`)

- Rules for financial data (individual assets and derivates) (see :ref:`Evaluating financial Data Rules`)

- Patterns to compare two subsequent reports (see :ref:`Evaluating rule sets for report comparison`)

All rule sets are evaluated with DNB's `data-patterns package <https://github.com/DeNederlandscheBank/data-patterns>`_. With this package we generated most rule sets that we have published here (based on reports that have been submitted to us).

.. include:: usage_xbrl2csv.rst
.. include:: usage_additionalrules.rst
.. include:: usage_financialdatarules.rst
.. include:: usage_reportscomparisonrules.rst


Rule thresholds
===============

Currently, we have set the threshold on zero decimals, which means that a rule is satisfied if the difference between the expected value and the reported value is lower than 1.5e0. This threshold is set at the level of the rule. This is a slightly different approach than the one applied in XBRL validation rules, where thresholds are set at the level of separate data points. This means that it is possible that an exception to a DQR rule is triggered, where an XBRL rule is not triggered because it applies higher thresholds.


Logging
=======

Logging is performed for each rule set and is set to **logging.INFO**. Output is written to  results\\rule-set-1.log, results\\rule-set-2.log and results\\rule-set-3.log, depending on the rule set that is evaluated. Logging of the data-patterns package is stored in this file, so you can see the result of each rule and pattern evaluation. Log level is currently not an input but you can change the level in the apply-files in solvency2-rules\\.


The format of the patterns and rules files
==========================================

The input with the rule sets described above are stored in the same format in Excel files. The columns are described here:

- **pattern_id**: the name of the pattern or rule that was applied. A pattern or rule can apply to more than part of the report, but has the same form.

- **cluster**: the group or cluster to which the pattern or rule applies (optional), for example life, non-life or reinsurance.

- **pattern_def**: the definition of the pattern. The definition uses a simply syntax with references to the datapoints that should be relatively easy to read.

- **support**: the number of occurences that satisfy this pattern or rule in reports that were previously submitted to DNB.

- **exceptions**: the number of occurences that do not satisfy this pattern or rule in reports submitted to DNB.

- **confidence**: the support divided by (support plus exceptions). This is an indicator for how exceptional this pattern or rule is. If the confidence is one, then the pattern or rule is in all cases satisfied. If the confidence is lower than one then this could point to an error in the data or an unusual but acceptable circumstance that led to this exception. Only patterns with very high confidences are published in this repository.

- **pattern_status**: the status of the pattern or rule, i.e. blocking taxonomy rule, non-blocking taxonomy rule, validation rule or statistical validation rule.

You can find the documentation of the data-patterns package `here <https://data-patterns.readthedocs.io/en/latest/>`_.


The format of the results files
===============================

The output of the evaluation of the rule sets are all stored in the same format in Excel files.

* **First columns** describe the index of the report

* **result_type**: true if the pattern or rule is satisfied, false if the pattern or rule is not satisfied

* **pattern_id**: the name of the pattern or rule that was applied. A pattern or rule can apply to one or more parts of the report, but has the same form.

* **cluster**: the group or cluster to which the pattern or rule applies (optional), for example life, non-life or reinsurance.

* **support**: the number of occurrences that satisfy this pattern or rule in the report.

* **exceptions**: the number of occurrences that do not satisfy this pattern or rule in the report.

* **confidence**: the support divided by (support plus exceptions). 

* **pattern_def**: the definition of the pattern. The definition uses a simply syntax with references to the datapoints that should be relatively easy to read.

* **P values**: the values of data points in the left hand side of the pattern or rule (in case of an if-then rule: the if part)

* **Q values**: the values of data points in the right hand side of the pattern or rule (in case of an if-then rule: the then part)


Data format requirements
========================

If you want to apply the rules on internal data sets, then you have to make sure that the data is in the correct format.

Solvency 2
----------

- the template name follows the standard Solvency 2 code, for example S.02.01.02.01 and S.28.02.01.02;

- the file names of the individual templates is the template name plus an extension (.csv or .pickle), for example S.01.02.07.01.pickle;

- the file name of all closed axes templates combined is the instance file name plus an extension, for example qrs_240_instance.pickle (the example instance for qrs);

- the column names and the index names for all templates have the following format: {reporting template name},R????,C???? or {reporting template name},C????, depending on the definition; for example S.02.01.02.01,R0030,C0010 or S.06.02.01.01,C0040;
 
FTK
---

- the template name follows the standard FTK code with prefix FTK, for example FTK.K101-1 or FTK.K209B;

- the file names of the individual templates is the template name plus an extension (.csv or .pickle), for example FTK.K101-1.pickle;

- the file name of all closed axes templates combined is the instance file name plus an extension, for example DNB-NR_FTK-2019-06_2019-12-31_MOD_FTK-BEL.pickle (the example instance for FTK-BEL);

- the column names and the index names for all templates have the following format: {reporting template name},R???,C??? or {reporting template name},C???, depending on the definition; for example FTK.K101-1,R010,C010 or FTK.K209B,C150;

