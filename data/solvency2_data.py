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
make_folder = True
delete_old_folder = False
url = 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/'
path_zipfile = r'taxonomy\arelle\cache\http'
name_zipfile = 'EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_with_external_hotfix.zip'
url_inst = 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/'
path_zipfile_inst = r'taxonomy\examples'
name_zipfile_inst = 'EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0.zip'
extention_inst =  r'\EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0\random'
extention = r'\EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_Hotfix_with_external'


# Needed for long paths
class ZipfileLongPaths(zipfile.ZipFile):

    def _extract_member(self, member, targetpath, pwd):
        targetpath = winapi_path(targetpath)
        return zipfile.ZipFile._extract_member(self, member, targetpath, pwd)

# Needed for long paths
def winapi_path(dos_path, encoding=None):
    path = os.path.abspath(dos_path)

    if path.startswith("\\\\"):
        path = "\\\\?\\UNC\\" + path[2:]
    else:
        path = "\\\\?\\" + path

    return path


def make_path(path_zipfile):
    if not os.path.exists(path_zipfile):
       print("path doesn't exist. trying to make")
       os.makedirs(path_zipfile)





# Extract files
def extract(url_inst, name_zipfile_inst, path_zipfile_inst):
    if os.path.isfile(join(path_zipfile_inst, name_zipfile_inst)):
        z = ZipfileLongPaths(join(path_zipfile_inst, name_zipfile_inst))
    else:
        r = requests.get(url_inst + name_zipfile_inst)
        z = ZipfileLongPaths(io.BytesIO(r.content))
    for file in tqdm(iterable=z.namelist(), total=len(z.namelist())):
        try:
            z.extract(member=file, path=path_zipfile_inst)
        except:
            print('\nCannot extract: ' + str(file))

    z.close()


# Move files examples
def move_files(source, dest1):
    files = os.listdir(source)
    for f in files:
        shutil.move(join(source,f), dest1)



def main():
    if make_folder:
        make_path(path_zipfile)
        make_path(path_zipfile_inst)

    # Delete content if there is content
    if delete_old_folder:
        shutil.rmtree(winapi_path(path_zipfile))
        shutil.rmtree(path_zipfile_inst)

    extract(url_inst, name_zipfile_inst, path_zipfile_inst)
    extract(url, name_zipfile, path_zipfile)

    move_files(path_zipfile_inst + extention_inst, path_zipfile_inst)
    move_files(path_zipfile + extention, path_zipfile)

    print("\nThank you for waiting!")

main()
