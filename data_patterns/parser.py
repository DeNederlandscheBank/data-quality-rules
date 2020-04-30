# -*- coding: utf-8 -*-

import re
import operator

def logical_equivalence(*c):
    nonzero_c1 = (c[0] != 0)
    nonzero_c2 = (c[1] != 0)
    return ((nonzero_c1 & nonzero_c2) | (~nonzero_c1 & ~nonzero_c2))

# implication
def logical_implication(*c):
    nonzero_c1 = (c[0] != 0)
    nonzero_c2 = (c[1] != 0)
    return ~(nonzero_c1 & ~nonzero_c2)

operators = {'>' : operator.gt,
             '<' : operator.lt,
             '>=': operator.ge,
             '<=': operator.le,
             '=' : operator.eq,
             '!=': operator.ne,
             '<->': logical_equivalence,
             '-->': logical_implication}

preprocess = {'>':   operator.and_,
              '<':   operator.and_,
              '>=':  operator.and_,
              '<=':  operator.and_,
              '=' :  operator.and_,
              '!=':  operator.and_,
              'sum': operator.and_,
              'ratio': operator.and_,
              '<->': operator.or_,
              '-->': operator.or_}

logicals = {
        '&': operator.and_,
        '|': operator.or_,
        '^':operator.xor
}

def generate_single_expression(P_columns, Q_columns, pattern):
    if pattern == 'percentile':
            expression = '({"' + P_columns[0] + '"} ' + '>=' + ' ' +  str(Q_columns[0])  + ') & ({"' + P_columns[0] + '"} ' + '<=' + ' ' +  str(Q_columns[1])  + ')'
    elif pattern == 'sum':
        expression = '({"' + P_columns[0] + '"}'
        for idx in range(len(P_columns[1:])):
            expression += ' + {"' + P_columns[idx+1]+ '"}'
        expression += ' = {"' + Q_columns[0] + '"})'
        return expression
    elif isinstance(Q_columns, list):
        expression = '({"' + P_columns[0] + '"} ' + pattern + ' {"' + Q_columns[0] + '"})'
    else:
        expression = '({"' + P_columns[0] + '"} ' + pattern + ' ' + str(Q_columns) + ')'
    for idx in range(len(P_columns[1:])):
        expression += " & " + '({"' + P_columns[idx+1]+ '"} ' + pattern + ' {"'+ Q_columns[idx+1] + '"})'
    return expression

def generate_conditional_expression(P_columns, P_values, Q_columns, Q_values, parameters):
    '''this function generates the conditional expression from P/Q_columns and P/Q_values'''

    P_operators = parameters.get("P_operators", ['='] * len(P_columns))
    # operators between Q_column and Q_value, default is =
    Q_operators = parameters.get("Q_operators", ['='] * len(Q_columns))
    # logical operators between P expressions, default is &
    P_logics = parameters.get("P_logics", ['&'] * (len(P_columns) - 1))
    # logical operators between Q expressions, default is &
    Q_logics = parameters.get("Q_logics", ['&'] * (len(Q_columns) - 1))

    # Boolean that is set to True if we want to also look for patterns the other way around
    both_ways = parameters.get("both_ways", False)

    pattern = "IF "
    if isinstance(P_values[0], str):
        pattern += '({"' + str(P_columns[0]) + '"} ' + P_operators[0] + ' "'+ P_values[0] + '")'
    else: # numerical value
        pattern += '({"' + str(P_columns[0]) + '"} ' + P_operators[0] + ' ' + str(P_values[0]) + ')'
    for idx in range(len(P_columns[1:])):
        if isinstance(P_values[idx+1], str):
            pattern += ' ' + P_logics[idx] + ' ({"' + str(P_columns[idx+1]) + '"} ' + P_operators[idx+1] + ' "'+ P_values[idx+1] + '")'
        else: # numerical value
            pattern += ' ' + P_logics[idx] + ' ({"' + str(P_columns[idx+1]) + '"} ' + P_operators[idx+1] + ' ' + str(P_values[idx+1]) + ')'
    pattern += " THEN "
    if isinstance(Q_values[0], str):
        pattern += '({"' + str(Q_columns[0]) + '"} ' + Q_operators[0] + ' "' + Q_values[0] + '")'
    else: # numerical value
        pattern += '({"' + str(Q_columns[0]) + '"} ' + Q_operators[0] + ' ' + str(Q_values[0]) + ')'
    for idx in range(len(Q_columns[1:])):
        if isinstance(Q_values[idx+1], str):
            pattern += ' ' + Q_logics[idx] + ' ({"' + str(Q_columns[idx+1]) + '"} ' + Q_operators[idx+1] + ' "' + Q_values[idx+1]+ '")'
        else: # numerical value
            pattern += ' ' + Q_logics[idx] + ' ({"' + str(Q_columns[idx+1]) + '"} ' + Q_operators[idx+1] + ' ' + str(Q_values[idx+1]) + ')'

    if both_ways:
        pattern += " AND IF "
        if isinstance(P_values[0], str):
            pattern += '~({"' + str(P_columns[0]) + '"} ' + P_operators[0] + ' "'+ str(P_values[0]) + '")'
        else: # numerical value
            pattern += '~({"' + str(P_columns[0]) + '"} ' + P_operators[0] + ' ' + str(P_values[0]) + ')'
        for idx in range(len(P_columns[1:])):
            if isinstance(P_values[idx+1], str):
                pattern += ' ' + P_logics[idx] + ' {"' + str(P_columns[idx+1]) + '"} ' + P_operators[idx+1] + ' "'+ str(P_values[idx+1]) + '"'
            else: # numerical value
                pattern += ' ' + P_logics[idx] + ' {"' + str(P_columns[idx+1]) + '"} ' + P_operators[idx+1] + ' ' + str(P_values[idx+1])
        pattern += " THEN "
        if isinstance(Q_values[0], str):
            pattern += '~({"' + str(Q_columns[0]) + '"} ' + Q_operators[0] + ' "' + str(Q_values[0]) + '")'
        else: # numerical value
            pattern += '~({"' + str(Q_columns[0]) + '"} ' + Q_operators[0] + ' ' + str(Q_values[0]) + ')'
        for idx in range(len(Q_columns[1:])):
            if isinstance(Q_values[idx+1], str):
                pattern += ' ' + Q_logics[idx] + ' ({"' + str(Q_columns[idx+1]) + '"} ' + Q_operators[idx+1] + ' "' + str(Q_values[idx+1]) + '")'
            else: # numerical value
                pattern += ' ' + Q_logics[idx] + ' ({"' + str(Q_columns[idx+1]) + '"} ' + Q_operators[idx+1] + ' ' + str(Q_values[idx+1]) + ')'

    return pattern

def evaluate_excel_string(s):
    if s != '':
        if type(s)==str:
            return ast.literal_eval(s)
        else:
            return s
    else:
        return s

def to_xbrl_expressions(pattern, encode, parameters):
    """Placeholder for XBRL"""
    return ["", ""]

def replace_and_or(s):
    """Replace and by & and or by |, but not within strings"""
    if re.search(r"(.*?)\'(.*?)\'(.*)", s) is None: # input text does not contain strings
        s = s.replace("OR", "|")
        s = s.replace("AND", "&")
    for item in re.findall(r"(.*?)\'(.*?)\'(.*)", s):
        s = s.replace(item[0], item[0].replace("OR", "|"))
        s = s.replace(item[0], item[0].replace("AND", "&"))
        s = s.replace(item[2], replace_and_or(item[2]))
    return s

def replace_div_by_zero(s):
    """Replace division by adding a smal value to numerator"""
    item = re.search(r"{(.*?)}(/)({.*?})", s)
    if item is not None: # input text does not contain strings
        k = s.rfind("/")
        s = s[:k] + ".divide(" + s[k+1:].replace(item.group(3), item.group(3) + '.replace([0], -1))')
    return s

def preprocess_pattern(pattern, parameters):
    solvency = parameters.get("solvency", False)

    pattern = pattern.replace("=" , "==")
    pattern = pattern.replace(">==" , ">=")
    pattern = pattern.replace("<==" , "<=")
    pattern = pattern.replace('!==', '!=')
    pattern = pattern.replace("<>", "!=")
    pattern = pattern.replace("< >", "!=") # the space between < and > should be deleted in EVA2
    pattern = pattern.replace('"', "'")
    pattern = pattern.replace(" )", ")")
    pattern = pattern.replace(';', ",") # this should be corrected in EVA2

    if solvency:
        pattern = replace_and_or(pattern)
        pattern = replace_div_by_zero(pattern)
    return pattern

def datapoints2pandas(s, encode):
    """Transform datapoints to Pandas datapoints
    Examples:
    {column_name} -> df[column_name]
    {column_name} -> encoded(df[column_name]) where column_name is in encoding definitions
    """
    nonzero_col = []
    res = s
    for item in re.findall(r'{(.*?)}', res):
        if item[1:-1] in encode.keys():
            res = res.replace("{"+item+"}", encode[item[1:-1]] + "(df["+item+"])")
        else:
            res = res.replace("{"+item+"}", "df["+item+"]")
        nonzero_col.append("df["+item+"]")
    return res, nonzero_col

def add_brackets(s, decimal = 8):
    """Add brackets around expressions with & and |
    """
    item = re.search(r'(.*)([&|\|])(.*)', s) # & and | takes priority over other functions like ==
    if item is not None:
        return '('+add_brackets(item.group(1))+') '+item.group(2).strip()+' ('+add_brackets(item.group(3))+')'
    else:
        item = re.search(r'(.*)([>|<|!=|<=|>=|==])(.*)', s)
        if item is not None:
            return add_brackets(item.group(1)) + item.group(2).strip() + add_brackets(item.group(3))
        else:
            return s.strip()

def expression2pandas(g, nonzero_col, parameters):
    """Transform conditional expression to Pandas code"""

    exclude_zero_columns = parameters.get("nonzero", False)
    both_ways = parameters.get("both_ways", False)
    decimal = parameters.get("decimal", 8)
    if re.search('AND', g):
        both_ways = True
    if decimal != 0:
        decimal = -decimal

    item = re.search(r'IF(.*)THEN(.*)', g)
    if item is not None:
        if both_ways:
            item = re.search(r'(.*)AND(.*)', g)
            item = re.search(r'IF(.*)THEN(.*)', item.group(1))
            co_str = 'df[(('+add_brackets(item.group(1))+') & ('+add_brackets(item.group(2))+")) | (~("+add_brackets(item.group(1)) +")& ~("+add_brackets(item.group(2))+ "))]"
            ex_str = 'df[('+add_brackets(item.group(1))+') & ~('+add_brackets(item.group(2))+") | (~("+add_brackets(item.group(1)) +")& ("+add_brackets(item.group(2))+ "))]"
        else:
            co_str = 'df[('+add_brackets(item.group(1))+') & ('+add_brackets(item.group(2))+")]"
            ex_str = 'df[('+add_brackets(item.group(1))+') & ~('+add_brackets(item.group(2))+")]"
    else:
        item = re.search(r'(.*)(==)(.*)', g)
        if item is None or (isinstance(item.group(3),str) and item.group(3)[:3] != ' df' and item.group(3)[:1] != '{'): # take out strings except when string is from sum
            co_str = 'df[('+add_brackets(g)+')&'
            ex_str = 'df[~('+add_brackets(g)+')&'
            if exclude_zero_columns:
                for i in nonzero_col:
                    co_str += '(' + i +'!=0)&'
                    ex_str += '(' + i +'!=0)&'
            co_str = co_str[:-1] + ']'
            ex_str = ex_str[:-1] + ']'
        else:
            g_co = 'abs('+ item.group(1).strip() + '-' + item.group(3).strip() + ')<1.5e' + str(decimal)
            g_ex = 'abs(' + item.group(1).strip() + '-' + item.group(3).strip() + ')>=1.5e' + str(decimal)
            co_str = 'df[('+g_co+')&'
            ex_str = 'df[('+g_ex+')&'
            if exclude_zero_columns:
                for i in nonzero_col:
                    co_str += '(' + i +'!=0)&'
                    ex_str += '(' + i +'!=0)&'
            co_str = co_str[:-1] + ']'
            ex_str = ex_str[:-1] + ']'
    return co_str, ex_str
