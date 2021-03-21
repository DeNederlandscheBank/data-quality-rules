import pandas as pd
import numpy as np
import math
from os import listdir, walk, makedirs, environ
from os.path import isfile, join, exists, basename, isdir
import re
from src import Evaluator
import logging
import data_patterns
import click
import sys

DECIMALS = 0
RULES_PATH = join('solvency2-rules')
INSTANCES_DATA_PATH = join('data', 'instances') #path of folder with converted xbrl-instance data
RESULTS_PATH = join('results')
DATA_PATH = join('data')
DATAPOINTS_PATH = join('data', 'datapoints')

logging.basicConfig(filename = join(RESULTS_PATH, 'rules.log'),level = logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

reports: list = [f for f in listdir(INSTANCES_DATA_PATH) if isdir(join(INSTANCES_DATA_PATH, f))]
report_choices: str = "\n".join([str(idx)+": "+item
                                 for idx, item in enumerate(reports) if item!='actual'])

@click.command()
@click.option('--report_dir', default=5, prompt=report_choices)
@click.option('--output_dir', default=RESULTS_PATH, prompt='output directory')

def main(report_dir, output_dir):
    financial(report_dir, output_dir)

def financial(report_dir, output_dir):

    output_dir = join(output_dir, reports[report_dir])
    report_dir = join(INSTANCES_DATA_PATH, reports[report_dir])

    def capitalize_row_columns(df):
        column_replace = set([column for sublist in [row for row in df['pandas ex'].str.findall(r'c\d\d\d\d')] for column in sublist])
        for ref in column_replace:
            df.replace(to_replace=ref, value=ref.capitalize(), inplace=True, regex=True)
        return df

    dfr_s06 = capitalize_row_columns(pd.read_excel(join(RULES_PATH, 'S2_06_02.xlsx'), engine='openpyxl'))
    dfr_s06_2 = capitalize_row_columns(pd.read_excel(join(RULES_PATH,'S2_06_02_01_02.xlsx'), engine='openpyxl'))
    dfr_s06_1 = capitalize_row_columns(pd.read_excel(join(RULES_PATH,'S2_06_02_01_01.xlsx'), engine='openpyxl'))
    dfr_s08 = capitalize_row_columns(pd.read_excel(join(RULES_PATH,'S2_08_01_01.xlsx'), engine='openpyxl'))
    dfr_s08_2 = capitalize_row_columns(pd.read_excel(join(RULES_PATH,'S2_08_01_01_02.xlsx'), engine='openpyxl'))

    df_s06_1 = pd.read_pickle(join(report_dir,'S.06.02.01.01.pickle')).fillna(0).reset_index()
    df_s06_1['S.06.02.01.01,C0040A'] = df_s06_1['S.06.02.01.01,C0040']

    listt = list(df_s06_1['S.06.02.01.01,C0040A'])
    for i in listt:
        lenn = len(df_s06_1[df_s06_1['S.06.02.01.01,C0040A']==i])
        if lenn > 1:
            list_ind = list(df_s06_1.loc[df_s06_1['S.06.02.01.01,C0040A']==i].index)
            temp = 0
            for j in list_ind[1:]:
                temp=temp+1
                df_s06_1['S.06.02.01.01,C0040A'].iloc[j] = df_s06_1['S.06.02.01.01,C0040A'].iloc[j] + '_' + str(temp)
    df_s06_1 = df_s06_1.set_index(['entity', 'period', 'S.06.02.01.01,C0040A'])

    df_s06_2 = pd.read_pickle(join(report_dir, 'S.06.02.01.02.pickle')).fillna(0).reset_index()
    df_s06_2 = df_s06_2.set_index(['entity', 'period', 'S.06.02.01.02,C0040'])
    df_s06_2['S.06.02.01.02,C0040'] = df_s06_2.index.get_level_values(2)

    df_s06 = pd.merge(pd.read_pickle(join(report_dir,'S.06.02.01.01.pickle')).reset_index(), 
                      pd.read_pickle(join(report_dir, 'S.06.02.01.02.pickle')).reset_index(),
                      how='inner', 
                      left_on=['entity','period','S.06.02.01.01,C0040'], 
                      right_on=['entity','period','S.06.02.01.02,C0040']).set_index(['entity', 'period', 'S.06.02.01.01,C0040'])
    df_s06 = df_s06.fillna(0).reset_index()
    df_s06['S.06.02.01.02,C0040A'] = df_s06['S.06.02.01.02,C0040']
    listt=list(df_s06['S.06.02.01.02,C0040A'])
    for i in listt:
        lenn = len(df_s06[df_s06['S.06.02.01.02,C0040A']==i])
        if lenn > 1:
            list_ind = list(df_s06.loc[df_s06['S.06.02.01.02,C0040A']==i].index)
            temp = 0
            for j in list_ind[1:]:
                temp=temp+1
                df_s06['S.06.02.01.02,C0040A'].iloc[j] = df_s06['S.06.02.01.02,C0040A'].iloc[j] + '_' + str(temp)
    df_s06 = df_s06.set_index(['entity', 'period', 'S.06.02.01.02,C0040A'])

    df_s08_2 = pd.read_pickle(join(report_dir, 'S.08.01.01.02.pickle')).fillna(0).reset_index()
    df_s08_2 = df_s08_2.set_index(['entity', 'period', 'S.08.01.01.02,C0040'])
    df_s08_2['S.08.01.01.02,C0040'] = df_s08_2.index.get_level_values(2)

    df_s08 = pd.merge(pd.read_pickle(join(report_dir,'S.08.01.01.01.pickle')).reset_index(),
                      pd.read_pickle(join(report_dir, 'S.08.01.01.02.pickle')).reset_index(),
                      how='inner', 
                      left_on=['entity','period','S.08.01.01.01,C0040'], 
                      right_on=['entity','period','S.08.01.01.02,C0040']).set_index(['entity', 'period', 'S.08.01.01.01,C0040'])
    df_s08 = df_s08.fillna(0).reset_index()
    df_s08['S.08.01.01.02,C0040A'] = df_s08['S.08.01.01.02,C0040']
    listt=list(df_s08['S.08.01.01.02,C0040A'])
    for i in listt:
        lenn = len(df_s08[df_s08['S.08.01.01.02,C0040A']==i])
        if lenn > 1:
            list_ind = list(df_s08.loc[df_s08['S.08.01.01.02,C0040A']==i].index)
            temp = 0
            for j in list_ind[1:]:
                temp=temp+1
                df_s08['S.08.01.01.02,C0040A'].iloc[j] = df_s08['S.08.01.01.02,C0040A'].iloc[j] + '_' + str(temp)
    df_s08 = df_s08.set_index(['entity', 'period', 'S.08.01.01.02,C0040A'])

    if not exists(output_dir):
        makedirs(output_dir)

    miner = data_patterns.PatternMiner(df_patterns=dfr_s06)
    results_06 = miner.analyze(df_s06)
    results_06.to_excel(join(output_dir, "results_S2_06_02.xlsx"), engine='openpyxl')

    miner = data_patterns.PatternMiner(df_patterns=dfr_s06_2)
    results_06_2 = miner.analyze(df_s06_2)
    results_06_2.to_excel(join(output_dir, "results_S2_06_02_01_02.xlsx"), engine='openpyxl')

    miner = data_patterns.PatternMiner(df_patterns=dfr_s06_1)
    results_06_1 = miner.analyze(df_s06_1)
    results_06_1.to_excel(join(output_dir, "results_S2_06_02_01_01.xlsx"), engine='openpyxl')

    miner = data_patterns.PatternMiner(df_patterns=dfr_s08)
    results_08 = miner.analyze(df_s08)
    results_08.to_excel(join(output_dir, "results_S2_08_01_01.xlsx"), engine='openpyxl')

    miner2 = data_patterns.PatternMiner(df_patterns=dfr_s08_2)
    results_08_2 = miner2.analyze(df_s08_2)
    results_08_2.to_excel(join(output_dir, "results_S2_08_01_01_02.xlsx"), engine='openpyxl')


if __name__ == "__main__":
    sys.exit(main())

