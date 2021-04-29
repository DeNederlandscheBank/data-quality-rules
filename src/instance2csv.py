from arelle import ModelManager, Cntlr, ModelXbrl, XbrlConst, RenderingEvaluator, \
                   ViewFileRenderedGrid, ModelFormulaObject
from arelle import PackageManager, FileSource
import sys
from src import generateCSV
import pandas as pd
from os import listdir, walk, makedirs, environ
from os.path import isfile, join, exists, basename
from datetime import datetime
import click

# the taxonomy should be data/taxonomy/arelle
# the instances you want to use should be in data/instances

XBRL_TAXONOMY_PATH = join('data', 'taxonomies')
XBRL_INSTANCES_PATH = join('data', 'instances')
LANGUAGE = "en-GB"
euRCcode = 'http://www.eurofiling.info/xbrl/role/rc-code'

taxonomies = [f for f in listdir(XBRL_TAXONOMY_PATH) if isfile(join(XBRL_TAXONOMY_PATH, f)) and f[-3:] == 'zip']

environ['XDG_CONFIG_HOME'] = XBRL_TAXONOMY_PATH

taxo_choices = "Choose taxonomy:\n"+"\n".join([str(idx)+": "+str(item) 
                  for idx, item in enumerate(taxonomies)])


instances: list = [f for f in listdir(XBRL_INSTANCES_PATH) if isfile(join(XBRL_INSTANCES_PATH, f)) and f[-4:].lower()=='xbrl']
instance_choices: str = "Choose instance file:\n"+"\n".join([str(idx)+": "+item
                                 for idx, item in enumerate(instances) if item!='actual'])

@click.command()
@click.option('--taxo', default=0, prompt=taxo_choices)
@click.option('--instance', default=0, prompt=instance_choices)
@click.option('--output', default=XBRL_INSTANCES_PATH, prompt="output directory")
@click.option('--verbose_labels', default=False, prompt="verbose labels")

def main(taxo, instance, output, verbose_labels):

    if taxo not in range(0, len(taxonomies)):
        print("ERROR: incorrect taxonomy choice.")
        return 0
    if instance not in range(0, len(instances)):
        print("ERROR: incorrect instance choice.")
        return 0
    if verbose_labels not in [True, False]:
        print("ERROR: incorrect verbose label choice.")
        return 0

    instance = join(XBRL_INSTANCES_PATH, instances[instance])

    subdir = join(XBRL_INSTANCES_PATH, basename(instance).split(".")[0])
    if not exists(subdir):
        makedirs(subdir)

    logFileName = join(subdir, basename(instance).split(".")[0]+'.log')

    controller = Cntlr.Cntlr(logFileName=join(XBRL_TAXONOMY_PATH, "arelle.log"), logFileMode="w")
    controller.webCache.workOffline = True
    controller.logger.messageCodeFilter = None

    modelmanager = ModelManager.initialize(controller)
    modelmanager.defaultLang = LANGUAGE
    modelmanager.formulaOptions = ModelFormulaObject.FormulaOptions()
    modelmanager.loadCustomTransforms()

    if isfile(join(XBRL_TAXONOMY_PATH, "taxonomyPackages.json")):
        os.remove(join(XBRL_TAXONOMY_PATH, "taxonomyPackages.json"))

    taxos = [taxonomies[taxo]]
    PackageManager.init(controller)
    for taxonomy in taxos:
        PackageManager.addPackage(controller, join(XBRL_TAXONOMY_PATH, taxonomy))
    PackageManager.rebuildRemappings(controller)
    PackageManager.save(controller)

    controller.startLogging(logFileName=logFileName, logFileMode="w")

    print("... Reading instance file ...")
    xbrl_instance = ModelXbrl.load(modelManager = modelmanager, url = instance)
    RenderingEvaluator.init(xbrl_instance)

    print("... generating pickle and csv: ", end='')
    tables = list(xbrl_instance.modelRenderingTables)
    tables.sort(key = lambda table: table.genLabel(lang = LANGUAGE,strip = True, role = euRCcode))
    for table in tables:
        obj = generateCSV.generateCSVTables(xbrl_instance, subdir, 
                                                table = table, 
                                                lang = LANGUAGE,
                                                verbose_labels = verbose_labels)
        print(".", end='')
    print("")

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

    print("... generating closed axis pickle ")
    df_closed_axis.to_pickle(join(subdir, basename(instance).split(".")[0])+'.pickle')


if __name__ == "__main__":
    sys.exit(main())
