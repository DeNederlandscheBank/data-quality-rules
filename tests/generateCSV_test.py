#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for generateCSV.py"""

import unittest
import os
from datetime import datetime
import filecmp
from arelle import ModelManager, Cntlr, ModelXbrl, XbrlConst, RenderingEvaluator, \
                   ViewFileRenderedGrid, ModelFormulaObject
from arelle import PackageManager, FileSource
import src

XBRL_TAXONOMIES_PATH = os.path.join('data', 'taxonomies')
XBRL_INSTANCES_PATH = os.path.join('tests', 'data', 'test_instances')
LANGUAGE = "en-GB"
euRCcode = 'http://www.eurofiling.info/xbrl/role/rc-code'

taxonomies = ['EIOPA_SolvencyII_XBRL_Taxonomy_2.6.0_hotfix_with_External_Files.zip']

os.environ['XDG_CONFIG_HOME'] = XBRL_TAXONOMIES_PATH

controller = Cntlr.Cntlr(logFileName = os.path.join('tests', "unittests.log"), logFileMode="w")
controller.webCache.workOffline = True
controller.logger.messageCodeFilter = None

modelmanager = ModelManager.initialize(controller)
modelmanager.defaultLang = LANGUAGE
modelmanager.formulaOptions = ModelFormulaObject.FormulaOptions()
modelmanager.loadCustomTransforms()

PackageManager.init(controller)
for taxonomy in taxonomies:
    PackageManager.addPackage(controller, os.path.join(XBRL_TAXONOMIES_PATH, taxonomy))
PackageManager.rebuildRemappings(controller)
PackageManager.save(controller)

def process_testcase(instance_name, unittest):

    actual_subdir = os.path.join('actual', os.path.basename(instance_name).split(".")[0])
    instance = os.path.join(XBRL_INSTANCES_PATH, instance_name)
    subdir = os.path.join(XBRL_INSTANCES_PATH, actual_subdir)

    # Actual output
    xbrl_instance = ModelXbrl.load(modelManager = modelmanager, url = instance)
    RenderingEvaluator.init(xbrl_instance)

    tables = list(xbrl_instance.modelRenderingTables)
    tables.sort(key = lambda table: table.genLabel(lang = LANGUAGE,strip = True, role = euRCcode))        
    for table in tables:
        obj = src.generateCSV.generateCSVTables(xbrl_instance, 
                                                subdir, 
                                                table = table, 
                                                lang = LANGUAGE,
                                                verbose_labels = False)        
    # Expected output
    expected_subdir = os.path.join('expected', os.path.basename(instance_name).split(".")[0])

    # Comparing files
    files = [f for f in os.listdir(os.path.join(XBRL_INSTANCES_PATH, expected_subdir)) if os.path.isfile(os.path.join(XBRL_INSTANCES_PATH, expected_subdir, f))]
    for file in files:
        with unittest.subTest(file = file):
            if os.path.exists(os.path.join(XBRL_INSTANCES_PATH, actual_subdir, file)):
                with open(os.path.join(XBRL_INSTANCES_PATH, actual_subdir, file), 'rb') as f:
                    actual = f.read()
            else:
                actual = ""
            if os.path.exists(os.path.join(XBRL_INSTANCES_PATH, expected_subdir, file)):
                with open(os.path.join(XBRL_INSTANCES_PATH, expected_subdir, file), 'rb') as f:
                    expected = f.read()
            else:
                expected = ""
            unittest.assertEqual(actual, expected, 'files {0} are different'.format(file))

class TestData_generateCSV(unittest.TestCase):

    def test_taxonomies(self):
        """Test whether taxonomies are available"""
        for taxonomy in taxonomies:
            self.assertTrue(os.path.exists(os.path.join(XBRL_TAXONOMIES_PATH, taxonomy)), 'Taxonomy not available')

    def test_instances(self):
        """Test of instance-data to csv-data"""
        xbrl_files = [f for f in os.listdir(os.path.join(XBRL_INSTANCES_PATH)) if os.path.isfile(os.path.join(XBRL_INSTANCES_PATH, f)) and f[-4:].lower()=='xbrl']
        for xbrl_file in xbrl_files:
            with self.subTest(xbrl_file = xbrl_file):
                process_testcase(xbrl_file, self)
