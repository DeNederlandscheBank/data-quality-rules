Converting XBRL instances to Pandas and CSV
===========================================

We use a command line interface to convert XBRL instance to Pandas and CSV. You can run the XBRL to Pandas and CSV converter with::

	python src\instance2csv.py

The script will ask for the desired taxonomy, instance-file, output directory, and whether you want verbose column names instead of rc-codes (row-column codes). To evaluate rules you need the templates with the rc-codes. You can also run the script with command line arguments --taxo, --instance, --output and --verbose_labels.

Make sure you use the corresponding version of the taxonomy for your instance.

For each template in the XBRL instance the results are exported to a Pandas pickle-file and a csv-file. A Pandas pickle-file maintains the correct indices, whereas the csv does not, so if you want to access the data read the pickle-files. 

The csv-files and the pickle-files are stored in a subdirectory identical to the name of the XBRL-instance (without extension).

All closed axis tables in the XBRL-instance are combined and stored in one pickle-file in the subdirectory where all pickle-files are stored (with the name of the XBRL-instance).

The easiest way to access the data of a separate template is to read the corresponding pickle-file with::

	df = pd.read_pickle(filename)
