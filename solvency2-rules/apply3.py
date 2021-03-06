import pandas as pd
import numpy as np
import math
from os import listdir, walk, makedirs, environ
from os.path import isfile, join, exists, basename, isdir
import re
import logging
import data_patterns
import click
import sys
import datetime

DECIMALS = 0
RULES_PATH = join('solvency2-rules')
INSTANCES_DATA_PATH = join('data', 'instances') #path of folder with converted xbrl-instance data
RESULTS_PATH = join('results')
DATA_PATH = join('data')
DATAPOINTS_PATH = join('data', 'datapoints')

logging.basicConfig(filename = join(RESULTS_PATH, 'rule-set-3.log'),level = logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

reports: list = [f for f in listdir(INSTANCES_DATA_PATH) if isdir(join(INSTANCES_DATA_PATH, f))]
report_choices: str = "\n".join([str(idx)+": "+item
                                 for idx, item in enumerate(reports) if item!='actual'])

categories: list = ["Schade", "Herverzekeraar", "Leven"]
category_choices: str = "Select category: \n"+", ".join([str(idx)+": "+item
                                 for idx, item in enumerate(categories)])

@click.command()
@click.option('--rule_set', default=1, prompt="1: Patterns between periods QRS\n2: Patterns between periods ARS")
@click.option('--entity_category', default=0, prompt=category_choices)
@click.option('--report_dir_1', default=0, prompt="Select report 1:\n"+report_choices)
@click.option('--report_dir_2', default=1, prompt="Select report 2:\n"+report_choices)
@click.option('--output_type', default=1, prompt='Select output type:\n1: exceptions\n2: confirmation\n3: both')
@click.option('--output_dir', default=RESULTS_PATH, prompt='output directory')

def main(rule_set, entity_category, report_dir_1, report_dir_2, output_type, output_dir):

    if rule_set not in [1, 2]:
        print("ERROR: incorrect rule set choice.")
        return 0
    if entity_category not in [0, 1, 2]:
        print("ERROR: incorrect entity category choice.")
        return 0
 
    output_dir = join(output_dir, reports[report_dir_1])
    report_dir_1 = reports[report_dir_1]
    report_dir_2 = reports[report_dir_2]

    if rule_set == 1:
        between_qrs(report_dir_1, report_dir_2, output_type, output_dir, entity_category)
    elif rule_set == 2:
        between_ars(report_dir_1, report_dir_2, output_type, output_dir, entity_category)


def between_ars(report_dir_1, report_dir_2, output_type, output_dir, entity_category):

    # We start with importing the (t-1)-t rules that are applicable to two consecutive periods. 
    # We import a set of rules used to evaluate year data and a set of rules for quarter data.

    dfr_ARS = pd.read_excel(join(RULES_PATH,'S2_betweenperiods_ARS.xlsx'), engine='openpyxl')

    report_dirs_ARS = [report_dir_1, report_dir_2]

    #Capitalize row-column references:
    column_replace = set([column for sublist in [row for row in dfr_ARS['pandas ex'].str.findall(r'c\d\d\d\d')] for column in sublist])
    for ref in column_replace:
        dfr_ARS.replace(to_replace=ref, value=ref.capitalize(), inplace=True, regex=True)
    column_replace = set([column for sublist in [row for row in dfr_ARS['pandas ex'].str.findall(r'r\d\d\d\d')] for column in sublist])
    for ref in column_replace:
        dfr_ARS.replace(to_replace=ref, value=ref.capitalize(), inplace=True, regex=True)

    df_datapoints = pd.read_csv(join(DATAPOINTS_PATH, 'ARS.csv'), sep=";").fillna("")  # load file to dataframe
    dft = pd.DataFrame()
    for instance in report_dirs_ARS:
        df_closed_axis = pd.DataFrame()
        tables_closed_axis = []  # for listing all input tables with closed axis
        tables_complete_set = df_datapoints.tabelcode.sort_values().unique().tolist()  # list of all ARS tables
        tables = [table for table in tables_complete_set 
            if isfile(join(INSTANCES_DATA_PATH, instance, table + '.pickle'))]  # ARS tables found in the specified instance path
        for table in [table for table in tables if table not in ['S.14.01.01.04','S.30.03.01.01']]:  #tables:
            if isfile(join(INSTANCES_DATA_PATH, instance, table + '.pickle')):
                df = pd.read_pickle(join(INSTANCES_DATA_PATH,instance, table + '.pickle'))  # read dataframe
            else:
                continue   
            if df.index.nlevels > 2:  # if more than 2 indexes (entity, period), then the table has an open axis
                continue
            else:  # closed axis
                tables_closed_axis.append(table)  # add to relevant list
                # Add table to dataframe with all data from closed axis tables
                if len(df_closed_axis) == 0:  # no data yet --> copy dataframe
                    df_closed_axis = df.copy()
                else:  # join to existing dataframe
                    df_closed_axis = df_closed_axis.join(df)
        if len(dft) == 0:  # no data yet 
            dft = df_closed_axis
        else:  # join to existing dataframe
            dft = dft.append(df_closed_axis)

    # Next we import the reporting data. We import the data of two consecutive periods. 
    # In the tutorial 'Convert XBRL-instances to CSV, HTML and pickles' the XBRL-instances 
    # are converted to pickle files per template. The pickle files are written to the 
    # data/instances folder. The rules are applicable to all tables with closed axis. We 
    # import these pickle files. When comparing two periods it can be the case that two 
    # different taxonomies are applicable. The right taxonomy has to be selected in the 
    # tutorial 'Convert XBRL-instances to CSV, HTML and pickles' to convert the 
    # XBRL-instance properly. 

    # The list _instances_ARS_ contains the names of the folders with the converted 
    # XBRL-instance for yearly data. The list _instances_QRS_ contains the names of the 
    # folders with the converted XBRL-instance for two consecutive quarters. Finally, we 
    # also have to define the category of the insurer. The rules are set-up for each type 
    # of insurer separately.

    dft = dft.reset_index()
    dft['categorie'] = categories[entity_category]
    numerical_columns = ['entity', 'period', 'categorie'] + [dft.columns[c] for c in range(len(dft.columns))
                            if ((dft.dtypes[c] == 'float64') or (dft.dtypes[c] == 'int64'))] #select only numerical columns

    df_ARS = dft[numerical_columns].copy()
    df_ARS['period'] = df_ARS['period'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d')) #convert to datetime
    df_ARS.fillna(0, inplace=True)

    miner = data_patterns.PatternMiner(df_patterns=dfr_ARS)
    miner.df_data = df_ARS
    miner.metapatterns = {'cluster': 'categorie'}
    miner.convert_to_time(['entity', 'categorie'], 'period')
    miner.df_data = miner.df_data.reset_index()

    results = miner.analyze()

    if not exists(output_dir):
        makedirs(output_dir)

    if output_type == 1:
        results = result[results['result_type']==False]
    elif output_type == 2:
        results = results[results['result_type']==True]

    if len(results) > 0:
        results.to_excel(join(output_dir, "rule-set-3-results_ARS.xlsx"), engine='openpyxl')

def between_qrs(report_dir_1, report_dir_2, output_type, output_dir, entity_category):

    # We start with importing the (t-1)-t rules that are applicable to two consecutive periods. 
    # We import a set of rules used to evaluate year data and a set of rules for quarter data.

    dfr_QRS = pd.read_excel(join(RULES_PATH,'S2_betweenperiods_QRS.xlsx'), engine='openpyxl')

    report_dirs_QRS = [report_dir_1, report_dir_2]

    #Capitalize row-column references:
    column_replace = set([column for sublist in [row for row in dfr_QRS['pandas ex'].str.findall(r'c\d\d\d\d')] for column in sublist])
    for ref in column_replace:
        dfr_QRS.replace(to_replace=ref, value=ref.capitalize(), inplace=True, regex=True)
    column_replace = set([column for sublist in [row for row in dfr_QRS['pandas ex'].str.findall(r'r\d\d\d\d')] for column in sublist])
    for ref in column_replace:
        dfr_QRS.replace(to_replace=ref, value=ref.capitalize(), inplace=True, regex=True)

    df_datapoints = pd.read_csv(join(DATAPOINTS_PATH, 'QRS.csv'), sep=";").fillna("")  # load file to dataframe
    dft = pd.DataFrame()
    for instance in report_dirs_QRS:
        df_closed_axis = pd.DataFrame()
        tables_closed_axis = []  # for listing all input tables with closed axis
        tables_complete_set = df_datapoints.tabelcode.sort_values().unique().tolist()  # list of all QRS tables
        tables = [table for table in tables_complete_set 
            if isfile(join(INSTANCES_DATA_PATH, instance, table + '.pickle'))]  # QRS tables found in the specified instance path
        for table in [table for table in tables if table not in ['S.14.01.01.04','S.30.03.01.01']]:  #tables:
            if isfile(join(INSTANCES_DATA_PATH, instance, table + '.pickle')):
                df = pd.read_pickle(join(INSTANCES_DATA_PATH,instance, table + '.pickle'))  # read dataframe
            else:
                continue   
            if df.index.nlevels > 2:  # if more than 2 indexes (entity, period), then the table has an open axis
                continue
            else:  # closed axis
                tables_closed_axis.append(table)  # add to relevant list
                # Add table to dataframe with all data from closed axis tables
                if len(df_closed_axis) == 0:  # no data yet --> copy dataframe
                    df_closed_axis = df.copy()
                else:  # join to existing dataframe
                    df_closed_axis = df_closed_axis.join(df)
        if len(dft) == 0:  # no data yet 
            dft = df_closed_axis
        else:  # join to existing dataframe
            dft = dft.append(df_closed_axis)

    # Next we import the reporting data. We import the data of two consecutive periods. 
    # In the tutorial 'Convert XBRL-instances to CSV, HTML and pickles' the XBRL-instances 
    # are converted to pickle files per template. The pickle files are written to the 
    # data/instances folder. The rules are applicable to all tables with closed axis. We 
    # import these pickle files. When comparing two periods it can be the case that two 
    # different taxonomies are applicable. The right taxonomy has to be selected in the 
    # tutorial 'Convert XBRL-instances to CSV, HTML and pickles' to convert the 
    # XBRL-instance properly. 

    # The list _instances_QRS_ contains the names of the folders with the converted 
    # XBRL-instance for yearly data. The list _instances_QRS_ contains the names of the 
    # folders with the converted XBRL-instance for two consecutive quarters. Finally, we 
    # also have to define the category of the insurer. The rules are set-up for each type 
    # of insurer separately.

    dft = dft.reset_index()
    dft['categorie'] = categories[entity_category]
    numerical_columns = ['entity','period','categorie'] + [dft.columns[c] for c in range(len(dft.columns))
                            if ((dft.dtypes[c] == 'float64') or (dft.dtypes[c] == 'int64'))] #select only numerical columns
    df_QRS = dft[numerical_columns].copy()
    df_QRS['period'] = df_QRS['period'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d')) #convert to datetime
    df_QRS.fillna(0, inplace=True)

    miner = data_patterns.PatternMiner(df_patterns=dfr_QRS)
    miner.df_data = df_QRS
    miner.metapatterns = {'cluster': 'categorie'}
    miner.convert_to_time(['entity', 'categorie'], 'period', set_year = False)
    miner.df_data = miner.df_data.reset_index()

    results = miner.analyze()

    if not exists(output_dir):
        makedirs(output_dir)

    results.to_excel(join(output_dir, "rule-set-3-results_QRS.xlsx"), engine='openpyxl')


if __name__ == "__main__":
    sys.exit(main())

