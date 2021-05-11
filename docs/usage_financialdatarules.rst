Evaluating financial Data Rules
===============================

To run the financial data rules use::

  python solvency2-rules/apply2.py

The command line interface will ask the directory where the reports (in pickle-files) are stored and the output directory. You can also run the script with command line arguments --report_dir, output_type and --output_dir.

With output_type you can choose to output confirmations only, exceptions only, or all results.

If, given the output_type, no output was generated (for example, no exceptions when the output type is exceptions only), then no Excel output file is generated.

The rules are related to the following tables:

- S.06.02.01.01 (Information on positions held)

- S.06.02.01.02 (Information on assets)

- S.06.02.01.01 (Information on positions held) and S.06.02.01.02 (Information on assets)

- S.08.01.01.01 (Information on positions held) and S2.08.01.01.02 (Information on derivatives)

- S.08.01.01.02 (Information on derivatives)

