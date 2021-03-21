from arelle import ModelManager, Cntlr, ModelXbrl, XbrlConst, RenderingEvaluator, \
                   ViewFileRenderedGrid, ModelFormulaObject
from arelle import PackageManager, FileSource

import sys
import src
import pandas as pd
from os import listdir, walk, makedirs, environ
from os.path import isfile, join, exists, basename
from datetime import datetime
import click

# the taxonomy should be data/taxonomy/arelle
# the instances you want to use should be in data/instances

XBRL_TAXONOMY_PATH = join('data', 'taxonomies')
XBRL_INSTANCES_PATH = join('data', 'instances')

LANGUAGE: str = "en-GB"
environ['XDG_CONFIG_HOME']: str = XBRL_TAXONOMY_PATH

# The role defined in the model.xsd schema for resources representing codes of rows or columns is
euRCcode: str = 'http://www.eurofiling.info/xbrl/role/rc-code'

# Now we make a modelmanager
# logFileName = "logToPrint" -> logging is print to notebook
# logFileName = "arelle.log" -> logging is to filename (use .json or .xml for specific format)

controller = Cntlr.Cntlr(logFileName=join(XBRL_TAXONOMY_PATH, "arelle.log"),
                         logFileMode="w")
controller.webCache.workOffline = True
controller.logger.messageCodeFilter = None

modelmanager = ModelManager.initialize(controller)
modelmanager.defaultLang = LANGUAGE
modelmanager.formulaOptions = ModelFormulaObject.FormulaOptions()
modelmanager.loadCustomTransforms()

taxonomies: list = [f for f in listdir(XBRL_TAXONOMY_PATH) if isfile(join(XBRL_TAXONOMY_PATH, f)) and f[-3:] == 'zip']
PackageManager.init(controller)
for taxonomy in taxonomies:
    PackageManager.addPackage(controller, join(XBRL_TAXONOMY_PATH, taxonomy))
PackageManager.rebuildRemappings(controller)
PackageManager.save(controller)

taxo_choices: str = "\n".join([str(idx)+": "+str(item['name'])+
                    " v"+str(item['version']) 
                    for idx, item in enumerate(PackageManager.packagesConfig['packages'])])

# Now we make a modelmanager
# logFileName = "logToPrint" -> logging is print to notebook
# logFileName = "arelle.log" -> logging is to filename (use .json or .xml for specific format)

@click.command()
@click.option('--taxo', default=0, prompt=taxo_choices)
@click.option('--instance', default=join("data", "instances", "qrs_240_instance.xbrl"), prompt="input file")
@click.option('--output', default=XBRL_INSTANCES_PATH, prompt="output directory")
@click.option('--verbose_labels', default=False, prompt="verbose labels")

def main(taxo, instance, output, verbose_labels):

    subdir = join(XBRL_INSTANCES_PATH, basename(instance).split(".")[0])
    if not exists(subdir):
        makedirs(subdir)
    controller.startLogging(logFileName=join(subdir, basename(instance).split(".")[0]+'.log'), 
                            logFileMode="w")

    xbrl_instance = ModelXbrl.load(modelManager = modelmanager, url = instance)
    RenderingEvaluator.init(xbrl_instance)


    tables = list(xbrl_instance.modelRenderingTables)
    tables.sort(key = lambda table: table.genLabel(lang = LANGUAGE,strip = True, role = euRCcode))

    for table in tables:
        obj = src.generateCSV.generateCSVTables(xbrl_instance, subdir, 
                                                table = table, 
                                                lang = LANGUAGE,
                                                verbose_labels = verbose_labels)

    df_closed_axis = pd.DataFrame()  
    for table in tables:
        table_name = table.genLabel(lang = LANGUAGE,strip = True, role = euRCcode)
        if exists(join(subdir, table_name + '.pickle')):
            df = pd.read_pickle(join(subdir, table_name + '.pickle'))  # read dataframe
            if df.index.nlevels == 2:  # if 2 indexes (entity, period) --> closed axis table
                if len(df_closed_axis) == 0:  
                    # no data yet --> copy dataframe
                    df_closed_axis = df.copy()
                else:  
                    # join to existing dataframe
                    df_closed_axis = df_closed_axis.join(df)

    df_closed_axis.to_pickle(join(subdir, basename(instance).split(".")[0])+'.pickle')


if __name__ == "__main__":
    sys.exit(main())

