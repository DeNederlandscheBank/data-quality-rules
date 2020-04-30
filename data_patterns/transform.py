'''Dataframe definitions
'''

#imports
import pandas as pd
import numpy as np
import xlsxwriter
import ast
from .constants import *
from .constants import *

__author__ = """De Nederlandsche Bank"""
__email__ = 'ECDB_berichten@dnb.nl'
__version__ = '0.1.13'

class PatternDataFrame(pd.DataFrame):
    ''' 
    A PatternDataframe is a subclass of a Pandas DataFrame for patterns with 
    a specialized to_excel function to get a readable format

    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------

    See Also
    --------

    Notes
    -----

    '''

    def to_excel(self, filename, *args, **kwargs):
        writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
        sheet_name = kwargs.pop('sheet_name', DEFAULT_SHEET_NAME_PATTERNS)
        font = writer.book.add_format({'font_name': 'Arial', 
                                       'font_size': 10, 
                                       'valign'   : 'top', 
                                       'align'    : 'left', 
                                       'text_wrap': True})
        if not self.empty:
            df = super(PatternDataFrame, self).copy()
            # make sure that the '='-sign is read properly by Excel
            #df[RELATION_TYPE] = "'" + df[RELATION_TYPE]
            df.to_excel(writer, 
                        sheet_name = sheet_name, 
                        merge_cells = False, *args, **kwargs)
        else:
            print("Empty patterns dataframe. No patterns to export.")
        for name in writer.sheets:
            worksheet = writer.sheets[name]
            worksheet.set_column('A:O', None, font)
            worksheet.set_default_row(60)
            worksheet.set_column(1, 1, 20)
            worksheet.set_column(2, 2, 5)
            worksheet.set_column(3, 3, 40)
            worksheet.set_column(4, 4, 5)
            worksheet.set_column(5, 5, 40)
            worksheet.set_column(6, 6, 40)
            worksheet.set_column(7, 7, 5)
            worksheet.set_column(8, 8, 40)
            worksheet.set_column(9, 9, 13)
            worksheet.set_column(10, 10, 13)
            worksheet.set_column(11, 11, 13)
            worksheet.set_column(12, 12, 13)
            worksheet.set_column(13, 13, 25)
            worksheet.set_column(14, 14, 25)
        writer.save()
        writer.close()
        return None

class ResultDataFrame(pd.DataFrame):
    ''' 
    A ResultDataframe is a subclass of a Pandas DataFrame for patterns results with 
    a specialized to_excel function to get a readable format

    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------

    See Also
    --------

    Notes
    -----

    '''

    def to_excel(self, filename, *args, **kwargs):
        writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
        font = writer.book.add_format({'font_name': 'Arial', 
                                       'font_size': 10, 
                                       'valign'   : 'top', 
                                       'align'    : 'left', 
                                       'text_wrap': True})
        if not self.empty:
            for pattern_id in self[PATTERN_ID].unique().sort():
                co = self[(self[PATTERN_ID]==pattern_id) & (self[RESULT_TYPE])]
                co = co.drop([PATTERN_ID, RESULT_TYPE], axis = 1)
                ex = self[(self[PATTERN_ID]==pattern_id) & (~self[RESULT_TYPE])]
                ex = ex.drop([PATTERN_ID, RESULT_TYPE], axis = 1)
                if not co.empty:
                    co.to_excel(writer, sheet_name = pattern_id + SHEET_NAME_POST_CO, merge_cells = False)
                if not ex.empty:
                    ex.to_excel(writer, sheet_name = pattern_id + SHEET_NAME_POST_EX, merge_cells = False)
        for name in writer.sheets:
            worksheet = writer.sheets[name]
            worksheet.set_column('A:O', None, font)
            worksheet.set_default_row(60)
            levels = self.index.nlevels
            for n in range(0, levels):
                worksheet.set_column(n, n, 20, font)
            worksheet.set_column(levels-1, levels-1, 5)
            worksheet.set_column(levels, levels, 7)
            worksheet.set_column(levels+1, levels+1, 7)
            worksheet.set_column(levels+2, levels+2, 7)
            worksheet.set_column(levels+3, levels+3, 7)
            worksheet.set_column(levels+4, levels+4, 40)
            worksheet.set_column(levels+5, levels+5, 10)
            worksheet.set_column(levels+6, levels+6, 40)
            worksheet.set_column(levels+7, levels+7, 40)
            worksheet.set_column(levels+8, levels+8, 10)
            worksheet.set_column(levels+9, levels+9, 40)
            worksheet.set_column(levels+10, levels+10, 40)
            worksheet.set_column(levels+11, levels+11, 10)
            worksheet.set_column(levels+12, levels+12, 40)
        writer.save()
        writer.close()
        return None
