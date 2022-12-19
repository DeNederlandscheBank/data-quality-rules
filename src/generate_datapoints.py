import sys
import pandas as pd
from os import listdir, walk, makedirs, environ, remove
from os.path import isfile, join, exists, basename, isdir
from datetime import datetime
import click
import pickle
import re
from tqdm import tqdm
import csv

# the instances you want to use should be in data/instances and should already have been converted to a pickle

DATAPOINTS_PATH = join('data', 'datapoints')
INSTANCES_PATH = join('data', 'instances')
LANGUAGE = "en-GB"
euRCcode = 'http://www.eurofiling.info/xbrl/role/rc-code'

environ['XDG_CONFIG_HOME'] = DATAPOINTS_PATH

instances: list = [f for f in listdir(INSTANCES_PATH) if '.' not in f]
instance_choices: str = "Choose instance folder:\n"+"\n".join([str(idx)+": "+item
                                 for idx, item in enumerate(instances) if item!='actual'])

@click.command()
@click.option('--instance', default=0, prompt=instance_choices)
@click.option('--output', default=DATAPOINTS_PATH, prompt="output directory")
@click.option('--verbose_labels', default=False, prompt="verbose labels")

def main(instance, output, verbose_labels):

    if instance not in range(0, len(instances)):
        print("ERROR: incorrect instance choice.")
        return 0

    instance = instances[instance]
    instance_folder = join(INSTANCES_PATH, instance)
    instance_files = [f for f in listdir(instance_folder) if isfile(join(instance_folder, f)) and f[-6:] == 'pickle' and ((f[0:2].lower() == 's.') or bool(re.match(r't\d[a-z]?.', f.lower())))]

    ### This does yet not include open axis tables
    # Loop over the files within the instance
    master_instance = ['tabelcode;datapunt;rij;kolom']
    for file in tqdm(instance_files):
        # Load pickle
        with open(join(instance_folder, file), 'rb') as handle:
            df_file = pickle.load(handle)
        
        # List labels of columns
        df_file.reset_index(inplace=True)
        df_file.set_index(['entity', 'period'], inplace=True)
        labels_file = list(df_file.columns)
        num_file = len(labels_file)
        
        # Determine the structure of the column labels
        if file[0:2].lower() == 's.':
            elements_labels = [(re.findall("([Ss].\d\d.\d\d.\d\d.\d\d),(.*?)$", lab) + [""])[0] for lab in labels_file]
            tables_file = [el[0] for el in elements_labels]
            datapoints_file = [el[1].replace(",", "") for el in elements_labels]
            rows_file = [(re.findall("([Rr]\d\d\d\d)", el[1]) + [""])[0] for el in elements_labels]
            cols_file = [(re.findall("([Cc]\d\d\d\d)", el[1]) + [""])[0] for el in elements_labels]
        elif bool(re.match(r't\d[a-z]?.', file.lower())):
            elements_labels = [(re.findall("([Tt]\d[A-Za-z]?),(.*?)$", lab) + [""])[0] for lab in labels_file]
            tables_file = [el[0] for el in elements_labels]
            datapoints_file = [el[1].replace(",", "") for el in elements_labels]
            rows_file = [(re.findall("([Rr]\d\d\d)", el[1]) + [""])[0] for el in elements_labels]
            cols_file = [(re.findall("([Cc]\d\d\d)", el[1]) + [""])[0] for el in elements_labels]
        master_instance += [tables_file[i] + ";" + datapoints_file[i] + ";" + rows_file[i] + ";" + cols_file[i] for i in range(num_file)]

    # Export as csv
    with open(join(output, instance[:3].upper() + ".csv"), 'w', newline = '') as list_file:
        wr = csv.writer(list_file, quoting = csv.QUOTE_NONE)
        wr.writerows([[i] for i in master_instance])

if __name__ == "__main__":
    sys.exit(main())
