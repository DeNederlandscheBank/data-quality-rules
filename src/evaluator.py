import pandas as pd
import numpy as np
import os
from os.path import join
import re
import sys
import data_patterns
import logging


class Evaluator:
    def __init__(self, df_rules, df_datapoints, parameters):

        self.entrypoint_templates = sorted(list(df_datapoints['tabelcode'].unique()))
        self.entrypoint_datapoints = sorted(list((df_datapoints['tabelcode'] + "," +
                                                  df_datapoints['rij'] + "," +
                                                  df_datapoints['kolom']
                                                  ).str.replace(",,", ",")))
        self.df_rules = self.pre_process_rules(df_rules)
        self.df_patterns = self.process_rules(df_datapoints, parameters)

    def datapoints2pandas(self, s):
        """Transform EVA2 datapoints to Python Pandas datapoints by making letters uppercase"""
        datapoints = []
        for item in list(set(re.findall(r'{(.*?)}', s))):
            datapoints.append(item.upper())
            s = s.replace(item, '"' + item.upper() + '"')
        s = self.preprocess_pattern(s)
        return s, datapoints

    def replace_and_or(self, s):
        """Replace and by & and or by |, but not within strings"""
        if re.search(r"(.*?)\"(.*?)\"(.*)", s) is None:  # input text does not contain strings
            s = s.replace("OR", "|")
            s = s.replace("AND", "&")
        for item in re.findall(r"(.*?)\"(.*?)\"(.*)", s):
            s = s.replace(item[0], item[0].replace("OR", "|"))
            s = s.replace(item[0], item[0].replace("AND", "&"))
            s = s.replace(item[2], self.replace_and_or(item[2]))
        return s

    def replace_substr(self, s):
        """Replace SUBSTR(A,B,C) by A.str.slice(B,B+C,1)"""
        for item in re.findall(r"(SUBSTR\s?\()(.*?)(,)([0-9]{1,2})(,)([0-9]{1,2})(\))", s):
            s = s.replace("".join(item), item[1] + ".str.slice(" + str(int(item[3]) - int(1)) + "," + str(int(item[3]) - int(1) + int(item[5])) + ",1)")
        return s

    def replace_in_not_in(self, s):
        """Replace IN and NOT IN by str.contains((...))"""
        # NOT IN
        for item in re.findall(r"(.*?)(\s?[^\w]NOT IN[^\w]\s?)(\(.*?\))", s):
            item_2_adj = item[2] if "None" not in item[2] else "(" + item[2].replace("None, ", "").replace("None,", "").replace(", None", "").replace(",None", "") + ", True, 0, True)"
            s = s.replace("".join(item),item[0] + ".str.contains" + item[2].replace('","', "|").replace('", "', "|") + "=False")
        # IN
        for item in re.findall(r"(.*?)(\s?[^\w]IN[^\w]\s?)(\(.*?\))", s):
            item_2_adj = item[2] if "None" not in item[2] else "(" + item[2].replace("None, ", "").replace("None,", "").replace(", None", "").replace(",None", "") + ", True, 0, True)"
            s = s.replace("".join(item),item[0] + ".str.contains" + item_2_adj.replace('","', "|").replace('", "', "|"))
        return s

    def adjust_sum(self, s):
        """Adjust SUM by adding additional parenthesis""" 
        for item in re.findall(r"(SUM\s?\()(\(?.*\).*?\)?)", s):
            s = s.replace("".join(item),item[0] + "(" + item[1] + ")")
        return s

    def preprocess_pattern(self, pattern):
        # Pattern: AND, OR
        pattern = self.replace_and_or(pattern)
        # Pattern: SUBSTR
        pattern = self.replace_substr(pattern)
        # Pattern: IN, NOT IN
        pattern = self.replace_in_not_in(pattern)
        # Pattern: SUM
        pattern = self.adjust_sum(pattern)

        return pattern

    def make_pattern_expression(self, expression, name, parameters):
        """Make expressions for the miner"""
        parameters['solvency'] = True
        pandas_expressions = data_patterns.to_pandas_expressions(expression, {}, parameters, None)
        pattern = [[name, 0] + [expression] + [0, 0, 0] + ["DNB"] + [{}] + pandas_expressions + ["", "", ""]]
        return pattern

    def pre_process_rules(self, df_rules):
        """Transform rules so that we can evaluate them. Not all rules are fit to be evaluated"""
        logger = logging.getLogger(__name__)
        df_rules['datapoints'] = ''
        df_rules['datapoints'] = df_rules['datapoints'].astype('object')
        df_rules['templates'] = ''
        df_rules['templates'] = df_rules['templates'].astype('object')
        for row in df_rules.index:
            rule_original = df_rules.loc[row, 'Formule']
            if not isinstance(rule_original, str):
                logger.info("Rule " + row + ": " + "duplicate rule. ")
                rule_original = rule_original.values[0]
            rule_original, datapoints = self.datapoints2pandas(rule_original)
            df_rules.at[row, 'datapoints'] = datapoints
            df_rules.at[row, 'templates'] = list(set([datapoint[0:13].upper() for datapoint in datapoints]))
            df_rules.loc[row, 'Formule_input'] = rule_original

        df_rules['error'] = ''  # error message
        df_rules['n_patterns'] = 0  # number of patterns derived from rules

        return df_rules

    def unpack_rows_columns(self, row_range, column_range, datapoints, df_datapoints):
        "Unpack rows and columns"
        datapoints_not_found = []
        expansion_dict = {}
        # are the datapoints in the rule in the instance?
        for datapoint in datapoints:
            if datapoint not in self.entrypoint_datapoints:  # if datapoint is not there, see if we need to add rows or columns
                new_list = []
                bool_wildcard = ",#" in datapoint
                datapoint_orig = datapoint
                datapoint = datapoint.replace(",#", "")
                if datapoint[14] == "C" and (row_range[0] != "" or row_range[0].upper() == "ALL"):
                    if len(row_range) == 1 and row_range[0].upper() == "ALL":
                        for col in self.entrypoint_datapoints:
                            reg = re.search(datapoint[0:14] + "R....," + datapoint[14:],col)  # do for all rows if necessary
                            if reg:
                                new_list.append(reg.group(0))
                    else:
                        rows = []
                        for r in row_range:
                            if len(r) - len(r.replace("-", "")) == 1:  # range
                                low, high = r.split("-")
                                rows.extend(list(df_datapoints[(df_datapoints['tabelcode'] == datapoint[0:13]) &
                                                                (df_datapoints['kolom'] == datapoint[14:]) &
                                                                (df_datapoints['rij'].str[-4:] >= low) &
                                                                (df_datapoints['rij'].str[-4:] <= high)
                                                                ].rij))
                            else:
                                if r.upper()[0] == 'R':
                                    rows.extend([r.upper()])
                                else:
                                    rows.extend([('R' + r)])
                        for r in rows:
                            new_list.append(datapoint[0:14] + r + "," + datapoint[14:])
                if datapoint[14] == "R" and (column_range[0] != "" or column_range[0].upper() == "ALL"):
                    if len(column_range) == 1 and column_range[0].upper() == "ALL":
                        for col in self.entrypoint_datapoints:
                            reg = re.search(datapoint + ",C....", col)  # do for all columns if necessary
                            if reg:
                                new_list.append(reg.group(0))
                    else:
                        cols = []
                        for c in column_range:
                            if len(c) - len(c.replace("-", "")) == 1:  # range
                                low, high = c.split("-")
                                cols.extend(list(df_datapoints[(df_datapoints['tabelcode'] == datapoint[0:13]) &
                                                                (df_datapoints['rij'] == datapoint[14:]) &
                                                                (df_datapoints['kolom'].str[-4:] >= low) &
                                                                (df_datapoints['kolom'].str[-4:] <= high)
                                                                ].kolom))
                            else:
                                if c.upper()[0] == 'C':
                                    cols.extend([c.upper()])
                                else:
                                    cols.extend([('C' + c)])
                        for c in cols:
                            new_list.append(datapoint + "," + c)
                if new_list != []:
                    # Wildcard # notation indicates that we need to sum over all the datapoints
                    new_list = ['"},{"'.join(new_list)] if bool_wildcard else new_list
                    expansion_dict[datapoint_orig] = new_list
                else:
                    datapoints_not_found.append(datapoint_orig)

        return expansion_dict, datapoints_not_found

    def process_rule(self, pre_expression, name, datapoints, expansion_dict, df_datapoints, parameters):
        """Some rules have multiple rows or columns. This function makes all the expressions with every row/column"""
        expressions = []
        invalid_expressions = ""
        if expansion_dict:
            if datapoints[0] in expansion_dict.keys():
                zero = datapoints[0]
            else:
                zero = datapoints[1]
            bool_wildcard = ",#" in pre_expression
            for i in range(len(expansion_dict[zero])):
                expression = pre_expression
                valid_expression = True
                for datapoint in datapoints:
                    if datapoint in expansion_dict.keys():
                        datapoints_wildcard = [item for item in re.findall(r"(S\.\d\d\.\d\d\.\d\d\.\d\d,R\d\d\d\d,C\d\d\d\d)*", expansion_dict[datapoint][i]) if item != '']
                        for datapoint_wildcard in datapoints_wildcard:
                            if len(df_datapoints[(df_datapoints['tabelcode'] == datapoint_wildcard[:13]) &
                                                (df_datapoints['rij'] == datapoint_wildcard[14:19].upper()) &
                                                (df_datapoints['kolom'] == datapoint_wildcard[20:25].upper())]) == 0:
                                valid_expression = False
                        expression = expression.replace(datapoint, expansion_dict[datapoint][i])
                if valid_expression:
                    expressions.extend(self.make_pattern_expression(expression, name, parameters))
                else:
                    if invalid_expressions == "":
                        invalid_expressions = invalid_expressions + "(" + expression + ")"
                    else:
                        invalid_expressions = invalid_expressions + ", (" + expression + ")"
        else:
            expressions.extend(self.make_pattern_expression(pre_expression, name, parameters))

        return expressions, invalid_expressions

    def process_rules(self, df_datapoints, parameters):
        """Evaluate all rules and stores the result in df_rules"""
        logger = logging.getLogger(__name__)
        rules_expressions = []
        for idx in range(len(self.df_rules.index)):
            row = self.df_rules.index[idx]
            rule_original = self.df_rules.loc[row, 'Formule_input']
            rule_name = self.df_rules.index[idx]
            datapoints = self.df_rules.loc[row, 'datapoints'].copy()
            templates = self.df_rules.loc[row, 'templates']
            self.df_rules['Rijen'] = self.df_rules['Rijen'].astype(str)
            self.df_rules['Kolommen'] = self.df_rules['Kolommen'].astype(str)
            row_range = self.df_rules.loc[row, 'Rijen'].replace("(", "").replace(")", "").replace(",", ";").split(";")
            column_range = self.df_rules.loc[row, 'Kolommen'].replace("(", "").replace(")", "").replace(",", ";").split(";")
            # are the templates in the rule in the instance?
            templates_not_found = []
            for template in templates:
                if template not in self.entrypoint_templates:
                    templates_not_found.append(template)

            if templates_not_found == []:
                expansion_dict, datapoints_not_found = self.unpack_rows_columns(row_range, column_range, datapoints, df_datapoints)
                if datapoints_not_found == []:
                    rule_expressions, invalid_expressions = self.process_rule(rule_original, rule_name, datapoints, expansion_dict, df_datapoints, parameters)
                    rules_expressions.extend(rule_expressions)
                    if invalid_expressions != "":
                        self.df_rules.loc[row, 'error'] = \
                            'Some expressions skipped due to invalid datapoint references: ' + invalid_expressions
                        logger.warning("Rule " + row + ", " + self.df_rules.loc[row, 'error'])
                    else:
                        self.df_rules.loc[row, 'error'] = ''
                    self.df_rules.loc[row, 'n_patterns'] = len(rule_expressions)
                    logger.info("Rule " + row + ", " + str(len(rule_expressions)) + " pattern(s) generated")
                else:
                    # expression = rule_original
                    self.df_rules.loc[row, 'error'] = 'missing datapoint(s): ' + str(datapoints_not_found)
                    logger.warning("Rule " + row + ", " + self.df_rules.loc[row, 'error'])
            else:
                # expression = rule_original
                self.df_rules.loc[row, 'error'] = 'missing template(s): ' + str(templates_not_found)
                logger.warning("Rule " + row + ", " + self.df_rules.loc[row, 'error'])

        df_patterns = pd.DataFrame(data = rules_expressions, columns = data_patterns.PATTERNS_COLUMNS)
        df_patterns.index.name = 'index'

        return df_patterns