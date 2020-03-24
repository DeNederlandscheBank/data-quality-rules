
import os
import pandas as pd
import re

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

from typing import List, Union
from collections import defaultdict

emptySet = set()
emptyList = []

def generateCSVTables(modelXbrl, results_path, lang="en", table_uri=None):
    return GenerateCSVTables(modelXbrl, lang).generate(results_path, table_uri)
    
class GenerateCSVTables(object):
    def __init__(self, modelXbrl, lang):
        self.modelXbrl = modelXbrl
        self.processedXbrl = ProcessXbrl(xbrl = modelXbrl)
        self.labels = []
        for dim in self.processedXbrl.dimensions:
            self.labels.append((dim.uri, dim.labels))
        self.lang = lang

        class nonTkBooleanVar():
            def __init__(self, value=True):
                self.value = value
            def set(self, value):
                self.value = value
            def get(self):
                return self.value

        # context menu boolean vars (non-tkinter boolean
        self.ignoreDimValidity = nonTkBooleanVar(value=True)
        self.xAxisChildrenFirst = nonTkBooleanVar(value=True)
        self.yAxisChildrenFirst = nonTkBooleanVar(value=False)

    def generate(self, results_path = None, table_uri = None):
        # generate for one table_uri is it is given, otherwise all available table_uris
        if table_uri is not None:
            table_uris = (table_uri,)
        else:
            table_uris = self.modelXbrl.relationshipSet("Table-rendering").linkRoleUris

        for table_uri in table_uris:
            df = pd.DataFrame()
            self.zOrdinateChoices = {}
            tblAxisRelSet, xTopNode, yTopNode, zTopNode = resolveAxesStructure(self, table_uri)
            self.hasTableFilters = bool(self.modelTable.filterRelationships)
            self.zStrNodesWithChoices = []
            if tblAxisRelSet:
                tableLabel = (self.modelTable.genLabel(lang=self.lang, strip=True) or self.roledefinition)
                zAspectNodes = defaultdict(set)
                self.zAxis(zTopNode, zAspectNodes, False)
                xNodes = []
                if (xTopNode and xTopNode.childStructuralNodes):
                    self.xAxis(xTopNode, xNodes)
                self.bodyCells(yTopNode, xNodes, zAspectNodes, df)
            df.to_csv(os.path.join(results_path if results_path else '.', os.path.basename(table_uri) + ".csv"))
        return None
        
    # def yAxisByRow(self, yParentNode):
    #     if yParentNode is not None:
    #         for yNode in yParentNode.childStructuralNodes:
    #             self.yAxisByRow(yNode)
    #             if yNode.isLabeled:
    #                 label = yNode.header(lang=self.lang,
    #                                      returnGenLabel=isinstance(yNode.definitionNode, ModelClosedDefinitionNode),
    #                                      recurseParent=not isinstance(yNode.definitionNode, ModelFilterDefinitionNode))
    #                 isAbstract = (yNode.isAbstract or 
    #                               (yNode.childStructuralNodes and
    #                                not isinstance(yNode.definitionNode, (ModelClosedDefinitionNode, ModelEuAxisCoord))))
    #                 if not isAbstract:
    #                     for i, role in enumerate(self.rowHdrNonStdRoles):
    #                         hdr = yNode.header(role=role, lang=self.lang)
    #                         print(label + ": " + hdr)
    #         return None

    def zAxis(self, zNode, zAspectNodes, discriminatorsTable):
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
                self.zAxis(zNode, zAspectNodes, discriminatorsTable)
                            
    def xAxis(self, xParent, xChilds):
        for xChild in xParent.childStructuralNodes:
            if not xChild.isAbstract:
                xChilds.append(xChild)
            self.xAxis(xChild, xChilds)
            
    def bodyCells(self, yParent, xNodes, zAspectNodes, df):

        if yParent is not None:
            dimDefaults = self.modelXbrl.qnameDimensionDefaults
            for yNode in yParent.childStructuralNodes:

                if not (yNode.isAbstract or (yNode.childStructuralNodes and
                         not isinstance(yNode.definitionNode, (ModelClosedDefinitionNode, ModelEuAxisCoord)))) and yNode.isLabeled:

                    # define verbose labels and row labels
                    label_y = yNode.header(lang=self.lang,
                                  returnGenLabel=isinstance(yNode.definitionNode, ModelClosedDefinitionNode),
                                  recurseParent=not isinstance(yNode.definitionNode, ModelFilterDefinitionNode))

                    index_name = ""
                    for role in self.rowHdrNonStdRoles:
                        index_name = yNode.header(role=role, lang=self.lang)

                    short_y = yNode.header(role=self.rowHdrNonStdRoles[0], lang=self.lang)

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
                        conceptNotAbstract = concept is None or not concept.isAbstract
                        fact = None
                        value = None
                        objectId = None
                        justify = None
                        fp = FactPrototype(self, cellAspectValues)
                        if conceptNotAbstract:
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
                                        value = fact.effectiveValue
                                    break

                        # define verbose and column labels 
                        label_x = xNode.header(lang=self.lang,
                                               returnGenLabel=isinstance(xNode.definitionNode, 
                                                                (ModelClosedDefinitionNode, ModelEuAxisCoord)))
                        short_x = xNode.header(role=self.colHdrNonStdRoles[0], lang=self.lang) or "\u00A0"

                        if type(value)==str:
                            for label in self.labels:
                                if label[1]['concept_id'] == value[0:6]:
                                    for child in label[1]['children']:
                                        if (child['concept_id'][4:])==(value[7:]):
                                            value = child['label']
                        if short_y[0]!="R": # we have a z-axis
                            # a = list(str(aspect) for aspect in matchableAspects if not aspectMatches(self.rendrCntx, fact, fp, aspect))
                            # print(str(a))
                            # print(fact.qname)
                            # print(fact.contextID)
                            # print(fact.effectiveValue[:32])
                            # print(fact.modelDocument.basename)
                            # print(fact.sourceline)
                            data_point_def  = str(self.roledefinition) + ","+ str(short_x).lower()
#                            df.index = pd.MultiIndex.from_tuples([], names=['entity', 'key'])
                            df.loc[label_y, data_point_def] = value
                            df.index.name = str(self.roledefinition) + "," + index_name
                        else:
                            data_point_def  = str(self.roledefinition) + "," + str(label_y).lower() + ","+ str(label_x).lower()
                            df.loc[0, data_point_def] = value
                        fp.clear()
                self.bodyCells(yNode, xNodes, zAspectNodes, df)
        return None

def get_label_list(relationship_set, concepts, relationship=None):
    if relationship is None:
        if len(relationship_set.modelRelationships) > 0:
            preferred = relationship_set.modelRelationships[0].preferredLabel
        else:
            preferred = None
    else:
        preferred = relationship.preferredLabel

    label = concepts.label(lang='en') if preferred is None \
        else concepts.label(preferredLabel=preferred, lang='en')

    res = {
        'concept_id': concepts.id,
        'order': 1.0 if relationship is None else relationship.order,
        'label': label,
        'isAbstract': concepts.isAbstract,
        'children': []
    }

    new_relationship_set = relationship_set.fromModelObject(concepts)
    if len(new_relationship_set) > 0:
        new_relationship_set.sort(key=lambda x: x.order)
        for rel in new_relationship_set:
            new_concepts = rel.viewConcept
            res['children'].append(get_label_list(relationship_set, new_concepts, relationship=rel))
    return res


class Dimension(object):
    def __init__(self, parent, xbrl, code, definition, uri):
        self.parent = parent
        self.code = code
        self.definition = definition
        self.uri = uri
        self._xbrl = xbrl
        self._labels = None

    @property
    def labels(self):
        if self._labels is None:
            arcrole = XbrlConst.parentChild
            relationship_set = self._xbrl.relationshipSet(arcrole, self.uri)
            root_concept = relationship_set.rootConcepts[0]
            labels = get_label_list(relationship_set, root_concept)
            self._labels = labels
        return self._labels


class ProcessXbrl(object):
    def __init__(self, xbrl: ModelXbrl):
        self.xbrl = xbrl
        self._dims = None
        self._link_roles = None

    @property
    def dimensions(self) -> List[Dimension]:
        if self._dims is not None:
            return self._dims

        arcrole = XbrlConst.parentChild
        relationship = self.xbrl.relationshipSet(arcrole)

        dims = None
        if relationship is not None:
            dims = []
            for uri in relationship.linkRoleUris:
                role_types = self.xbrl.roleTypes.get(uri)

                if role_types is not None:
                    definition = (role_types[0].genLabel(lang='en', strip=True)
                                  or role_types[0].definition or uri)
                else:
                    definition = uri

                role_code = re.search(r"\[(.*?)\]", definition)
                role_code = role_code.group(1) if role_code else None
                dims.append(Dimension(self, self.xbrl, role_code, definition, uri))
        self._dims = dims
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


class ProcessXbrl(object):
    def __init__(self, xbrl: ModelXbrl):
        self.xbrl = xbrl
        self._dims = None
        self._link_roles = None

    @property
    def dimensions(self) -> List[Dimension]:
        if self._dims is not None:
            return self._dims

        arcrole = XbrlConst.parentChild
        relationship = self.xbrl.relationshipSet(arcrole)

        dims = None
        if relationship is not None:
            dims = []
            for uri in relationship.linkRoleUris:
                role_types = self.xbrl.roleTypes.get(uri)

                if role_types is not None:
                    definition = (role_types[0].genLabel(lang='en', strip=True)
                                  or role_types[0].definition or uri)
                else:
                    definition = uri

                role_code = re.search(r"\[(.*?)\]", definition)
                role_code = role_code.group(1) if role_code else None
                dims.append(Dimension(self, self.xbrl, role_code, definition, uri))
        self._dims = dims
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
