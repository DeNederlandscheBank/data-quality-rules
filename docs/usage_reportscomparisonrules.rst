
Evaluating rule sets for report comparison
==========================================

The idea of the report comparison rules is a bit more difficult than the additional validation rules from DNB and the financial data validation rules. The report comparison rule sets evaluate differences between two report sets (for example ARS-2020 and ARS-2019), whereas the latter rule sets evaluate one single report set (for example QRS-2020-Q1). 

The goal is to detect differences in whether data points are reported (datapoint that were included in one period and not in the other) and to detect significant changes in the values of data point between two periods. As such it is not unusual that some data points are included in one period and not in another, and that some data points change significantly between two periods. Because of that we only included datapoints for which it is highly unusual that they are included in one period and not in the other (< 5% of previous reports), and datapoints for which it is highly unusual (< 5% of previous reports) that they changes significantly over two periods (> 10% change).

You can compare two quarterly reports or two annual reports, but you cannot compare a quarterly report with an annual report, even if they have corresponding data points.

To run the additional rules use::

  python solvency2-rules\apply3.py

The command line interface will ask the rule set that you want to apply (compare two QRS-reports or compare two ARS-reports), the entity category (Schade, Herverzekeraar, Leven), the two directories where the two reports are located and the output directory. You can also run the script with command line arguments --rule_set, --entity_category, --report_dir_1, --report_dir_2, output_type and output_dir.

With output_type you can choose to output confirmations only, exceptions only, or all results.

You cannot test these rules with the example instances provided by EIOPA because the instances of subsequent periods contain different LEI-codes.

