import pandas as pd
import re


def adjust_syntax(rules):
    """Adjust syntax of additional Solvency 2 validation rules"""

    # Correct template typo's
    rules['Formule'] = rules['Formule'].str.replace('S.08.01.01.01,c0380', 'S.08.01.01.02,c0380')
    rules['Formule'] = rules['Formule'].str.replace('S.08.01.01.01,c0430', 'S.08.01.01.02,c0430')
    rules['Formule'] = rules['Formule'].str.replace('S.08.01.04.01,c0380', 'S.08.01.04.02,c0380')
    rules['Formule'] = rules['Formule'].str.replace('S.08.01.04.01,c0430', 'S.08.01.04.02,c0430')
    rules['Formule'] = rules['Formule'].str.replace('S.08.02.01.01,c0320', 'S.08.02.01.02,c0320')
    rules['Formule'] = rules['Formule'].str.replace('S.08.02.04.01,c0320', 'S.08.02.04.02,c0320')

    # " " has to be converted to None
    rules['Formule'] = rules['Formule'].str.replace('" "','None')
    rules['Formule'] = rules['Formule'].str.replace('""','None')
    # <> . has to be converted to <> None
    rules['Formule'] = rules['Formule'].str.replace('<> \.','<> None')
    rules['Formule'] = rules['Formule'].str.replace('<>\.','<> None')
    rules['Formule'] = rules['Formule'].str.replace('< > \.','< > None')
    rules['Formule'] = rules['Formule'].str.replace('< >\.','< > None')
    # = . has to be converted to = None
    rules['Formule'] = rules['Formule'].str.replace('= \.','= None')
    rules['Formule'] = rules['Formule'].str.replace('=\.','= None')
    # <> has to be converted to !=
    rules['Formule'] = rules['Formule'].str.replace('<>','!=')
    rules['Formule'] = rules['Formule'].str.replace('< >','!=')
    # ; has to be converted to ,
    rules['Formule'] = rules['Formule'].str.replace(';',',')

    # Use of rNNN is unnecessary
    rules['Formule'] = rules['Formule'].str.replace('rNNN,','')
    # Use wildcard # instead of RNNN for summing instead of repeating over multiple rows, and make sure all rows are included
    rules.loc[rules['Formule'].str.contains('RNNN,'), 'Rijen'] = '(All)'
    rules['Formule'] = rules['Formule'].str.replace('RNNN,','#,')
    # Correct C\d\d\d\dC to C\d\d\d\d
    for item in [tuple(filter(None, tup)) for cols in rules['Kolommen'] for tup in re.findall(r"([Cc]\d\d\d\d)([Cc])", cols)]:
        rules['Kolommen'] = rules['Kolommen'].str.replace("".join(item),item[0])
    # Correct C\d\d\d to C0\d\d\d
    for item in [tuple(filter(None, tup)) for cols in rules['Kolommen'] for tup in re.findall(r"([^0-9])(\d\d\d)($|;|\))", cols)]:
        item = tuple((item[0], item[1], "")) if len(item) == 2 else tuple((item[0], item[1], item[2]))
        rules['Kolommen'] = rules['Kolommen'].str.replace("".join(item),item[0] + '0' + item[1] + item[2])
    # Split double row entries {R\d\d\d\d,R\d\d\d\d} into two entries, i.e. {R\d\d\d\d},{R\d\d\d\d}
    for item in [tuple(filter(None, tup)) for form in rules['Formule'] for tup in re.findall(r"([Rr]\d\d\d\d)(,)([Rr]\d\d\d\d)", form)]:
        rules['Formule'] = rules['Formule'].str.replace("".join(item),item[0] + "}" + item[1] + "{" + item[2])
    # Add template when not included in formula
    for item in [tuple((rules.loc[idx, 'HoofdTabel'],tuple(filter(None, tup)))) for idx in list(rules.index) for tup in re.findall(r"(\{)([CcRr]\d\d\d\d\})", rules.loc[idx, 'Formule'])]:
        rules['Formule'] = rules['Formule'].str.replace("".join(item[1]),item[1][0] + item[0] + "," + item[1][1])
    # Add comma to SUBSTR({}#,#) expression
    for item in [tuple(filter(None, tup)) for form in rules['Formule'] for tup in re.findall(r"(\})([0-9]{1,2})", form)]:
        rules['Formule'] = rules['Formule'].str.replace("".join(item), item[0] + "," + item[1])
    # Remove trailing comma in (#,#,#,) expression
    rules['Formule'] = rules['Formule'].str.replace(r",\)",")")

    # Some rules check dates to be filled by > 0, this has to be changed to <> None
    list_of_rules = ['S.15.01_105', 'S.15.01_107', 'S.23.04_111', 'S.23.04_112', 'S.23.04_121', 'S.23.04_122', 'S.23.04_133', 'S.23.04_144', 'S.23.04_145', 'S.30.01_105', 'S.30.01_106', 
                     'S.30.01_117', 'S.30.01_118', 'S.30.03_102', 'S.30.03_103', 'S.36.01_106', 'S.36.02_106', 'S.36.02_108', 'S.36.03_104', 'S.10.01_115', 'S.15.01_106', 'S.15.01_108',
                     'S.23.04_127', 'S.23.04_128', 'S.23.04_137', 'S.23.04_148', 'S.23.04_149']
    list_of_rules_adj = [rule for rule in list_of_rules if rule in list(rules.index)]
    if len(list_of_rules_adj) > 0:
        rules.loc[list_of_rules_adj, 'Formule'] = rules.loc[list_of_rules_adj, 'Formule'].str.replace("> 0",'<> None').str.replace(">0",'<> None')

    return rules