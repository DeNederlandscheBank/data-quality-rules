import pandas as pd  # dataframes
import numpy as np  # mathematical functions, arrays and matrices
from os import listdir, walk, makedirs, environ
from os.path import isfile, join, exists, basename, isdir
import data_patterns  # evaluation of patterns
import regex as re  # regular expressions
from pprint import pprint  # pretty print
import logging
import click
import sys

ENTRYPOINTS = ['QRS', 'ARS']
DATAPOINTS_PATH = join('data', 'datapoints')
INSTANCES_DATA_PATH = join('data', 'instances') #path of folder with converted xbrl-instance data
RULES_PATH = join('solvency2-rules')
RESULTS_PATH = join('results') 

logging.basicConfig(filename = join(RESULTS_PATH, 'rules.log'),level = logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

reports: list = [f for f in listdir(INSTANCES_DATA_PATH) if isdir(join(INSTANCES_DATA_PATH, f))]
report_choices: str = "\n".join([str(idx)+": "+item
                                 for idx, item in enumerate(reports) if item!='actual'])

@click.command()
@click.option('--entrypoint', default=1, prompt='Select entrypoint:\n1: QRS\n2: ARS\n')
@click.option('--report_dir', default=1, prompt=report_choices+"\n")
@click.option('--output_type', default=1, prompt='Select output type:\n1: exceptions\n2: confirmation\n3: both')
@click.option('--output_dir', default=RESULTS_PATH, prompt='Select output directory')

def main(entrypoint, report_dir, output_type, output_dir):
    additionalRules(entrypoint, report_dir, output_type, output_dir)

def additionalRules(entrypoint, report_dir, output_type, output_dir):

    df_datapoints = pd.read_csv(join(DATAPOINTS_PATH, ENTRYPOINTS[entrypoint] + '.csv'), sep=";").fillna("")  # load file to dataframe

    tables_complete_set = df_datapoints.tabelcode.sort_values().unique().tolist()
    tables_reported = [table for table in tables_complete_set if isfile(join(INSTANCES_DATA_PATH, reports[report_dir], table + '.pickle'))]
    tables_not_reported = [table for table in tables_complete_set if table not in tables_reported]

    df_closed_axis = pd.read_pickle(join(INSTANCES_DATA_PATH, reports[report_dir], reports[report_dir]+'.pickle'))
    tables_closed_axis = sorted(list(set(x[:13] for x in df_closed_axis.columns)))

    dict_open_axis = dict()
    tables_open_axis = [table for table in tables_reported if table not in tables_closed_axis]

    for table in tables_open_axis:
        df = pd.read_pickle(join(INSTANCES_DATA_PATH, reports[report_dir], table + '.pickle'))
        # Identify which columns within the open-axis table make a table row unique (index-columns):
        index_columns_open_axis = [col for col in list(df.index.names) if col not in ['entity','period']]
        # Duplicate index-columns to data columns:
        df.reset_index(level=index_columns_open_axis, inplace=True)
        for i in range(len(index_columns_open_axis)):
            df['index_col_' + str(i)] = df[index_columns_open_axis[i]].astype(str)
            df.set_index(['index_col_' + str(i)], append=True, inplace=True)
        dict_open_axis[table] = df 

    all_datapoints = [x.replace(',,',',') for x in 
                      list(df_datapoints['tabelcode'] + ',' + df_datapoints['rij'] + ',' + df_datapoints['kolom'])]
    all_datapoints_closed = [x for x in all_datapoints if x[:13] in tables_closed_axis]
    all_datapoints_open = [x for x in all_datapoints if x[:13] in tables_open_axis]

    # add not reported datapoints to the dataframe with data from closed axis tables:
    for col in [column for column in all_datapoints_closed if column not in list(df_closed_axis.columns)]:
        df_closed_axis[col] = np.nan
    df_closed_axis.fillna(0, inplace = True)

    # string values to uppercase
    df_closed_axis = df_closed_axis.applymap(lambda s:s.upper() if type(s) == str else s)

    for table in [table for table in dict_open_axis.keys()]:
        all_datapoints_table = [x for x in all_datapoints_open if x[:13] == table]
        for col in [column for column in all_datapoints_table if column not in list(dict_open_axis[table].columns)]:
            dict_open_axis[table][col] = np.nan
        dict_open_axis[table].fillna(0, inplace = True)
        dict_open_axis[table] = dict_open_axis[table].applymap(lambda s:s.upper() if type(s) == str else s)

    df_patterns = pd.read_excel(join(RULES_PATH, ENTRYPOINTS[entrypoint].lower()+'_patterns_additional_rules.xlsx'), 
                                engine='openpyxl').fillna("").set_index('index')

    df_patterns_closed_axis = df_patterns.copy()
    df_patterns_closed_axis = df_patterns_closed_axis[df_patterns_closed_axis['pandas ex'].apply(
        lambda expr: not any(table in expr for table in tables_not_reported) 
        and not any(table in expr for table in tables_open_axis))]

    miner = data_patterns.PatternMiner(df_patterns=df_patterns_closed_axis)
    df_results_closed_axis = miner.analyze(df_closed_axis)

    df_patterns_open_axis = df_patterns.copy()
    df_patterns_open_axis = df_patterns_open_axis[df_patterns_open_axis['pandas ex'].apply(
        lambda expr: any(table in expr for table in tables_open_axis))]
    df_patterns_open_axis = df_patterns_open_axis[df_patterns_open_axis['pandas ex'].apply(
        lambda expr: len(set(re.findall('S.\d\d.\d\d.\d\d.\d\d',expr)))) == 1]

    output_open_axis = {}  # dictionary with input and results per table
    for table in tables_open_axis:  # loop through open-axis tables
        if df_patterns_open_axis['pandas ex'].apply(lambda expr: table in expr).sum() > 0:  # check if there are patterns
            info = {}
            info['data'] = dict_open_axis[table]  # select data
            info['patterns'] = df_patterns_open_axis[df_patterns_open_axis['pandas ex'].apply(
                lambda expr: table in expr)]  # select patterns
            miner = data_patterns.PatternMiner(df_patterns=info['patterns'])
            info['results'] = miner.analyze(info['data'])  # evaluate patterns
            output_open_axis[table] = info

    # Function to transform results for open-axis tables, so it can be appended to results for closed-axis tables
    # The 'extra' index columns are converted to data columns
    def transform_results_open_axis(df):
        if df.index.nlevels > 2:
            reset_index_levels = list(range(2, df.index.nlevels))
            df = df.reset_index(level=reset_index_levels)
            rename_columns = {}
            for x in reset_index_levels:
                rename_columns['level_' + str(x)] = 'id_column_' + str(x - 1)
            df.rename(columns=rename_columns, inplace=True)
        return df

    df_results = df_results_closed_axis.copy()  # results for closed axis tables
    for table in list(output_open_axis.keys()):  # for all open axis tables with rules -> append and sort results
        df_results = transform_results_open_axis(output_open_axis[table]['results']).append(df_results, sort=False).sort_values(by=['pattern_id']).sort_index()

    list_col_order = []
    for i in range(1, len([col for col in list(df_results.columns) if col[:10] == 'id_column_']) + 1):
        list_col_order.append('id_column_' + str(i))
    list_col_order.extend(col for col in list(df_results.columns) if col not in list_col_order)
    df_results = df_results[list_col_order]

    # To save all results use df_results
    # To save all exceptions use df_results['result_type']==False 
    # To save all confirmations use df_results['result_type']==True

    output_dir = join(output_dir, reports[report_dir])
    if not exists(output_dir):
        makedirs(output_dir)
    df_results[df_results['result_type']==False].to_excel(join(output_dir, "results.xlsx"))


if __name__ == "__main__":
    sys.exit(main())

