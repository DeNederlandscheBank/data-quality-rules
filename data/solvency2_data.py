# THIS SCRIPT MIGHT TAKE A WHILE

import zipfile
import os
from os.path import join
from datetime import datetime, timedelta
from urllib.request import urlopen
import requests
import io
import shutil
from pathlib import Path
from tqdm import tqdm

# variables
url = 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/'
path_zipfile = r'taxonomy\arelle\cache\http'
name_zipfile = 'EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_with_external_hotfix.zip'
url_inst = 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/'
path_zipfile_inst = r'taxonomy\examples'
name_zipfile_inst = 'EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0.zip'

#
# Make paths
if not os.path.exists(path_zipfile):
   print("path doesn't exist. trying to make")
   os.makedirs(path_zipfile)

if not os.path.exists(path_zipfile_inst):
   print("path doesn't exist. trying to make")
   os.makedirs(path_zipfile_inst)



# Delete content if there is content
shutil.rmtree(path_zipfile)
shutil.rmtree(path_zipfile_inst)




# Extract files
r = requests.get(url_inst + name_zipfile_inst)
z = zipfile.ZipFile(io.BytesIO(r.content))
for file in tqdm(iterable=z.namelist(), total=len(z.namelist())):
    try:
        z.extract(member=file, path=path_zipfile_inst)
    except:
        print('\nCannot extract: ' + str(file))

z.close()


r = requests.get(url + name_zipfile)
z = zipfile.ZipFile(io.BytesIO(r.content))
for file in tqdm(iterable=z.namelist(), total=len(z.namelist())):
    try:
        z.extract(member=file, path=path_zipfile)
    except:
        print('\nCannot extract: ' + str(file))

z.close()

# Move files examples
source = path_zipfile_inst + r'\EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0\random'
dest1 = path_zipfile_inst
files = os.listdir(source)
for f in files:
    shutil.move(join(source,f), dest1)

# Move files taxonomy
source = path_zipfile + r'\EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_Hotfix_with_external'
dest1 = path_zipfile
files = os.listdir(source)
for f in files:
    shutil.move(join(source,f), dest1)

print("\nThank you for waiting!")
