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
        """Transform EVA2 datapoints to Python Pandas datapoints by making letters uppercase"""
        datapoints = []
        for item in re.findall(r'{(.*?)}', s):
            datapoints.append(item.upper())
            s = s.replace(item, '"' + item.upper() + '"')
        s = self.preprocess_pattern(s)
        return s, datapoints

    def replace_and_or(self, s):
        """Replace and by & and or by |, but not within strings"""
        if re.search(r"(.*?)\'(.*?)\'(.*)", s) is None: # input text does not contain strings
            s = s.replace("OR", "|")
            s = s.replace("AND", "&")
        for item in re.findall(r"(.*?)\'(.*?)\'(.*)", s):
            s = s.replace(item[0], item[0].replace("OR", "|"))
            s = s.replace(item[0], item[0].replace("AND", "&"))
            s = s.replace(item[2], self.replace_and_or(item[2]))
        return s


    def preprocess_pattern(self, pattern):

        pattern = pattern.replace("<>", "!=")
        pattern = pattern.replace("< >", "!=") # the space between < and > should be deleted in EVA2
        pattern = pattern.replace(';', ",") # this should be corrected in EVA2

        pattern = pattern.replace('"', "'")
        pattern = self.replace_and_or(pattern)
        return pattern

    def make_pattern_expression(self, expression, name):
        """Make expressions for the miner"""
        parameters = {'solvency': True}
        pandas_expressions = data_patterns.to_pandas_expressions(expression, {}, parameters, None)
        pattern = [[name, 0] + [expression] + [0, 0, 0] + ["DNB"] + [{}] + pandas_expressions + ["", "", ""]]
        return pattern

# PATTERNS_COLUMNS            = [PATTERN_ID, CLUSTER,
#                                PATTERN_DEF,
#                                SUPPORT, EXCEPTIONS, CONFIDENCE, PATTERN_STATUS, ENCODINGS, PANDAS_CO, PANDAS_EX, XBRL_CO, XBRL_EX, ERROR]



    def transform_rules(self):
        """Transform rules so that we can evaluate them. Not all rules are fit to be evaluated"""
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


    def evaluate_rule(self, expression, name, datapoints, substitutions, expansion_dict):
        """Some rules have multiple rows or columns. This function makes all the expressions with every row/column"""

        # if datapoints is empty then make expression
        if datapoints == []:
            for item in substitutions.keys():
                expression = expression.replace(item, substitutions[item])
            self.expressions.extend(self.make_pattern_expression(expression, name))
        # if there are datapoints see if we can change it by adding rows and columns
        else:
            datapoint = datapoints.pop()
            if datapoint in expansion_dict.keys():
                for d in expansion_dict[datapoint]:
                    substitutions[datapoint] = d
                    self.evaluate_rule(expression, name, datapoints, substitutions, expansion_dict)
            else:
                self.evaluate_rule(expression, name, datapoints, substitutions, expansion_dict)


    def evaluate_rules(self):
        """Evaluate all rules and stores the result in df_rules"""
        self.expressions = []
        count_expression = 0
        self.df_rules['final'] = '' # final result
        for idx in range(len(self.df_rules.index)):
            row = self.df_rules.index[idx]
            rule_original = self.df_rules.loc[row, 'Formule_input']
            rule_name = self.df_rules.index[idx]
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
                    if datapoint not in self.df.columns: # if datapoint is not there, see if we need to add rows or columns
                        all_datapoints_found = False
                        new_list = []
                        if datapoint[14]=="C":
                            for col in self.df.columns:
                                reg = re.search(datapoint[0:14] + "R....," + datapoint[14:], col) # do for all rows if necessary
                                if reg:
                                    new_list.append(reg.group(0))
                        if datapoint[14]=="R":
                            for col in self.df.columns:
                                reg = re.search(datapoint + ",C....", col)# do for all columns if necessary
                                if reg:
                                    new_list.append(reg.group(0))
                        if new_list != []:
                            expansion_dict[datapoint] = new_list
                        else:
                            datapoints_not_found.append(datapoint)
                if datapoints_not_found == []:
                    expression = rule_original
                    self.evaluate_rule(expression, rule_name, datapoints, {}, expansion_dict)
                    self.df_rules.loc[row, 'final'] = len(self.expressions) - count_expression # if there are points then store how many
                    count_expression = len(self.expressions)
                else:
                    self.df_rules.loc[row, 'final'] = 'No datapoint'
            else:
                self.df_rules.loc[row, 'final'] = 'No template'

        self.df_patterns = pd.DataFrame(data = self.expressions, columns = data_patterns.PATTERNS_COLUMNS)
        self.df_patterns.index.name = 'index'
        return self.df_patterns
        #self.df_patterns = self.miner.find(self.expressions) # go through list of expressions at once


    def print_result(self):
        """Print results of the function evaluate"""
        patterns_counter = 0 # keep track of the expressions
        for idx in range(len(self.df_rules.index)):
            row = self.df_rules.index[idx]
            print(str(idx) + ": ", end='')
            if self.df_rules.loc[row, 'final'] == 'No template':
                print("Not all templates in instance: " +str(self.df_rules.loc[row, 'templates']))
            elif self.df_rules.loc[row, 'final'] == 'No datapoint':
                print("Datapoints not found: " +str(self.df_rules.loc[row, 'datapoints']))
            else:
                for i in range(self.df_rules.loc[row, 'final']): # one rules can have many expressions
                    if self.df_patterns.loc[patterns_counter,'Error message'] != '':
                        print("ERROR: "+  self.df_patterns.loc[patterns_counter,'Error message'])
                    co =  self.df_patterns.loc[patterns_counter,'support']
                    ex =  self.df_patterns.loc[patterns_counter,'exceptions']
                    print("Correctly parsed (#co=" + str(co)+", #ex="+str(ex)+")")
                    patterns_counter += 1
