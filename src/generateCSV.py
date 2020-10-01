# -*- coding: utf-8 -*-

"""Code to extract csv-files with data per template from XBRL instance
"""

import os
import pandas as pd
import re
import ast

from lxml import etree
from arelle import ViewFile, XbrlConst
from arelle.ModelFormulaObject import Aspect, aspectModels, aspectRuleAspects, aspectModelAspect, aspectStr
from arelle.RenderingResolver import resolveAxesStructure, RENDER_UNITS_PER_CHAR
from arelle.ModelObject import ModelObject
from arelle.FormulaEvaluator import aspectMatches
from arelle.ModelInstanceObject import ModelDimensionValue
from arelle.ModelValue import QName
from arelle.ModelXbrl import DEFAULT, ModelXbrl
from arelle.ModelRenderingObject import (ModelClosedDefinitionNode, ModelEuAxisCoord, ModelFilterDefinitionNode,
                                         OPEN_ASPECT_ENTRY_SURROGATE)
from arelle.PrototypeInstanceObject import FactPrototype
from arelle.ValidateXbrlDimensions import isFactDimensionallyValid
from arelle.ValidateInfoset import validateRenderingInfoset

from arelle import ModelValue
from arelle.ValidateXbrlCalcs import roundValue
from arelle import XmlUtil

from typing import List, Union
from collections import defaultdict

emptySet = set()
emptyList = []

# The role defined in the model.xsd schema for resources representing codes of rows or columns is
euRCcode = 'http://www.eurofiling.info/xbrl/role/rc-code'

def generateCSVTables(modelXbrl, results_path, lang = "en", table = None, verbose_labels = False):
    return GenerateCSVTables(modelXbrl, lang, verbose_labels).generate(results_path, table)
    
class GenerateCSVTables(object):
    def __init__(self, modelXbrl, lang, verbose_labels):
        self.modelXbrl = modelXbrl
        self.lang = lang
        self.verbose_labels = verbose_labels
        self.processedXbrl = ProcessXbrl(modelXbrl = modelXbrl, lang = lang)
        self.FTK = False

        # create a quick way to find the labels from the taxonomy
        self.labels = []
        for dim in self.processedXbrl.dimensions:
            self.labels.append((dim.uri, dim.labels))

        def child_loop(parent, concept_id, label_dict):
            for child in parent['children']:
                label_dict[concept_id + ":" + child['concept_id'][4:]] = child['label']
                child_loop(child, concept_id, label_dict)

        self.label_dict = dict()
        for label in self.labels:
            concept_id = label[1]['concept_id']
            child_loop(label[1], concept_id, self.label_dict)

        class nonTkBooleanVar():
            def __init__(self, value=True):
                self.value = value
            def set(self, value):
                self.value = value
            def get(self):
                return self.value

        # context menu boolean vars (non-tkinter boolean)
        self.ignoreDimValidity = nonTkBooleanVar(value=True)
        self.xAxisChildrenFirst = nonTkBooleanVar(value=True)
        self.yAxisChildrenFirst = nonTkBooleanVar(value=False)

    def generate(self, results_path = None, table = None):
        # generate for one table_uri is it is given, otherwise all available table_uris
        if table is not None:
            tables = (table,)
        else:
            tables = list(self.modelXbrl.modelRenderingTables)

        for table in tables:

            self.zOrdinateChoices = {}

            self.tableLabel = (table.genLabel(lang=self.lang, strip=True, role = euRCcode) or self.roledefinition)
#            self.modelXbrl.modelManager.addToLog(_("generating template {0}").format(self.tableLabel))

            # self.modelXbrl.modelManager.addToLog(" ... resolving axes structure")
            tblAxisRelSet, xTopNode, yTopNode, zTopNode = resolveAxesStructure(self, table)

            self.hasTableFilters = bool(self.modelTable.filterRelationships)
            self.zStrNodesWithChoices = []

            if tblAxisRelSet:

                zAspectNodes = defaultdict(set)
                self.extract_zAxis(zTopNode, zAspectNodes, False)

                xNodes = []
                if (xTopNode and xTopNode.childStructuralNodes):
                    self.extract_columns(xTopNode, xNodes)

                self.index_values = {}
                self.z_axis = False

                self.extract_indices(1, self.dataFirstRow,
                                yTopNode, self.yAxisChildrenFirst.get(), True)

                # derive index names directly from taxonomy
                index_names = []
                for item in list(self.modelTable.modelXbrl.relationshipSet((XbrlConst.tableBreakdown)).fromModelObject(self.modelTable)):
                    if len(item.toModelObject.definitionLabelsView) == 4:
                        if self.FTK:
                            index_names.append("FTK." + self.tableLabel + "," + item.toModelObject.genLabel(lang = self.lang, strip = True, role = euRCcode))
                        else:
                            index_names.append(self.tableLabel + "," + item.toModelObject.genLabel(lang = self.lang, strip = True, role = euRCcode))
                        self.z_axis = True

                # self.modelXbrl.modelManager.addToLog(" ... filling table content")
                df = pd.DataFrame(index = pd.MultiIndex.from_tuples((), names=['entity', 'period'] + index_names))
                self.extract_content(self.dataFirstRow, yTopNode, xNodes, zAspectNodes, df)
                df = df[df.columns.sort_values()]
                
            if not df.empty:
                path_name = os.path.join(results_path if results_path else '.')
                if not os.path.exists(path_name):
                    os.makedirs(path_name)
                    self.modelXbrl.modelManager.addToLog(_(" ... directory {0} created").format(path_name))
                if self.FTK:
                    file_name = os.path.join(path_name, "FTK." + self.tableLabel)
                else:
                    file_name = os.path.join(path_name, self.tableLabel)
                self.modelXbrl.modelManager.addToLog(_(" ... saved output {0}").format(file_name + '.csv and .pickle'))
                df.to_csv(file_name + ".csv")
                df.to_pickle(file_name + ".pickle")
            else:
                self.modelXbrl.modelManager.addToLog(" ... empty dataframe, no csv-file saved")

        return self
       
    def extract_indices(self, leftCol, row, yParentNode, childrenFirst, renderNow):

        if row not in self.index_values.keys():
            self.index_values[row] = []

        if yParentNode is not None:
            nestedBottomRow = row
            for yNode in yParentNode.childStructuralNodes:
                nestRow, nextRow = self.extract_indices(leftCol + 1, row, yNode,
                                        childrenFirst, childrenFirst)
                isAbstract = (yNode.isAbstract or 
                              (yNode.childStructuralNodes and
                               not isinstance(yNode.definitionNode, (ModelClosedDefinitionNode, ModelEuAxisCoord))))
                isNonAbstract = not isAbstract
                isLabeled = yNode.isLabeled
                topRow = row
                if renderNow and isLabeled:
                    label = yNode.header(lang=self.lang,
                                         returnGenLabel=isinstance(yNode.definitionNode, ModelClosedDefinitionNode),
                                         recurseParent=not isinstance(yNode.definitionNode, ModelFilterDefinitionNode))
                    #print ( "row {0} topRow {1} nxtRow {2} col {3} renderNow {4} label {5}".format(row, topRow, nextRow, leftCol, renderNow, label))
                    self.index_values[row].append(label)

                if isNonAbstract:
                    row += 1
                elif childrenFirst:
                    row = nextRow
                if nestRow > nestedBottomRow:
                    nestedBottomRow = nestRow + (isNonAbstract and not childrenFirst)
                if row > nestedBottomRow:
                    nestedBottomRow = row
                if not childrenFirst:
                    dummy, row = self.extract_indices(leftCol + 1, row, yNode, childrenFirst, renderNow) 
            return (nestedBottomRow, row)
    
    def extract_zAxis(self, zNode, zAspectNodes, discriminatorsTable):
        if zNode is not None:
            effectiveNode = zNode
            if zNode.choiceStructuralNodes: # same as combo box selection in GUI mode
                if not discriminatorsTable:
                    self.zStrNodesWithChoices.insert(0, zNode) # iteration from last is first
                try:
                    effectiveNode = zNode.choiceStructuralNodes[zNode.choiceNodeIndex]
                except KeyError:
                    pass
            for aspect in aspectModels[self.aspectModel]:
                if effectiveNode.hasAspect(aspect, inherit=True): #implies inheriting from other z axes
                    if aspect == Aspect.DIMENSIONS:
                        for dim in (effectiveNode.aspectValue(Aspect.DIMENSIONS, inherit=True) or emptyList):
                            zAspectNodes[dim].add(effectiveNode)
                    else:
                        zAspectNodes[aspect].add(effectiveNode)
            for zNode in zNode.childStructuralNodes:
                self.extract_zAxis(zNode, zAspectNodes, discriminatorsTable)
                            
    def extract_columns(self, xParent, xChilds):
        for xChild in xParent.childStructuralNodes:
            if not xChild.isAbstract:
                xChilds.append(xChild)
            self.extract_columns(xChild, xChilds)

    def extract_content(self, row, yParent, xNodes, zAspectNodes, df):

        dimDefaults = self.modelXbrl.qnameDimensionDefaults

        if yParent is not None:
            for yNode in yParent.childStructuralNodes:

                isAbstract = (yNode.isAbstract or 
                              (yNode.childStructuralNodes and
                               not isinstance(yNode.definitionNode, (ModelClosedDefinitionNode, ModelEuAxisCoord))))

                if not isAbstract and yNode.isLabeled:

                    isEntryPrototype = yNode.isEntryPrototype(default=False) # row to enter open aspects
                    yAspectNodes = defaultdict(set)
                    for aspect in aspectModels[self.aspectModel]:
                        if yNode.hasAspect(aspect):
                            if aspect == Aspect.DIMENSIONS:
                                for dim in (yNode.aspectValue(Aspect.DIMENSIONS) or emptyList):
                                    yAspectNodes[dim].add(yNode)
                            else:
                                yAspectNodes[aspect].add(yNode)
                    yTagSelectors = yNode.tagSelectors

                    ignoreDimValidity = self.ignoreDimValidity.get()
                    for i, xNode in enumerate(xNodes):
                        xAspectNodes = defaultdict(set)
                        for aspect in aspectModels[self.aspectModel]:
                            if xNode.hasAspect(aspect):
                                if aspect == Aspect.DIMENSIONS:
                                    for dim in (xNode.aspectValue(Aspect.DIMENSIONS) or emptyList):
                                        xAspectNodes[dim].add(xNode)
                                else:
                                    xAspectNodes[aspect].add(xNode)
                        cellTagSelectors = yTagSelectors | xNode.tagSelectors
                        cellAspectValues = {}
                        matchableAspects = set()
                        for aspect in _DICT_SET(xAspectNodes.keys()) | _DICT_SET(yAspectNodes.keys()) | _DICT_SET(zAspectNodes.keys()):
                            aspectValue = xNode.inheritedAspectValue(yNode,
                                               self, aspect, cellTagSelectors, 
                                               xAspectNodes, yAspectNodes, zAspectNodes)
                            # value is None for a dimension whose value is to be not reported in this slice
                            if (isinstance(aspect, _INT) or  # not a dimension
                                dimDefaults.get(aspect) != aspectValue or aspectValue is not None):
                                cellAspectValues[aspect] = aspectValue
                            matchableAspects.add(aspectModelAspect.get(aspect,aspect)) #filterable aspect from rule aspect
                        cellDefaultedDims = _DICT_SET(dimDefaults) - _DICT_SET(cellAspectValues.keys())
                        priItemQname = cellAspectValues.get(Aspect.CONCEPT)
                        concept = self.modelXbrl.qnameConcepts.get(priItemQname)
                        fp = FactPrototype(self, cellAspectValues)
                        value = 0
                        if concept is None or not concept.isAbstract:
                            if isinstance(yNode.definitionNode, ModelFilterDefinitionNode):
                                facts = set(yNode.factsPartition)
                            else:
                                # reduce set of matchable facts to those with pri item qname and have dimension aspects
                                facts = self.modelXbrl.factsByQname[priItemQname] if priItemQname else self.modelXbrl.factsInInstance
                                if self.hasTableFilters:
                                    facts = self.modelTable.filterFacts(self.rendrCntx, facts)

                            for aspect in matchableAspects:  # trim down facts with explicit dimensions match or just present
                                if isinstance(aspect, QName):
                                    aspectValue = cellAspectValues.get(aspect, None)
                                    if isinstance(aspectValue, ModelDimensionValue):
                                        if aspectValue.isExplicit:
                                            dimMemQname = aspectValue.memberQname # match facts with this explicit value
                                        else:
                                            dimMemQname = None  # match facts that report this dimension
                                    elif isinstance(aspectValue, QName): 
                                        dimMemQname = aspectValue  # match facts that have this explicit value
                                    elif aspectValue is None: # match typed dims that don't report this value
                                        dimMemQname = DEFAULT
                                    else:
                                        dimMemQname = None # match facts that report this dimension
                                    facts = facts & self.modelXbrl.factsByDimMemQname(aspect, dimMemQname)

                            for fact in facts:
                                if (all(aspectMatches(self.rendrCntx, fact, fp, aspect) for aspect in matchableAspects) and
                                    all(fact.context.dimMemberQname(dim,includeDefaults=True) in (dimDefaults[dim], None)
                                        for dim in cellDefaultedDims)):
                                    if yNode.hasValueExpression(xNode):
                                        value = yNode.evalValueExpression(fact, xNode)
                                    else:
                                        value = parse_value(fact)
                                    reporting_period = XmlUtil.dateunionValue(fact.context.instantDatetime, subtractOneDay=True)
                                    reporting_entity = fact.context.entityIdentifier[1]
                                    self.store_value(value, row, df, xNode, yNode, reporting_entity, reporting_period)
                                    break
                        fp.clear()
                    row += 1
                row = self.extract_content(row, yNode, xNodes, zAspectNodes, df)
        return row

    def store_value(self, value, row, df, xNode, yNode, reporting_entity, reporting_period):

        # define verbose labels and row labels
        short_y = yNode.header(role = euRCcode, lang = self.lang) or "\u00A0"
        short_x = xNode.header(role = euRCcode, lang = self.lang) or "\u00A0"
        if self.verbose_labels:
            label_y = yNode.header(lang = self.lang,
                                   returnGenLabel = isinstance(yNode.definitionNode, ModelClosedDefinitionNode),
                                   recurseParent = not isinstance(yNode.definitionNode, ModelFilterDefinitionNode))
            label_x = xNode.header(lang = self.lang,
                                   returnGenLabel = isinstance(xNode.definitionNode,
                                                    (ModelClosedDefinitionNode, ModelEuAxisCoord)))
        else:
            label_y = short_y
            label_x = short_x
        
        # find label in taxonomy
        if type(value)==str:
             if value in self.label_dict.keys():
                 value = self.label_dict[value]

        # put value in dataframe with proper indices and columns
        if self.z_axis:
            if len(label_x)==3:
                column_name = "FTK." + str(self.tableLabel) + ",C"+ str(label_x).upper()
                self.FTK = True
            else:
                column_name = str(self.tableLabel) + ","+ str(label_x).upper()
            df.loc[tuple([reporting_entity, reporting_period] + self.index_values[row]), column_name] = value
        else:
            if len(label_x)==3:
                column_name = "FTK." + str(self.tableLabel) + ",R" + str(label_y).upper() + ",C" + str(label_x).upper()
                self.FTK = True
            else:
                column_name = str(self.tableLabel) + "," + str(label_y).upper() + ","+ str(label_x).upper()
            df.loc[tuple([reporting_entity, reporting_period]), column_name] = value

        return None

def parse_value(fact):
    '''Parse value to Python datatype
    '''
    concept = fact.concept  # type: ModelConcept
    if concept is None or concept.isTuple or fact.isNil:
        return None
    if concept.isFraction:
        num, den = map(fractions.Fraction, fact.fractionValue)
        return num / den
    val = fact.value.strip()
    if concept.isInteger:
        return int(val)
    elif concept.isNumeric:
        dec = fact.decimals
        if dec is None or dec == "INF":  # show using decimals or reported format
            dec = len(val.partition(".")[2])
        else:  # max decimals at 28
            dec = max(min(int(dec), 28), -28)  # 2.7 wants short int, 3.2 takes regular int, don't use _INT here
        num = float(roundValue(val, fact.precision, dec))  # round using reported decimals
        return num
    elif concept.baseXbrliType == 'dateItemType':
        return ModelValue.dateTime(val).strftime("%Y-%m-%d %H:%M:%S")
    elif concept.baseXbrliType == 'booleanItemType':
        return val.lower() in ('1', 'true')
    return val

def get_label_list(relationship_set, concepts, relationship = None, lang = "en"):
    if relationship is None:
        if len(relationship_set.modelRelationships) > 0:
            preferred = relationship_set.modelRelationships[0].preferredLabel
        else:
            preferred = None
    else:
        preferred = relationship.preferredLabel

    label = concepts.label(lang = lang) if preferred is None \
        else concepts.label(preferredLabel=preferred, lang=lang)

    res = {'concept_id': concepts.id,
           'order': 1.0 if relationship is None else relationship.order,
           'label': label,
           'isAbstract': concepts.isAbstract,
           'children': []}

    new_relationship_set = relationship_set.fromModelObject(concepts)
    if len(new_relationship_set) > 0:
        new_relationship_set.sort(key=lambda x: x.order)
        for rel in new_relationship_set:
            new_concepts = rel.viewConcept
            res['children'].append(get_label_list(relationship_set, new_concepts, rel, lang))
    return res

class Dimension(object):
    def __init__(self, parent, modelXbrl, lang, code, definition, uri):
        self.parent = parent
        self.modelXbrl = modelXbrl
        self.code = code
        self.lang = lang
        self.definition = definition
        self.uri = uri
        self._labels = None

    @property
    def labels(self):
        if self._labels is None:
            relationship_set = self.modelXbrl.relationshipSet(XbrlConst.parentChild, self.uri)
            root_concept = relationship_set.rootConcepts[0]
            labels = get_label_list(relationship_set, root_concept, None, self.lang)
            self._labels = labels
        return self._labels

class ProcessXbrl(object):
    def __init__(self, modelXbrl, lang = "en"):
        self.modelXbrl = modelXbrl
        self.lang = lang
        self.dims = None

    @property
    def dimensions(self) -> List[Dimension]:
        if self.dims is not None:
            return self.dims
        relationship = self.modelXbrl.relationshipSet(XbrlConst.parentChild)
        dims = None
        if relationship is not None:
            dims = []
            for uri in relationship.linkRoleUris:
                role_types = self.modelXbrl.roleTypes.get(uri)
                if role_types is not None:
                    definition = (role_types[0].genLabel(lang = self.lang, strip=True)
                                  or role_types[0].definition or uri)
                else:
                    definition = uri
                role_code = re.search(r"\[(.*?)\]", definition)
                role_code = role_code.group(1) if role_code else None
                dims.append(Dimension(self, self.modelXbrl, self.lang, role_code, definition, uri))
        self.dims = dims
        return dims

    def get_dim_by_code(self, code: str) -> Union[Dimension, None]:
        for dim in self.dims:
            if (dim.code is not None) and code is not None:
                if compare_str(dim.code, code):
                    return dim
        return None

    def __repr__(self):
        df = self.get_document_information()
        columns = df.columns.tolist()
        dict_info = df.set_index(columns[1]).to_dict()
        info = None
        for key, value in dict_info.items():
            if key != 'label':
                info = value
        return str(info)

def saveCSVTablesMenuExtender(cntlr, menu, *args, **kwargs):
    # Extend menu with an item for the save infoset plugin
    menu.add_command(label="Save Solvency 2 CSV Tables", 
                     underline=0, 
                     command=lambda: saveCSVTablesMenuCommand(cntlr) )

def saveCSVTablesMenuCommand(cntlr):
    # save Infoset menu item has been invoked
    from arelle.ModelDocument import Type
    if cntlr.modelManager is None or cntlr.modelManager.modelXbrl is None:
        cntlr.addToLog("No DTS loaded.")
        return
        # get file name into which to save log file while in foreground thread
    indexFile = cntlr.uiFileDialog("save",
            title=_("arelle - Save Solvency 2 Instance into CSV"),
            initialdir=cntlr.config.setdefault("csvTablesFileDir","."),
            filetypes=[(_("CSV index file .csv"), "*.csv")],
            defaultextension=".csv")
    if not indexFile:
        return False
    import os
    cntlr.config["csvTablesFileDir"] = os.path.dirname(indexFile)
    cntlr.saveConfig()

    import threading
    thread = threading.Thread(target=lambda 
                                  _dts=cntlr.modelManager.modelXbrl,
                                  _indexFile=indexFile: 
                                        getDataFrame(_dts, _indexFile))
    thread.daemon = True
    thread.start()

def saveCSVTablesCommandLineOptionExtender(parser, *args, **kwargs):
    # extend command line options with a save CSV Tables
    parser.add_option("--save-instance", 
                      action="store", 
                      dest="CSVTableset", 
                      help=_("Save Solvency 2 instance into CSV."))

def saveCSVTablesCommandLineXbrlLoaded(cntlr, options, modelXbrl, *args, **kwargs):
    from arelle.ModelDocument import Type
    if getattr(options, "CSVTableset", None) and options.CSVTableset == "generateCSVFiles" and modelXbrl.modelDocument.type in (Type.TESTCASESINDEX, Type.TESTCASE):
        cntlr.modelManager.generateCSVFiles = True

def saveCSVTablesCommandLineXbrlRun(cntlr, options, modelXbrl, *args, **kwargs):
    if getattr(options, "CSVTableset", None) and options.generateCSVFiles != "generateCSVFiles":
        if cntlr.modelManager is None or cntlr.modelManager.modelXbrl is None:
            cntlr.addToLog("No taxonomy loaded.")
            return

        from arelle import RenderingEvaluator
        RenderingEvaluator.init(modelXbrl)
        generateCSVTables(cntlr.modelManager.modelXbrl, options.CSVTableset)
  

__pluginInfo__ = {
    'name': 'Save Solvency 2 XBRL Instance to CSV',
    'version': '0.0.1',
    'description': "This plug-in stores a Solvency 2 XBRL instance into CSV files.",
    'license': '',
    'author': '',
    'copyright': '',
    # classes of mount points (required)
    'CntlrWinMain.Menu.Tools' : saveCSVTablesMenuExtender,
    'CntlrCmdLine.Options'    : saveCSVTablesCommandLineOptionExtender,
    'CntlrCmdLine.Xbrl.Loaded': saveCSVTablesCommandLineXbrlLoaded,
    'CntlrCmdLine.Xbrl.Run'   : saveCSVTablesCommandLineXbrlRun,
}
