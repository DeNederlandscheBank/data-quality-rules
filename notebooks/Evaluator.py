import pandas as pd
import numpy as np
import os
from os.path import join
import re
import sys
import data_patterns



class Evaluator:
    def __init__(self, df, df_rules, instance_templates):
        self.df = df
        self.df_rules = df_rules
        self.expressions = []
        self.miner = data_patterns.PatternMiner(df)
        self.instance_templates = instance_templates
        self.df_patterns = None

    def datapoints2pandas(self, s):
        """Transform EVA2 datapoints to Python Pandas datapoints"""
        datapoints = []
        for item in re.findall(r'{(.*?)}', s):
            datapoints.append(item.upper())
            s = s.replace(item,  item.upper() )
        return s, datapoints



    def make_expression(self, expression):
        """Evaluate Python Pandas string for confirmation and exceptions"""

        parameters = {'min_confidence': 0,'min_support'   : 0, 'solvency' : True}
        p2 = {'name'      : 'Pattern 1',
            'expression' : expression,
             'parameters':parameters}
        return p2
        # df_patterns = miner.find(p2)
        # co = df_patterns.loc[0,'support']
        # ex = df_patterns.loc[0,'exceptions']
        # if df_patterns.loc[0,'Error message'] != '':
        #     return "ERROR: "+ df_patterns.loc[0,'Error message']
        # return "Correctly parsed (#co=" + str(co)+", #ex="+str(ex)+")"

    def transform_rules(self):
        for row in self.df_rules.index:
            rule_original = self.df_rules.loc[row, 'Formule']
            if not isinstance(rule_original, str):
                print("Rule " + row + ": " + "duplicate rule. ")
                rule_original = rule_original.values[0]
            else:
                rule_original, datapoints = self.datapoints2pandas(rule_original)
                self.df_rules.at[row, 'datapoints'] = ''
                self.df_rules.at[row, 'datapoints'] = self.df_rules['datapoints'].astype('object')
                self.df_rules.at[row, 'datapoints'] = datapoints
                self.df_rules.at[row, 'templates'] = ''
                self.df_rules.at[row, 'templates'] = self.df_rules['templates'].astype('object')
                self.df_rules.at[row, 'templates'] = [datapoint[0:13].upper() for datapoint in datapoints]
                self.df_rules.loc[row, 'Formule_input'] = rule_original

    def evaluate_rule(self, expression, datapoints, substitutions, expansion_dict):
        if datapoints == []:
            for item in substitutions.keys():
                expression = expression.replace(item, substitutions[item])
            self.expressions.append(self.make_expression(expression))
        else:
            datapoint = datapoints.pop()
            if datapoint in expansion_dict.keys():
                for d in expansion_dict[datapoint]:
                    substitutions[datapoint] = d
                    self.evaluate_rule(expression, datapoints, substitutions, expansion_dict)
            else:
                self.evaluate_rule(expression, datapoints, substitutions, expansion_dict)

    def evaluate_rules(self):
        self.expressions = []
        count_expression = 0
        self.df_rules['final'] = ''
        for idx in range(len(self.df_rules.index)):
            row = self.df_rules.index[idx]
            rule_original = self.df_rules.loc[row, 'Formule_input']
            datapoints = self.df_rules.loc[row, 'datapoints'].copy()
            templates = self.df_rules.loc[row, 'templates']
            # are the templates in the rule in the instance?
            templates_not_found = []
            for template in templates:
                if template not in self.instance_templates:
                    templates_not_found.append(template)

            if templates_not_found == []:
                datapoints_not_found = []
                expansion_dict = {}
                # are the datapoints in the rule in the instance?
                for datapoint in datapoints:
                    if datapoint not in self.df.columns:
                        all_datapoints_found = False
                        new_list = []
                        if datapoint[14]=="C":
                            for col in self.df.columns:
                                reg = re.search(datapoint[0:14] + "R....," + datapoint[14:], col)
                                if reg:
                                    new_list.append(reg.group(0))
                        if datapoint[14]=="R":
                            for col in self.df.columns:
                                reg = re.search(datapoint + ",C....", col)
                                if reg:
                                    new_list.append(reg.group(0))
                        if new_list != []:
                            expansion_dict[datapoint] = new_list
                        else:
                            datapoints_not_found.append(datapoint)
                if datapoints_not_found == []:
                    expression = rule_original
                    self.evaluate_rule(expression, datapoints, {}, expansion_dict)
                    self.df_rules.loc[row, 'final'] = len(self.expressions) - count_expression
                    count_expression = len(self.expressions)
                else:
                    self.df_rules.loc[row, 'final'] = 'No datapoint'
            else:
                self.df_rules.loc[row, 'final'] = 'No template'
        self.df_patterns = self.miner.find(self.expressions)


    def print_result(self):
        patterns_counter = 0
        for idx in range(len(self.df_rules.index)):
            row = self.df_rules.index[idx]
            print(str(idx) + ": ", end='')
            if self.df_rules.loc[row, 'final'] == 'No template':
                print("Not all templates in instance: " +str(self.df_rules.loc[row, 'templates']))
            elif self.df_rules.loc[row, 'final'] == 'No datapoint':
                print("Datapoints not found: " +str(self.df_rules.loc[row, 'datapoints']))
            else:
                for i in range(self.df_rules.loc[row, 'final']):
                    if self.df_patterns.loc[patterns_counter,'Error message'] != '':
                        print("ERROR: "+  self.df_patterns.loc[patterns_counter,'Error message'])
                    co =  self.df_patterns.loc[patterns_counter,'support']
                    ex =  self.df_patterns.loc[patterns_counter,'exceptions']
                    print("Correctly parsed (#co=" + str(co)+", #ex="+str(ex)+")")
                    patterns_counter += 1
