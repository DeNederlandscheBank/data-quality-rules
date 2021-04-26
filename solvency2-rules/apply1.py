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
@click.option('--report_dir', default=0, prompt=report_choices+"\n")
@click.option('--output_type', default=1, prompt='Select output type:\n1: exceptions\n2: confirmation\n3: both')
@click.option('--output_dir', default=RESULTS_PATH, prompt='Select output directory')

def main(entrypoint, report_dir, output_type, output_dir):

    if entrypoint not in [1, 2]:
        print("ERROR: incorrect entrypoint choice.")
        return 0
    if output_type not in [1, 2, 3]:
        print("ERROR: incorrect output type choice.")
        return 0

    additionalRules(entrypoint, report_dir, output_type, output_dir)

def additionalRules(entrypoint, report_dir, output_type, output_dir):

    # In the data/datapoints directory there is a file for both ARS and QRS in which 
    # all possible datapoints are listed (simplified taxonomy).  
    # We will use this information to add all unreported datapoints to the imported data.

    # Read possible datapoints

    df_datapoints = pd.read_csv(join(DATAPOINTS_PATH, ENTRYPOINTS[entrypoint-1] + '.csv'), sep=";").fillna("")  # load file to dataframe

    # Read data

    # First we gather some general information:
    # - list of all possible reported tables
    # - list of all reported tables
    # - list of all tables that have not been reported

    tables_complete_set = df_datapoints.tabelcode.sort_values().unique().tolist()
    tables_reported = [table for table in tables_complete_set if isfile(join(INSTANCES_DATA_PATH, reports[report_dir], table + '.pickle'))]
    tables_not_reported = [table for table in tables_complete_set if table not in tables_reported]

    # We use this closed axis dataframe for evaluating the patterns on closed-axis tables.
    df_closed_axis = pd.read_pickle(join(INSTANCES_DATA_PATH, reports[report_dir], reports[report_dir]+'.pickle'))
    tables_closed_axis = sorted(list(set(x[:13] for x in df_closed_axis.columns)))

    # For open-axis tables we create a dictionary with all data per table.  
    # Later we will evaluate the additional rules on each seperate table in this dictionary.
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

    # Clean data

    # We have to make 2 modifications on the data:
    # 1. Add unreported datapoints  
    # so rules (partly) pointing to unreported datapoints can still be evaluated
    # 2. Change string values to uppercase  
    # because the additional rules are defined using capital letters for textual comparisons 

    all_datapoints = [x.replace(',,',',') for x in 
                      list(df_datapoints['tabelcode'] + ',' + df_datapoints['rij'] + ',' + df_datapoints['kolom'])]
    all_datapoints_closed = [x for x in all_datapoints if x[:13] in tables_closed_axis]
    all_datapoints_open = [x for x in all_datapoints if x[:13] in tables_open_axis]

    # Closed-axis tables

    # add not reported datapoints to the dataframe with data from closed axis tables:
    for col in [column for column in all_datapoints_closed if column not in list(df_closed_axis.columns)]:
        df_closed_axis[col] = np.nan
    df_closed_axis.fillna(0, inplace = True)
    # string values to uppercase
    df_closed_axis = df_closed_axis.applymap(lambda s:s.upper() if type(s) == str else s)

    # Open-axis tables

    for table in [table for table in dict_open_axis.keys()]:
        all_datapoints_table = [x for x in all_datapoints_open if x[:13] == table]
        for col in [column for column in all_datapoints_table if column not in list(dict_open_axis[table].columns)]:
            dict_open_axis[table][col] = np.nan
        dict_open_axis[table].fillna(0, inplace = True)
        dict_open_axis[table] = dict_open_axis[table].applymap(lambda s:s.upper() if type(s) == str else s)

    # DNBs additional validation rules are published as an Excel file on the 
    # DNB statistics website.  
    # We included the Excel file in the project under data/downloaded files.

    # The rules are already converted to a syntax Python can interpret, using the notebook: 'Convert DNBs Additional Validation Rules to Patterns'.  
    # In the next line of code we read these converted rules (patterns).

    df_patterns = pd.read_excel(join(RULES_PATH, ENTRYPOINTS[entrypoint-1].lower()+'_patterns_additional_rules.xlsx'), 
                                engine='openpyxl').fillna("").set_index('index')

    # Evaluate rules

    # To be able to evaluate the rules for closed-axis tables, we need to filter out:
    # - patterns for open-axis tables; and
    # - patterns pointing to tables that are not reported.

    df_patterns_closed_axis = df_patterns.copy()
    df_patterns_closed_axis = df_patterns_closed_axis[df_patterns_closed_axis['pandas ex'].apply(
        lambda expr: not any(table in expr for table in tables_not_reported) 
        and not any(table in expr for table in tables_open_axis))]

    # We now have:
    # - the data for closed-axis tables in a dataframe;
    # - the patterns for closed-axis tables in a dataframe.

    # To evaluate the patterns we need to create a 'PatternMiner' (part of the data_patterns 
    # package), and run the analyze function.

    miner = data_patterns.PatternMiner(df_patterns=df_patterns_closed_axis)
    df_results_closed_axis = miner.analyze(df_closed_axis)

    # First find the patterns defined for open-axis tables

    df_patterns_open_axis = df_patterns.copy()
    df_patterns_open_axis = df_patterns_open_axis[df_patterns_open_axis['pandas ex'].apply(
        lambda expr: any(table in expr for table in tables_open_axis))]

    # Patterns involving multiple open-axis tables are not yet supported

    df_patterns_open_axis = df_patterns_open_axis[df_patterns_open_axis['pandas ex'].apply(
        lambda expr: len(set(re.findall('S.\d\d.\d\d.\d\d.\d\d',expr)))) == 1]

    # Next we loop through the open-axis tables en evaluate the corresponding patterns on the data

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

    # To output the results in a single file, we want to combine the results 
    # for closed-axis and open-axis tables

    # Function to transform results for open-axis tables, so it can be appended 
    # to results for closed-axis tables
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
    # Change column order so the dataframe starts with the identifying columns:

    list_col_order = []
    for i in range(1, len([col for col in list(df_results.columns) if col[:10] == 'id_column_']) + 1):
        list_col_order.append('id_column_' + str(i))
    list_col_order.extend(col for col in list(df_results.columns) if col not in list_col_order)
    df_results = df_results[list_col_order]

    output_dir = join(output_dir, reports[report_dir])
    if not exists(output_dir):
        makedirs(output_dir)

    # The dataframe df_results contains all output of the evaluation of the validation rules. 

    if output_type == 1:
        if len(df_results[df_results['result_type']==False]) > 0:
            df_results[df_results['result_type']==False].to_excel(join(output_dir, "results.xlsx"))
    elif output_type == 2:
        if len(df_results[df_results['result_type']==True]) > 0:
            df_results[df_results['result_type']==True].to_excel(join(output_dir, "results.xlsx"))
    elif output_type == 3:
        df_results.to_excel(join(output_dir, "results.xlsx"))

if __name__ == "__main__":
    sys.exit(main())

