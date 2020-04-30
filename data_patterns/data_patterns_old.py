# -*- coding: utf-8 -*-

"""Main module."""

# imports
import pandas as pd
import numpy as np
import copy
import xlsxwriter
import ast
from functools import reduce
import itertools
import logging
from .constants import *
from .transform import *
from .encodings import *
from .parser import *

#import optimized

__author__ = """De Nederlandsche Bank"""
__email__ = 'ECDB_berichten@dnb.nl'
__version__ = '0.1.13'

class PatternMiner:

    '''
    A PatternMiner object mines patterns in a Pandas DataFrame.

    Parameters
    ----------
    dataframe : DataFrame, optional, the dataframe with data used for training and testing (optional)
    metapatterns : list of dictionaries, optional

    Attributes
    ----------

    dataframe : Dataframe, shape (n_observations,)
        Dataframe with most recent data used for training and testing

    metapatterns : list of dictionaries (optional)
        a metapattern is a dict with
            'name': identifier of the metapattern (optional)
            'P_columns': columns of dataframe (P part of metapattern)
            'Q_columns': columns of datafrane (Q part of metapattern)
            'parameters': minimum confidence, patterns with higher confidence are included (optional)
            'encode': encoding definitions of the columns (optional)

    data : list, shape (n_patterns,)
        Patterns with statistics and confirmation and exceptions

    Examples
    --------

    See Also
    --------

    Notes
    -----

    '''

    def __init__(self, *args, **kwargs):
        self.df_data = None
        self.df_patterns = None
        self.metapatterns = None
        self.__process_parameters(*args, **kwargs)

    def find(self, *args, **kwargs):
        '''General function to find patterns
        '''
        self.__process_parameters(*args, **kwargs)

        assert self.metapatterns is not None, "No patterns defined."
        assert self.df_data is not None, "No dataframe defined."

        new_df_patterns = derive_patterns(**kwargs, metapatterns = self.metapatterns, dataframe = self.df_data)

        if (not kwargs.get('append', False)) or (self.df_patterns is None):
            self.df_patterns = new_df_patterns
        else:
            if len(new_df_patterns.index) > 0:
                self.df_patterns.append(new_df_patterns)

        return self.df_patterns

    def analyze(self, *args, **kwargs):
        '''General function to analyze data given a list of patterns
        '''
        self.__process_parameters(*args, **kwargs)

        assert self.df_patterns is not None, "No patterns defined."
        assert self.df_data is not None, "No data defined."

        self.df_patterns = update_statistics(dataframe = self.df_data, df_patterns = self.df_patterns)

        df_results = derive_results(**kwargs, df_patterns = self.df_patterns, dataframe = self.df_data)

        return df_results

    def update_statistics(self, *args, **kwargs):
        '''Function that updates the pattern statistics in df_patterns
        '''
        self.__process_parameters(*args, **kwargs)

        assert self.df_patterns is not None, "No patterns defined."
        assert self.df_data is not None, "No data defined."

        self.df_patterns = update_statistics(dataframe = self.df_data, df_patterns = self.df_patterns)

        return self.df_patterns

    def convert_labels(self, df1, df2):
        ''' converts the column names of a pattern dataframe
        '''
        return to_dataframe(patterns = convert_columns(self.df_patterns, df1, df2))

    def __process_parameters(self, *args, **kwargs):
        '''Update variables in the object
        '''
        self.metapatterns = self.__process_key('metapatterns', dict, self.metapatterns, *args, **kwargs)
        self.metapatterns = self.__process_key('metapatterns', list, self.metapatterns, *args, **kwargs)
        self.df_patterns = self.__process_key('df_patterns', None, self.df_patterns, *args, **kwargs)
        self.df_data = self.__process_key('dataframe', pd.DataFrame, self.df_data, *args, **kwargs)

        if isinstance(self.metapatterns, dict):
            self.metapatterns = [self.metapatterns]

        return None

    def __process_key(self, key, key_type, current, *args, **kwargs):
        '''
        '''
        if key in kwargs.keys():
            return kwargs.pop(key)
        else:
            for arg in args:
                if (key_type is not None) and isinstance(arg, key_type):
                      return arg
        return current

def derive_patterns(dataframe   = None,
                    metapatterns = None):
    '''Derive patterns from metapatterns
       In three flavours:
       - expressions (defined as a string),
       - conditional rules ('-->'-pattern defined with their columns) and
       - single rules (defined with their colums)
    '''
    df_patterns = pd.DataFrame(columns = PATTERNS_COLUMNS)
    for metapattern in metapatterns:
        if "expression" in metapattern.keys():
            patterns = derive_patterns_from_template_expression(metapattern = metapattern,
                                                                dataframe = dataframe)
        elif metapattern.get("pattern", "-->") == "-->":

            patterns = derive_conditional_patterns(metapattern = metapattern,
                                                   dataframe = dataframe)
        else:
            patterns = derive_single_patterns(metapattern = metapattern,
                                              dataframe = dataframe)
        df_patterns = df_patterns.append(patterns, ignore_index = True)

    df_patterns[CLUSTER] = df_patterns[CLUSTER].astype(np.int64)
    df_patterns[SUPPORT] = df_patterns[SUPPORT].astype(np.int64)
    df_patterns[EXCEPTIONS] = df_patterns[EXCEPTIONS].astype(np.int64)
    df_patterns.index.name = 'index'
    return PatternDataFrame(df_patterns)

def derive_patterns_from_template_expression(metapattern = None,
                                             dataframe = None):
    """
    Here we can add the constructions of expressions from an expression with wildcards
    """
    expression = metapattern.get("expression", "")
    parameters = metapattern.get("parameters", {})

    new_list = derive_patterns_from_expression(expression, metapattern, dataframe)
    df_patterns = to_dataframe(patterns = new_list, parameters = parameters)
    return df_patterns

def get_possible_columns(amount, expression, dataframe):
    if amount == 0:
        return [expression]

    all_columns = []

    for datapoint in re.findall(r'{.*?}', expression): # See which columns we are looking for per left open column
        d = datapoint[1:-1] # strip {" and "}
        all_columns.append([re.search(d, col).group(0) for col in dataframe.columns if re.search(d, col)])
        expression = expression.replace(datapoint, '{.*}', 1) # Replace it so that it goes well later
    if amount > 1: # Combine the lists into combinations where we do not have duplicates
        if re.search('AND', expression):
            possibilities = [p for p in itertools.product(*all_columns) if len(set(p)) == int(len(p)/2)]
        else:
            possibilities = [p for p in itertools.product(*all_columns) if len(set(p)) == len(p)]
    elif amount == 1: # If we have one empty spot, then just use the possible values
        possibilities = [[i] for i in all_columns[0]]

    possible_expressions = [] # list of all possible expressions
    for columns in possibilities:
        possible_expression = expression
        for column in columns: # replace with the possible column value
            possible_expression = possible_expression.replace(".*", '"' + column + '"', 1) # replace with column
        possible_expressions.append(possible_expression)
    return possible_expressions

def get_possible_values(amount, possible_expressions, dataframe):
    if amount < 1: # no values to be found
        return possible_expressions
    else:
        expressions = []
        for possible_expression in possible_expressions:
            all_columns_v = []
            for item in re.findall(r'.*?@', possible_expression): # See which columns we are looking for per left open column
                value_col = re.findall("{.*?}", item)[-1] # Get the column that matches the value indicator *@
                value_col = value_col[2:-2] # strip { and }
                all_columns_v.append(list(dataframe[value_col].unique()))

            if amount > 1: # same with columns
                possibilities_v = [p for p in itertools.product(*all_columns_v)]
            else:
                possibilities_v = [[i] for i in all_columns_v[0]]


            for columns_v in possibilities_v: # Make all combinations without duplicates  of values
                possible_expression_v = possible_expression
                for column_v in columns_v:
                    if isinstance(column_v, str):
                        possible_expression_v = possible_expression_v.replace("@", '"'+ column_v +'"', 1) # replace adn add ""
                    else:
                        possible_expression_v = possible_expression_v.replace("@", str(column_v), 1) # replace with str
                    expressions.append(possible_expression_v)
        return expressions

def derive_patterns_from_expression(expression = "",
                                    metapattern = None,
                                    dataframe = None):
    """
    """
    parameters = metapattern.get("parameters", {})
    name = metapattern.get('name', "No name")
    encode = metapattern.get(ENCODE, {}) # TO DO
    encodings = get_encodings()
    confidence, support = get_parameters(parameters)
    patterns = list()

    amount = expression.count('.*}') #Amount of columns to be found
    amount_v = expression.count("@") #Amount of column values to be found

    possible_expressions = get_possible_columns(amount, expression, dataframe)
    possible_expressions = get_possible_values(amount_v, possible_expressions, dataframe)

    for possible_expression in possible_expressions:
        pandas_expressions = to_pandas_expressions(possible_expression, encode, parameters, dataframe)
        try: # Some give error so we use try
            n_co = len(eval(pandas_expressions[0], encodings, {'df': dataframe}).index)
            n_ex = len(eval(pandas_expressions[1], encodings, {'df': dataframe}).index)
            conf = np.round(n_co / (n_co + n_ex + 1e-11), 4)
            if ((conf >= confidence) and (n_co >= support)):
                xbrl_expressions = to_xbrl_expressions(possible_expression, encode, parameters)
                patterns.extend([[[name, 0], possible_expression, [n_co, n_ex, conf]] + pandas_expressions + xbrl_expressions])
        except:
            continue

    return patterns

def derive_conditional_patterns(metapattern = None,
                                dataframe = None):
    '''Derive conditional rule patterns
       If no columns are given, then the algorithm searches for all possibilities
    '''
    new_list = list()

    parameters = metapattern.get("parameters", {})

    include_subsets = parameters.get("include_subsets", False)
    include_subsets_p = parameters.get("include_subsets_P_columns", False)
    include_subsets_q = parameters.get("include_subsets_Q_columns", False)

    if include_subsets:
        p_part = None
        q_part = None
        col_total_p = metapattern.get("P_columns", None)
        col_total_q = metapattern.get("Q_columns", None)
    elif include_subsets_q:
        q_part = None
        col_total_q = metapattern.get("Q_columns", None)
        p_part = metapattern.get("P_columns", None)
        col_total_p = dataframe.columns
    elif include_subsets_p:
        p_part = None
        col_total_p = metapattern.get("P_columns", None)
        q_part = metapattern.get("Q_columns", None)
        col_total_q = dataframe.columns
    else:
        p_part = metapattern.get("P_columns", None)
        q_part = metapattern.get("Q_columns", None)
        col_total_p = list(dataframe.columns.values)
        col_total_q = list(dataframe.columns.values)

    metapattern = copy.deepcopy(metapattern)

    # there are four cases:
    # - p and q are given,
    # - p is given but q is not given,
    # - q is given but p is not,
    # - p and q are not given

    if ((p_part is None) and (q_part is not None)):
        p_set = [col for col in col_total_p if col not in metapattern["Q_columns"]]
        p_set = itertools.chain.from_iterable(itertools.combinations(p_set, n+1) for n in range(len(p_set)))
        for item in p_set:
            metapattern["P_columns"] = list(item)
            new_patterns = derive_conditional_pattern(metapattern = metapattern, dataframe = dataframe)
            new_list.extend(new_patterns)
    elif ((q_part is None) and (p_part is not None)):
        q_set = [col for col in col_total_q if col not in metapattern["P_columns"]]
        q_set = itertools.chain.from_iterable(itertools.combinations(q_set, n+1) for n in range(len(q_set)))
        for item in q_set:
            metapattern["Q_columns"] = list(item)
            new_patterns = derive_conditional_pattern(metapattern = metapattern, dataframe = dataframe)
            new_list.extend(new_patterns)
    elif ((q_part is None) and (p_part is None)):
        p_set = [col for col in col_total_p]
        p_set = itertools.chain.from_iterable(itertools.combinations(p_set, n+1) for n in range(len(p_set)))
        for p_item in p_set:
            q_set = [col for col in col_total_q if col not in p_item]
            q_set = itertools.chain.from_iterable(itertools.combinations(q_set, n+1) for n in range(len(q_set)))
            for q_item in q_set:
                metapattern["Q_columns"] = list(q_item)
                metapattern["P_columns"] = list(p_item)
                new_patterns = derive_conditional_pattern(metapattern = metapattern, dataframe = dataframe)
                new_list.extend(new_patterns)
    else:
        new_patterns = derive_conditional_pattern(metapattern = metapattern, dataframe = dataframe)
        new_list.extend(new_patterns)
    df_patterns = to_dataframe(patterns = new_list, parameters = parameters)
    return df_patterns

def derive_conditional_pattern(dataframe = None,
                               metapattern = None):
    '''Here we derive the patterns from the metapattern definitions
       by evaluating the pandas expressions of all potential patterns
    '''
    # get items from metapattern definition
    parameters = metapattern.get("parameters", {})
    name = metapattern.get('name', "No name")
    encode = metapattern.get(ENCODE, {})
    P_columns = metapattern.get("P_columns", list(dataframe.columns.values))
    Q_columns = metapattern.get("Q_columns", list(dataframe.columns.values))
    P_values = metapattern.get("P_values", None)
    Q_values = metapattern.get("Q_values", None)

    confidence, support = get_parameters(parameters)

    # adding index levels to columns (in case the pattern contains index elements)
    for level in range(len(dataframe.index.names)):
        dataframe[dataframe.index.names[level]] = dataframe.index.get_level_values(level = level)

    # derive df_feature list from P and Q (we use a copy, so we can change values for encodings)
    df_features = dataframe[P_columns + Q_columns].copy()
    # execute dynamic encoding functions
    encodings = get_encodings()
    # perform encodings on df_features
    if encode != {}:
        for c in df_features.columns:
            if c in encode.keys():
                df_features[c] = eval(str(encode[c])+ "(s)", encodings, {'s': df_features[c]})
    patterns = list()
    # Booleans so that we know if P and Q values are given or not
    bool_P = False
    if P_values is None:
        bool_P = True
    bool_Q = False
    if Q_values is None:
        bool_Q = True

    # In the case of Q or P values not given, we can use the old code
    if bool_P or bool_Q:
        if bool_P and bool_Q:
            df_potential_patterns = df_features.drop_duplicates(P_columns + Q_columns)
        elif bool_P:
            df_potential_patterns = df_features.drop_duplicates(P_columns) # these are all unique combinations, i.e. the potential rules
        elif bool_Q:
            df_potential_patterns = df_features.drop_duplicates(Q_columns) # these are all unique combinations, i.e. the potential rules
        for idx in range(len(df_potential_patterns.index)):
            if bool_P: # only use when P value is not given
                P_values = list(df_potential_patterns[P_columns].values[idx])
            if bool_Q:# only use when Q value is not given
                Q_values = list(df_potential_patterns[Q_columns].values[idx])
            expression = generate_conditional_expression(P_columns, P_values, Q_columns, Q_values, parameters)


            patterns.extend(derive_patterns_from_expression(expression, metapattern, dataframe))

    # In the case that P and Q values are both given, we only want to compute it for these values and not search for other values like above
    else:
        expression = generate_conditional_expression(P_columns, P_values, Q_columns, Q_values, parameters)
        patterns.extend(derive_patterns_from_expression(expression, metapattern, dataframe))

    # deleting the levels of the index to the columns
    for level in range(len(dataframe.index.names)):
        del dataframe[dataframe.index.names[level]]
    return patterns

def derive_single_patterns(metapattern  = None,
                           dataframe    = None):
    '''
    '''
    logger = logging.getLogger("single-pattern")

    P_dataframe = metapattern.get("P_dataframe", None)
    Q_dataframe = metapattern.get("Q_dataframe", None)
    pattern = metapattern.get("pattern", None)
    pattern_name = metapattern.get("name", None)
    columns = metapattern.get("columns", None)
    P_columns = metapattern.get("P_columns", None)
    Q_columns = metapattern.get("Q_columns", None)
    value = metapattern.get("value", None)
    values = metapattern.get("values", None)
    parameters = metapattern.get("parameters", {})

    # if P_dataframe and Q_dataframe are given then join the dataframes and select columns
    if (P_dataframe is not None) and (Q_dataframe is not None):
        try:
            dataframe = P_dataframe.join(Q_dataframe)
        except:
            logger.error("Join of P_dataframe and Q_dataframe failed, overlapping columns?")
            return []
        P_columns = P_dataframe.columns
        Q_columns = Q_dataframe.columns

    # select all columns with numerical values
    numerical_columns = [dataframe.columns[c] for c in range(len(dataframe.columns))
                            if ((dataframe.dtypes[c] == 'float64') or (dataframe.dtypes[c] == 'int64')) and (dataframe.iloc[:, c] != 0).any()]
    dataframe = dataframe[numerical_columns]

    if P_columns is not None:
        P_columns = [dataframe.columns.get_loc(c) for c in P_columns if c in numerical_columns]
    else:
        P_columns = range(len(dataframe.columns))

    if Q_columns is not None:
        Q_columns = [dataframe.columns.get_loc(c) for c in Q_columns if c in numerical_columns]
    else:
        Q_columns = range(len(dataframe.columns))

    if columns is not None:
        columns = [dataframe.columns.get_loc(c) for c in columns if c in numerical_columns]
    else:
        columns = range(len(dataframe.columns))

    logger.info('START: %s (%s) in P_columns = %s and Q_columns = %s', pattern, pattern_name, str(P_columns), str(Q_columns))

    # if a value is given -> columns pattern value
    if value is not None:
        results = derive_column_value_pattern(dataframe = dataframe,
                                        pattern = pattern,
                                        pattern_name = pattern_name,
                                        columns = columns,
                                        value = value,
                                        parameters = parameters)
    elif pattern == 'sum':
        results = derive_sums_column_pattern(dataframe = dataframe,
                                       pattern_name = pattern_name,
                                       P_columns = P_columns,
                                       Q_columns = Q_columns,
                                       parameters = parameters)

    elif pattern == 'percentile':
        results = derive_percentile_column_pattern(dataframe = dataframe,
                                       pattern_name = pattern_name,
                                       pattern = pattern,
                                       columns = columns,
                                       parameters = parameters)

    elif pattern == 'ratio':
        results = derive_ratio_pattern(dataframe = dataframe,
                                 pattern_name = pattern_name,
                                 P_columns = P_columns,
                                 Q_columns = Q_columns,
                                 parameters = parameters)

    # everything else -> c1 pattern c2
    else:
        results = derive_column_column_pattern(dataframe = dataframe,
                                         pattern = pattern,
                                         pattern_name = pattern_name,
                                         P_columns = P_columns,
                                         Q_columns = Q_columns,
                                         parameters = parameters)

    patterns = [[pattern_id] + [pattern] + [pattern_stats] +
                to_pandas_expressions(pattern, {},parameters, dataframe) +
                to_xbrl_expressions(pattern, {}, parameters)
                 for [pattern_id, pattern, pattern_stats] in results]
    df = to_dataframe(patterns = patterns, parameters = parameters)

    logger.info('END: %s (%s)', pattern, pattern_name)

    return df

def to_pandas_expressions(pattern, encode, parameters, dataframe):
    """Derive pandas code from the pattern definition string both confirmation and exceptions"""

    # preprocessing step
    res = preprocess_pattern(pattern)
    # datapoints to pandas, i.e. {column} -> df[column]
    res, nonzero_col = datapoints2pandas(res, encode)
    # expression to pandas, i.e. IF X=x THEN Y=y -> df[df[X]=x & df[Y]=y] for confirmations
    co_str, ex_str = expression2pandas(res, nonzero_col, parameters)

    return [co_str, ex_str]

def to_dataframe(patterns = None, parameters = {}):
    '''Convert list of patterns to dataframe with patterns
    '''
    # unpack pattern_id and pattern and patterns_stats and exclude co and ex and set pattern status to unknown
    patterns = list(patterns)
    if len(patterns) > 0:
        data = [pattern_id + [pattern] + pattern_stats + [INITIAL_PATTERN_STATUS] + [{}] +
               [pandas_co, pandas_ex, xbrl_co, xbrl_ex] for [pattern_id, pattern, pattern_stats, pandas_co, pandas_ex, xbrl_co, xbrl_ex] in patterns]
        df = pd.DataFrame(data = data, columns = PATTERNS_COLUMNS)
        df.index.name = 'index'
    else:
        df = pd.DataFrame(columns = PATTERNS_COLUMNS)
        df.index.name = 'index'
    return df

def update_statistics(dataframe = None,
                      df_patterns = None):
    '''Update statistics in df_patterns with statistics from the data by evaluating pandas expressions
    '''
    encodings = get_encodings()
    df_new_patterns = pd.DataFrame()
    if (dataframe is not None) and (df_patterns is not None):
        # adding the levels of the index to the columns (so they can be used for finding rules)
        for level in range(len(dataframe.index.names)):
            dataframe[dataframe.index.names[level]] = dataframe.index.get_level_values(level = level)
        for idx in df_patterns.index:
            # Calculate pattern statistics (from evaluating pandas expressions)
            pandas_co = df_patterns.loc[idx, PANDAS_CO]
            pandas_ex = df_patterns.loc[idx, PANDAS_EX]
            n_co = len(eval(pandas_co, encodings, {'df': dataframe}).index)
            n_ex = len(eval(pandas_ex, encodings, {'df': dataframe}).index)
            total = n_co + n_ex
            if total > 0:
                conf = np.round(n_co / total, 4)
            else:
                conf = 0
            df_patterns.loc[idx, SUPPORT] = n_co
            df_patterns.loc[idx, EXCEPTIONS] = n_ex
            df_patterns.loc[idx, CONFIDENCE] = conf
            df_new_patterns = df_patterns
        # deleting the levels of the index to the columns
        for level in range(len(dataframe.index.names)):
            del dataframe[dataframe.index.names[level]]
    return df_new_patterns

def get_encodings():
    for item in encodings_definitions:
        exec(encodings_definitions[item])
    encodings = {}
    for item in encodings_definitions.keys():
        encodings[item]= locals()[item]
    return encodings

def derive_results(dataframe = None,
                   P_dataframe = None,
                   Q_dataframe = None,
                   df_patterns = None):
    '''Results (patterns applied to data) are derived
       All info of the patterns is included in the results
    '''
    if (P_dataframe is not None) and (Q_dataframe is not None):
        try:
            dataframe = P_dataframe.join(Q_dataframe)
        except:
            print("Join of P_dataframe and Q_dataframe failed, overlapping columns?")
            return []

    encodings = get_encodings()

    if (dataframe is not None) and (df_patterns is not None):
        df = dataframe.copy()
        results = list()
        for idx in df_patterns.index:
            pandas_ex = df_patterns.loc[idx, PANDAS_EX]
            pandas_co = df_patterns.loc[idx, PANDAS_CO]
            results_ex = eval(pandas_ex, encodings, {'df': df}).index.values.tolist()
            results_co = eval(pandas_co, encodings, {'df': df}).index.values.tolist()
            for i in results_ex:
                # values_p = df.loc[i, df_patterns.loc[idx, P_COLUMNS]].values.tolist()
                # if type(df_patterns.loc[idx, Q_COLUMNS])==list:
                #     values_q = df.loc[i, df_patterns.loc[idx, Q_COLUMNS]].values.tolist()
                # else:
                #     values_q = df_patterns.loc[idx, Q_COLUMNS]
                values_p = ""
                values_q = ""
                results.append([False,
                                df_patterns.loc[idx, "pattern_id"],
                                df_patterns.loc[idx, "cluster"],
                                i,
                                df_patterns.loc[idx, "support"],
                                df_patterns.loc[idx, "exceptions"],
                                df_patterns.loc[idx, "confidence"],
                                df_patterns.loc[idx, "pattern_def"],
                                values_p,
                                values_q])
            for i in results_co:
                # values_p = df.loc[i, df_patterns.loc[idx, P_COLUMNS]].values.tolist()
                # if type(df_patterns.loc[idx, Q_COLUMNS])==list:
                #     values_q = df.loc[i, df_patterns.loc[idx, Q_COLUMNS]].values.tolist()
                # else:
                #     values_q = df_patterns.loc[idx, Q_COLUMNS]
                values_p = ""
                values_q = ""
                results.append([True,
                                df_patterns.loc[idx, "pattern_id"],
                                df_patterns.loc[idx, "cluster"],
                                i,
                                df_patterns.loc[idx, "support"],
                                df_patterns.loc[idx, "exceptions"],
                                df_patterns.loc[idx, "confidence"],
                                df_patterns.loc[idx, "pattern_def"],
                                values_p,
                                values_q])
        df_results = pd.DataFrame(data = results, columns = RESULTS_COLUMNS)
        df_results.sort_values(by = ["index", "confidence", "support"], ascending = [True, False, False], inplace = True)
        df_results.set_index(["index"], inplace = True)
        try:
            df_results.index = pd.MultiIndex.from_tuples(df_results.index)
        except:
            df_results.index = df_results.index
    return ResultDataFrame(df_results)

# def convert_columns(patterns = [],
#                     dataframe_input = None,
#                     dataframe_output = None):
#     '''
#     '''
#     new_patterns = list()
#     for pattern_id, pattern, pattern_stats, encode in patterns:
#         new_pattern = [ [dataframe_output.columns[dataframe_input.columns.get_loc(item)] for item in pattern[0]],
#                         pattern[1],
#                         [dataframe_output.columns[dataframe_input.columns.get_loc(item)] for item in pattern[2]]] + pattern[3:6]
#         new_encode = {dataframe_output.columns[dataframe_input.columns.get_loc(item)]: encode[item] for item in encode.keys()}
#         new_patterns.append([pattern_id, new_pattern, pattern_stats, new_encode])
#     return new_patterns


def derive_pattern_statistics(co):
    # co_sum is the support of the pattern
    co_sum = co.sum()
    #co_sum = optimized.apply_sum(co)
    ex_sum = len(co) - co_sum
    # conf is the confidence of the pattern
    conf = np.round(co_sum / (co_sum + ex_sum), 4)
    # oddsratio is a correlation measure
    #oddsratio = (1 + co_sum) / (1 + ex_sum)
    return co_sum, ex_sum, conf #, oddsratio

def derive_pattern_data(df,
                        P_columns,
                        Q_columns,
                        pattern,
                        name,
                        co,
                        confidence,
                        data_filter):
    '''
    '''
    # pattern statistics
    co_sum, ex_sum, conf = derive_pattern_statistics(co)
    # we only store the patterns with confidence higher than conf
    pattern_def = generate_single_expression(P_columns, Q_columns, pattern)
    if conf >= confidence:
        return [[name, 0], pattern_def, [co_sum, ex_sum, conf]]
    else:
        return []

def get_parameters(parameters):
    confidence = parameters.get("min_confidence", 0.75)
    support = parameters.get("min_support", 2)
    return confidence, support

def derive_column_value_pattern(dataframe = None,
                          pattern   = None,
                          pattern_name = "value",
                          columns   = None,
                          value     = None,
                          parameters= {}):
    '''Generate patterns of the form [c1] operator value where c1 is in columns
    '''
    confidence, support = get_parameters(parameters)
    data_array = dataframe.values.T
    for c in columns:
        # confirmations and exceptions of the pattern, a list of booleans
        co = reduce(operators[pattern], [data_array[c, :], value])
        pattern_data = derive_pattern_data(dataframe,
                                           [dataframe.columns[c]],
                                           value,
                                           pattern,
                                           pattern_name,
                                           co,
                                           confidence,
                                           None)
        if pattern_data and len(co) >= support:
            yield pattern_data

def derive_percentile_column_pattern(dataframe = None,
                          pattern   = None,
                          pattern_name = "value",
                          columns   = None,
                          parameters= {}):
    '''Generate patterns of the form [c1] operator value where c1 is in columns
    '''
    confidence, support = get_parameters(parameters)
    percentile = parameters['percentile']
    add_per = (100-percentile)/2
    data_array = dataframe.values.T
    for c in columns:
        # confirmations and exceptions of the pattern, a list of booleans
        upper = round(np.percentile(data_array[c, :], percentile + add_per),2)
        lower = round(np.percentile(data_array[c, :], add_per),2)

        co1 = reduce(operators['>='], [data_array[c, :], lower])
        co2 = reduce(operators['<='], [data_array[c, :], upper])
        co = np.logical_and(co1,co2)
        pattern_data = derive_pattern_data(dataframe,
                                           [dataframe.columns[c]],
                                           [lower, upper],
                                           pattern,
                                           pattern_name,
                                           co,
                                           confidence,
                                           None)
        if pattern_data and len(co) >= support:
            yield pattern_data

def derive_column_column_pattern(dataframe  = None,
                                 pattern    = None,
                                 pattern_name = "column",
                                 P_columns  = None,
                                 Q_columns  = None,
                                 parameters = {}):
    '''Generate patterns of the form [c1] operator [c2] where c1 and c2 are in columns
    '''
    confidence, support = get_parameters(parameters)
    decimal = parameters.get("decimal", 8)
    preprocess_operator = preprocess[pattern]
    initial_data_array = dataframe.values.T
    # set up boolean masks for nonzero items per column
    nonzero = initial_data_array != None
    for c0 in P_columns:
        for c1 in Q_columns:
            if c0 != c1:
                # applying the filter
                data_filter = reduce(preprocess_operator, [nonzero[c] for c in [c0, c1]])
                if data_filter.any():
                    data_array = initial_data_array[:, data_filter]
                    if data_array.any():
                        # confirmations of the pattern, a list of booleans
                        if pattern == "=":
                            co = np.abs(data_array[c0, :] - data_array[c1, :]) < 1.5 * 10**(-decimal)
                        else:
                            co = reduce(operators[pattern], data_array[[c0, c1], :])
                        pattern_data = derive_pattern_data(dataframe,
                                            [dataframe.columns[c0]],
                                            [dataframe.columns[c1]],
                                            pattern,
                                            pattern_name,
                                            co,
                                            confidence,
                                            data_filter)
                        if pattern_data and len(co) >= support:
                            yield pattern_data

def derive_sums_column_pattern(dataframe  = None,
                         pattern_name = None,
                         P_columns  = None,
                         Q_columns  = None,
                         parameters = {}):
    '''Generate patterns of the form sum [c1-list] = [c2] where c1-list is column list and c2 is column
    '''
    confidence, support = get_parameters(parameters)
    sum_elements = parameters.get("sum_elements", 2)
    decimal = parameters.get("decimal", 8)
    preprocess_operator = preprocess["sum"]
    initial_data_array = dataframe.values.T
    # set up boolean masks for nonzero items per column
    nonzero = (dataframe.values != 0).T
    n = len(dataframe.columns)
    # setup matrix to speed up proces (under development)
    # matrix = np.ones(shape = (n, n), dtype = bool)
    # for c in itertools.combinations(range(n), 2):
    #     v = (data_array[c[1], :] <= data_array[c[0], :] + 1).any() # all is too strict
    #     matrix[c[0], c[1]] = v
    #     matrix[c[1], c[0]] = ~v
    # np.fill_diagonal(matrix, False)

    for lhs_elements in range(2, sum_elements + 1):
        for rhs_column in Q_columns:
            start_array = initial_data_array
            # minus righthandside is taken so we can use sum function for all columns
            start_array[rhs_column, :] = -start_array[rhs_column, :]
            lhs_column_list = [col for col in P_columns if (col != rhs_column)]
            for lhs_columns in itertools.combinations(lhs_column_list, lhs_elements):
                all_columns = lhs_columns + (rhs_column,)
                data_filter = np.logical_and.reduce(nonzero[all_columns, :])
                if data_filter.any():
                    data_array = start_array[:, data_filter]
                    co = (abs(np.sum(data_array[all_columns, :], axis = 0)) < 1.5 * 10**(-decimal))
                    co_sum, ex_sum, conf = derive_pattern_statistics(co)
                    # we only store the patterns that satisfy criteria
                    if (conf >= confidence) and (co_sum >= support):
                        P_column = [dataframe.columns[c] for c in lhs_columns]
                        Q_column = [dataframe.columns[rhs_column]]
                        pattern_def = '({"' + P_column[0] + '"}'
                        for idx in range(len(P_column[1:])):
                            pattern_def += ' + {"' + P_column[idx+1]+ '"}'
                        pattern_def += ' = {"' + Q_column[0] + '"})'
                        pattern_data = [[pattern_name, 0],
                                        pattern_def,
                                        [co_sum, ex_sum, conf]]
                        if pattern_data:
                            yield pattern_data

def derive_ratio_pattern(dataframe  = None,
                   pattern_name = None,
                   P_columns  = None,
                   Q_columns  = None,
                   parameters = {}):
    """Generate patterns with ratios
    """
    confidence, support = get_parameters(parameters)
    limit_denominator = parameters.get("limit_denominator", 10000000)
    decimal = parameters.get("decimal", 8)
    preprocess_operator = preprocess["ratio"]
    # set up boolean masks for nonzero items per column
    nonzero = (dataframe.values != 0).T
    for c0 in P_columns:
        for c1 in Q_columns:
            if c0 != c1:
                # applying the filter
                data_filter = reduce(preprocess_operator, [nonzero[c] for c in [c0, c1]])
                data_array = map(lambda e: Fraction(e).limit_denominator(limit_denominator),
                                 dataframe.values[data_filter, c0] / dataframe.values[data_filter, c1])
                ratios = pd.Series(data_array)
                if support >= 2:
                    possible_ratios = ratios.loc[ratios.duplicated(keep = False)].unique()
                else:
                    possible_ratios = ratios.unique()
                for v in possible_ratios:
                    if (abs(v) > 1.5 * 10**(-decimal)) and (v > -1) and (v < 1):
                        # confirmations of the pattern, a list of booleans
                        co = ratios==v
                        co_sum, ex_sum, conf = derive_pattern_statistics(co)
                        if (conf >= confidence) and (co_sum >= support):
                            pattern_data = [[pattern_name, 0],
                                            [dataframe.columns[c0],
                                             'ratio',
                                            [dataframe.columns[c1]], '', '', ''],
                                            [co_sum, ex_sum, conf], {}]
                            if pattern_data:
                                yield pattern_data

def read_excel(filename = None,
               dataframe = None,
               sheet_name = 'Patterns'):
    df = pd.read_excel(filename, sheet_name = sheet_name)
    df.fillna('', inplace = True)
    # df[RELATION_TYPE] = df[RELATION_TYPE].str[1:]
    patterns = list()
    for row in df.index:
        print(df.loc[row, PATTERN_DEF])
        pattern_def = df.loc[row, PATTERN_DEF]
        encode = ast.literal_eval(df.loc[row, ENCODINGS])
        pandas_co = df.loc[row, PANDAS_CO]
        pandas_ex = df.loc[row, PANDAS_EX]
        xbrl_co = df.loc[row, XBRL_CO]
        xbrl_ex = df.loc[row, XBRL_EX]
        patterns.append([[df.loc[row, PATTERN_ID], 0],
                         pattern_def,
                         [0, 0, 0], pandas_co, pandas_ex, xbrl_co, xbrl_ex])
    df_patterns = to_dataframe(patterns = patterns, parameters = {})
    if dataframe is not None:
        df_patterns = update_statistics(dataframe = dataframe, df_patterns = df_patterns)
    return df_patterns

def find_redundant_patterns(df_patterns = None):
    '''This function checks whether there are redundant patterns and changes pattern status accordingly
    so if [A, B, C] -> [Z] has conf = 0.95 and support = 10 and
          [A, B] -> [Z] has equal or better statistics then the former pattern is redundant
    '''
    for row in df_patterns.index:
        p_columns = df_patterns.loc[row, P_COLUMNS]
        q_columns = df_patterns.loc[row, Q_COLUMNS]
        p_items = df_patterns.loc[row, 'P']
        if len(p_columns) > 2: # only
            # determine all possible subsets of P and check whether they are better
            p_subsets = list(itertools.combinations(p_columns, len(p_columns) - 1))
            for subset in p_subsets:
                P_dict = {col: p_items[idx] for idx, col in enumerate(subset)}
                for i, row2 in enumerate(df_patterns.index):
                    p_columns2 = df_patterns.loc[row2, P_COLUMNS]
                    q_columns2 = df_patterns.loc[row2, Q_COLUMNS]
                    p_item2 = df_patterns.loc[row2, 'P']
                    if (set(q_columns2) == set(q_columns)) and (len(p_columns2) == len(P_dict.keys())):
                        equal = True
                        for key in P_dict.keys():
                            if key not in p_columns2:
                                equal = False
                            else:
                                if P_dict[key] not in p_item2:
                                    equal = False
                                else:
                                    if P_dict[key] != p_item2[p_item2.index(P_dict[key])]:
                                        equal = False
                        if equal:
                            if (df_patterns.loc[row, 'confidence'] <= df_patterns.loc[row2, 'confidence']) and (df_patterns.loc[row, 'support'] <= df_patterns.loc[row2, 'support']):
                                df_patterns.loc[row, 'pattern status'] = "redundant with pattern " + str(row2)
    return df_patterns
