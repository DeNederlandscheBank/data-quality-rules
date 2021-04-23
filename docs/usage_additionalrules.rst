
Evaluating additional Rules
===========================

To run the additional rules use::

	python solvency2-rules\apply1.py

You can run DNBs additional Rules for the following Solvency II reports

- Annual Reporting Solo (ARS); and

- Quarterly Reporting Solo (QRS)

The command line interface will ask the entrypoint (ARS or QRS), the directory where the reports (in pickle-files) are stored, the output type (confirmation, exceptions or both) and the output directory.  You can also run the script with command line arguments --entrypoint, --report_dir, --output_type and --output_dir.

We distinguish 2 types of tables

- With a closed-axis, e.g. the balance sheet: an entity reports only 1 balance sheet per period

- With an open-axis, e.g. the list of assets: an entity reports several 'rows of data' in the relevant table

To evaluate the patterns we use a PatternMiner-object (part of the data_patterns package), and run the analyze function.

