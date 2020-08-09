import os
import pandas as pd
import re
import ast
import functools
import src

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
 
from typing import List, Union
from collections import defaultdict
 
emptySet = set()
emptyList = []
 
def generateCSVTables(modelXbrl, results_path, lang = "en", table_uri = None):
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
        self.xAxisChildrenFirst = nonTkBooleanVar(value=True)
        self.yAxisChildrenFirst = nonTkBooleanVar(value=False)
 
    def generate(self, results_path = None, table_uri = None):
        # generate for one table_uri is it is given, otherwise all available table_uris
        if table_uri is not None:
            table_uris = (table_uri,)
        else:
            table_uris = self.modelXbrl.relationshipSet("Table-rendering").linkRoleUris
 
        for table_uri in table_uris:
 
            self.zOrdinateChoices = {}
 
            self.modelXbrl.modelManager.addToLog(_("generating template {0}").format(os.path.basename(table_uri)))
 
            df = pd.DataFrame()
 
            self.modelXbrl.modelManager.addToLog(" ... resolving axes structure")
            tblAxisRelSet, xTopNode, yTopNode, zTopNode = resolveAxesStructure(self, table_uri)
 
            self.hasTableFilters = bool(self.modelTable.filterRelationships)
            self.zStrNodesWithChoices = []
 
            if tblAxisRelSet:
                tableLabel = (self.modelTable.genLabel(lang=self.lang, strip=True) or self.roledefinition)
                zAspectNodes = defaultdict(set)
                self.zAxis(zTopNode, zAspectNodes, False)
 
                xNodes = []
                if (xTopNode and xTopNode.childStructuralNodes):
                    self.collect_nodes(xTopNode, xNodes)

                yNodes = []
                if (yTopNode and yTopNode.childStructuralNodes):
                    self.collect_nodes(yTopNode, yNodes)
 
                self.index_values = {}
                self.index_names = {}
                self.z_axis = False
 
                self.yAxisByRow(1, self.dataFirstRow,
                                yTopNode, self.yAxisChildrenFirst.get(), True)

#                self.modelXbrl.modelManager.addToLog(" ... storing xAspectNodes")
                self.xAspectNodes_dict = {}
                for i, xNode in enumerate(xNodes):
                    xAspectNodes = defaultdict(set)
                    for aspect in aspectModels[self.aspectModel]:
                        if xNode.hasAspect(aspect):
                            if aspect == Aspect.DIMENSIONS:
                                for dim in (xNode.aspectValue(Aspect.DIMENSIONS) or emptyList):
                                    xAspectNodes[dim].add(xNode)
                            else:
                                xAspectNodes[aspect].add(xNode)
                    self.xAspectNodes_dict[xNode] = xAspectNodes

#                self.modelXbrl.modelManager.addToLog(" ... storing yAspectNodes")
                self.yAspectNodes_dict = {}
                for i, yNode in enumerate(yNodes):
                    yAspectNodes = defaultdict(set)
                    for aspect in aspectModels[self.aspectModel]:
                        if yNode.hasAspect(aspect):
                            if aspect == Aspect.DIMENSIONS:
                                for dim in (yNode.aspectValue(Aspect.DIMENSIONS) or emptyList):
                                    yAspectNodes[dim].add(yNode)
                            else:
                                yAspectNodes[aspect].add(yNode)
                    self.yAspectNodes_dict[yNode] = yAspectNodes
 
                self.modelXbrl.modelManager.addToLog(" ... filling table content")
                self.bodyCells(self.dataFirstRow, yNodes, xNodes, zAspectNodes, df)
 
            if (self.z_axis == True):
                try:
                    df.index = pd.MultiIndex.from_tuples([tuple(ast.literal_eval(l)) for l in df.index])
                except:
                    df.index = df.index
 
                df.index.names = ['level ' + str(i) for i in range(df.index.nlevels)]
 
            # writing results to csv and pickle
            path_name = os.path.join(results_path if results_path else '.')
            file_name = os.path.basename(table_uri)
            self.modelXbrl.modelManager.addToLog(_(" ... writing results to {0}").format(os.path.join(path_name, file_name)+'.csv'))
            df.to_csv(os.path.join(path_name, file_name) + ".csv")
            df.to_pickle(os.path.join(path_name, file_name) + ".pickle")
 
        return self
      
    def yAxisByRow(self, leftCol, row, yParentNode, childrenFirst, renderNow):
 
        if row not in self.index_values.keys():
            self.index_values[row] = []
 
        if row not in self.index_names.keys():
            self.index_names[row] = []
 
        if yParentNode is not None:
            nestedBottomRow = row
            for yNode in yParentNode.childStructuralNodes:
                nestRow, nextRow = self.yAxisByRow(leftCol + 1, row, yNode,
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
                        for i, role in enumerate(self.rowHdrNonStdRoles):
                            hdr = yNode.header(role=role, lang=self.lang)
                            self.index_names[row].append(hdr or "\u00A0")
 
                if isNonAbstract:
                    row += 1
                elif childrenFirst:
                    row = nextRow
                if nestRow > nestedBottomRow:
                    nestedBottomRow = nestRow + (isNonAbstract and not childrenFirst)
                if row > nestedBottomRow:
                    nestedBottomRow = row
                if not childrenFirst:
                    dummy, row = self.yAxisByRow(leftCol + 1, row, yNode, childrenFirst, renderNow)
            return (nestedBottomRow, row)
   
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
                           
    def collect_nodes(self, Parent, Childs):
        for Child in Parent.childStructuralNodes:
            if not Child.isAbstract:
                Childs.append(Child)
            self.collect_nodes(Child, Childs)
 
    def bodyCells(self, row, yNodes, xNodes, zAspectNodes, df):
 
#        self.modelXbrl.modelManager.addToLog(_("body cells called {0}").format(str(row)))

        dimDefaults = self.modelXbrl.qnameDimensionDefaults
 
        for yNode in yNodes:
            for xNode in xNodes:
                # if isinstance(yNode.definitionNode, ModelFilterDefinitionNode):
                #     print("Facts in yNode: " + str(len(yNode.factsPartition)))
                cellTagSelectors = yNode.tagSelectors | xNode.tagSelectors
                cellAspectValues = {}
                matchableAspects = set()
                for aspect in _DICT_SET(self.xAspectNodes_dict[xNode].keys()) | _DICT_SET(self.yAspectNodes_dict[yNode].keys()) | _DICT_SET(zAspectNodes.keys()):
                    aspectValue = xNode.inheritedAspectValue(yNode,
                                       self, aspect, cellTagSelectors,
                                       self.xAspectNodes_dict[xNode], 
                                       self.yAspectNodes_dict[yNode], 
                                       zAspectNodes)
                    # value is None for a dimension whose value is to be not reported in this slice
                    if (isinstance(aspect, _INT) or  # not a dimension
                        dimDefaults.get(aspect) != aspectValue or aspectValue is not None):
                        cellAspectValues[aspect] = aspectValue
                    matchableAspects.add(aspectModelAspect.get(aspect,aspect)) #filterable aspect from rule aspect

                cellDefaultedDims = _DICT_SET(dimDefaults) - _DICT_SET(cellAspectValues.keys())
                priItemQname = cellAspectValues.get(Aspect.CONCEPT)
                concept = self.modelXbrl.qnameConcepts.get(priItemQname)
                value = 0.0

                fp = FactPrototype(self, cellAspectValues)

                if (concept is None) or (not concept.isAbstract):
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

                    if isinstance(yNode.definitionNode, ModelFilterDefinitionNode):
                        inter = facts.intersection(yNode.factsPartition)
                        for fact in inter:
                            if yNode.hasValueExpression(xNode):
                                # this code is not reached with example instance
                                value = yNode.evalValueExpression(fact, xNode)
                            else:
                                value = parse_value(fact)
                            break;
                    else:        
                        for fact in facts:
                            if (all(aspectMatches(self.rendrCntx, fact, fp, aspect) for aspect in matchableAspects) and
                                all(fact.context.dimMemberQname(dim, includeDefaults = True) in (dimDefaults[dim], None)
                                    for dim in cellDefaultedDims)):
                                if yNode.hasValueExpression(xNode):
                                    # this code is not reached with example instance
                                    value = yNode.evalValueExpression(fact, xNode)
                                else:
                                    value = parse_value(fact)
                                break

                # store value in dataframe
                self.store_datapoint(xNode, yNode, row, value, df)

#                fp.clear()

            row += 1

        return row

    def store_datapoint(self, xNode, yNode, row, value, df):

        # define verbose labels and row labels
        label_y = yNode.header(lang=self.lang,
                      returnGenLabel=isinstance(yNode.definitionNode, ModelClosedDefinitionNode),
                      recurseParent=not isinstance(yNode.definitionNode, ModelFilterDefinitionNode))

        short_y = ""
        for i, role in enumerate(self.colHdrNonStdRoles):
            short_y += yNode.header(role=role, lang=self.lang) or "\u00A0"

        # define verbose and column labels
        label_x = xNode.header(lang=self.lang,
                               returnGenLabel=isinstance(xNode.definitionNode,
                                                (ModelClosedDefinitionNode, ModelEuAxisCoord)))

        short_x = ""
        for i, role in enumerate(self.colHdrNonStdRoles):
            short_x += xNode.header(role=role, lang=self.lang) or "\u00A0"
       
        # find label in taxonomy, should be replaced by tree search
        if type(value)==str:
            for label in self.labels:
                if label[1]['concept_id'] == value[0:6]:
                    for child in label[1]['children']:
                        if (child['concept_id'][4:])==(value[7:]):
                            value = child['label']
                        else:
                            for child2 in child['children']:
                                if (child2['concept_id'][4:])==(value[7:]):
                                    value = child2['label']

        if short_y[0] != "R": # we have a z-axis
            # a = list(str(aspect) for aspect in matchableAspects if not aspectMatches(self.rendrCntx, fact, fp, aspect))
            # print(str(a))
            # print(fact.qname)
            # print(fact.contextID)                            # print(fact.value)
            # print(fact.modelDocument.basename)
            # print(fact.sourceline)
            data_point_def = str(self.roledefinition) + ","+ str(short_x).lower()
            df.loc[str(self.index_values[row]), data_point_def] = value
            self.z_axis = True
        else:
            data_point_def  = str(self.roledefinition) + "," + str(short_y).lower() + ","+ str(short_x).lower()
            df.loc[0, data_point_def] = value
 
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
