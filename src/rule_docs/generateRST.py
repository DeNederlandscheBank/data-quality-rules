import src
import pandas as pd
import re
import os
from os import listdir, walk, makedirs
from os.path import isfile, join, exists
from io import StringIO

def parse_formula(expr, syntax = "XBRL"):
    if syntax == "XBRL":
        pattern = r"(S\...\...\...\...),"
        rule_templates = []
        for item in re.findall(pattern, expr):
            rule_templates.append(item)
        l = pd.Series(data = rule_templates).sort_values()
        rule_templates = list(l.unique())
        pattern = r"\[.*\]"
        rule_ref = re.search(pattern, expr)
        if rule_ref:
            rule_ref = rule_ref.group(0)
        pattern = r"{{(.*?)}}"
        rule_datapoints = []
        if re.findall(pattern, expr)==[]:
            print(expr + ": no datapoints found")
        for item in re.findall(pattern, expr):
            rule_datapoints.append(item.replace(" ", ""))
        l = pd.Series(data = rule_datapoints).sort_values()
        rule_datapoints = list(l.unique())
        pattern = r"(BV.*?):"
        rule_id = re.search(pattern, expr).group(1)
    elif syntax=="EVA2":
        pattern = r"(S\...\...\...\...),"
        rule_templates = []
        for item in re.findall(pattern, expr):
            rule_templates.append(item)
        l = pd.Series(data = rule_templates).sort_values()
        rule_templates = list(l.unique())
        rule_ref = ""
        pattern = r"{(.*?)}"
        rule_datapoints = []
        if re.findall(pattern, expr)==[]:
            print(expr + ": no datapoints found")
        for item in re.findall(pattern, expr):
            rule_datapoints.append(item.replace(" ", ""))
        l = pd.Series(data = rule_datapoints).sort_values()
        rule_datapoints = list(l.unique())
        rule_id = None
    return rule_templates, rule_datapoints, rule_id, rule_ref

def write_file(filename, string):
    file = open(filename, "w", encoding = 'utf8')
    file.write(string.getvalue())
    file.close()

def header(io, text):
    io.write("=" * len(text) + "\n")
    io.write(text + "\n")
    io.write("=" * len(text) + "\n\n")
    return io

def section(io, text):
    io.write(text + "\n")
    io.write("-" * len(text) + "\n\n")
    return io

def write_rst(path, df, template_dict, datapoint_dict):
    for rule in df.index:
        for template in df.loc[rule, 'Rule templates']:
            string = StringIO()
            string = header(string, df.loc[rule,'Rule id'])
            string = section(string, "Rule definition")
            string.write(df.loc[rule, "Rule expression"] + "\n\n\n")
            # template references
            string = section(string, "Template references")
            for template in df.loc[rule, 'Rule templates']:
                if template in template_dict.keys():
                    string.write(template_dict[template] + "\n\n")
                else:
                    string.write(template + "\n")
            string.write("\n")
            # datapoints
            string = section(string, "Datapoints labels")
            for datapoint in df.loc[rule, "Rule datapoints"]:
                if datapoint in datapoint_dict.keys():
                    string.write(datapoint + " [" + datapoint_dict[datapoint] + "]\n\n")
                else:
                    string.write(datapoint + " [unknown label]\n")
            string.write("\n\n")
            # references (should be improved)
            rule_ref = df.loc[rule, 'Rule references']
            if rule_ref:
                string = section(string, "Datapoint references")
                string.write(rule_ref)
            write_file(join(path, template, df.loc[rule, 'Rule id']+".rst"), string)
            string.close()