# -*- coding: utf-8 -*-

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from arelle import ModelManager, Cntlr, ModelFormulaObject, ModelXbrl, ViewFileFormulae, XbrlConst, RenderingEvaluator

import src

import pandas as pd
from os import listdir, walk, makedirs, environ
from os.path import isfile, join, exists, basename
from io import StringIO

DIR = join('C:\\', 'Users', 'wjwil', '20_local_data', 'xbrl')

@click.command()
@click.option('--dir', default=DIR, help='The directory of the .xbrl-files')

def main(dir):
    """
    """
    logger = logging.getLogger(__name__)

    LANGUAGE     = "en-GB"
    # make sure you have a 'arelle' directory in the data_path! (This is where the taxonomy is stored)
    XBRL_DATA_PATH    = join('C:\\', 'Users' ,'wjwil', '20_local_data', 'xbrl')
    XBRL_RESULTS_PATH = join("..", "data")
    # set the location of taxonomy
    environ['XDG_CONFIG_HOME'] = XBRL_DATA_PATH
 
    DOCS_PATH = "docs\\"
    DATA_PATH = "data\\"
    RULES_PATH = "solvency2-rules\\"
    TAXO_NAME = "EIOPA Validation rules_2.4.0"

    controller = Cntlr.Cntlr()
    controller.webCache.workOffline = True

    modelmanager = ModelManager.initialize(controller)
    modelmanager.defaultLang = LANGUAGE
    modelmanager.formulaOptions = ModelFormulaObject.FormulaOptions()
    modelmanager.loadCustomTransforms()

    logger.info('Make docs started')
    logger.info('Docs directory:  %s' % DOCS_PATH)
    logger.info('Data directory:  %s' % DATA_PATH)
    logger.info('Rules directory:  %s' % RULES_PATH)
    logger.info('Xbrl data directory:  %s' % XBRL_DATA_PATH)

    # FILENAME_TAXO = 'simple_taxo.csv'
    # df_taxo = pd.read_csv(join(DATA_PATH, FILENAME_TAXO))
    # datapoint_dict = {}
    # for row in df_taxo.index:
    #     label = df_taxo.loc[row, 'label']
    #     datapoint_dict[df_taxo.loc[row, 'datapoint']] = str(label)  

    instances = [file for file in listdir(XBRL_DATA_PATH) if file.endswith(".xbrl")]

    for file in instances:
        logger.info('-- loading instance %s' % file)
        xbrl_instance = ModelXbrl.load(modelmanager, join(XBRL_DATA_PATH, file))
        logger.info('-- instance loaded')

        # Generate English rc labels
        tables = list(xbrl_instance.relationshipSet("Table-rendering").linkRoleUris)
        RenderingEvaluator.init(xbrl_instance)
        datapoint_dict = src.rc2label.rc2label_dict(xbrl_instance)

        # Generate English table labels
        template_dict = {}
        linkRoleUris = xbrl_instance.relationshipSet("Table-rendering").linkRoleUris
        for role_uri in linkRoleUris:
            definition = basename(role_uri)
            tblAxisRelSet = xbrl_instance.relationshipSet(XbrlConst.euTableAxis, role_uri)
            if len(tblAxisRelSet.modelRelationships)==0:
                tblAxisRelSet = xbrl_instance.relationshipSet((XbrlConst.tableBreakdown, XbrlConst.tableBreakdownMMDD, XbrlConst.tableBreakdown201305, XbrlConst.tableBreakdown201301, XbrlConst.tableAxis2011), role_uri)
            for rootconcept in tblAxisRelSet.rootConcepts:
                template_dict[rootconcept.definitionLabelsView[2][1]] = rootconcept.definitionLabelsView[3][1]

        ViewFileFormulae.viewFormulae(xbrl_instance, DATA_PATH + "formulae.csv", "header", None)
        formulae = pd.read_csv(DATA_PATH + "formulae.csv")
        df_xbrl = formulae[formulae['Expression'].str[0:2]=="BV"]

        logger.info('-- number of formulae %s' % str(len(df_xbrl.index)))

        df = pd.DataFrame()
        for row in df_xbrl.index:
            expr = df_xbrl.loc[row, 'Expression']
            label = df_xbrl.loc[row, 'Label']
            rule_templates, rule_datapoints, rule_id, rule_ref = src.parse_formula(expr, syntax = "XBRL")
            rule_date = "Unknown"
            df = df.append(pd.DataFrame(data = [[rule_id, label, rule_templates, rule_datapoints, rule_ref, expr]]), ignore_index = True)

        if not df.empty:
            df.columns = ['Rule id', 'Rule label', 'Rule templates', 'Rule datapoints', 'Rule references', 'Rule expression']
            all_templates = []
            for row in df.index:
                all_templates.extend(df.loc[row, "Rule templates"])
            templates = list(pd.Series(data = all_templates).sort_values().unique())

            for template in templates:
                if not exists(join(DOCS_PATH, TAXO_NAME, file[0:3], template)):
                    makedirs(join(DOCS_PATH, TAXO_NAME, file[0:3], template))
            logger.info('-- writing reST files')
            src.write_rst(join(DOCS_PATH, TAXO_NAME, file[0:3]), df, template_dict, datapoint_dict)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
