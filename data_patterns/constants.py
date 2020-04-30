'''Encoding definitions
'''

__author__ = """De Nederlandsche Bank"""
__email__ = 'ECDB_berichten@dnb.nl'
__version__ = '0.1.13'

PATTERN_ID       	   		= "pattern_id"
CLUSTER          	   		= "cluster"
PATTERN_DEF					= "pattern_def"
# P_COLUMNS        	   		= "P columns"
# RELATION_TYPE    	   		= "relation type"
# Q_COLUMNS        	   		= "Q columns"
# P_PART           	   		= "P"
# RELATION         	   		= "relation"
# Q_PART           	   		= "Q"
SUPPORT          	   		= "support"
EXCEPTIONS       	   		= "exceptions"
CONFIDENCE       	   		= "confidence"
PATTERN_STATUS   	   		= "pattern status"
ENCODINGS        	   		= "encodings"
PANDAS_CO					= "pandas co"
PANDAS_EX					= "pandas ex"
XBRL_CO						= "xbrl co"
XBRL_EX						= "xbrl ex"

RESULT_TYPE      	   		= 'result_type'
INDEX            	   		= "index"
P_VALUES         	   		= "P values"
Q_VALUES         	   		= "Q values"

ENCODE            	   		= "encode"

INITIAL_PATTERN_STATUS 		= 'not defined'
TEXT_CONFIRMATION	   		= 'confirmation'
TEXT_EXCEPTION		   		= 'exception'

DEFAULT_SHEET_NAME_PATTERNS = 'Patterns'
SHEET_NAME_POST_CO     		= "_co"
SHEET_NAME_POST_EX     		= "_ex"

PATTERNS_COLUMNS 	   		= [PATTERN_ID, CLUSTER, 
					  		   PATTERN_DEF, 
                    	  	   SUPPORT, EXCEPTIONS, CONFIDENCE, PATTERN_STATUS, ENCODINGS, PANDAS_CO, PANDAS_EX, XBRL_CO, XBRL_EX]
     
RESULTS_COLUMNS        		= [RESULT_TYPE, PATTERN_ID, CLUSTER, INDEX, SUPPORT, EXCEPTIONS, CONFIDENCE, 
                    	  	   PATTERN_DEF, 
                    	  	   P_VALUES, Q_VALUES]
