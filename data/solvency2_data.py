# -*- coding: utf-8 -*-

# THIS SCRIPT MIGHT TAKE A WHILE
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import zipfile
import os
from os.path import isfile, join, exists
from datetime import datetime, timedelta
from urllib.request import urlopen
import requests
import io
import shutil
from pathlib import Path
from tqdm import tqdm

# variables
make_folder = True

url_taxo = 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/'
url_inst = 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/'

path_zipfiles = join('downloaded files')

name_zipfile_taxo = 'EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_with_external_hotfix.zip'
path_zipfile_taxo = join('taxonomy', 'arelle', 'cache', 'http')
path_zipfile_taxo_2 = join('taxonomy', 'arelle', 'cache', 'https')
extension_taxo = join('EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_Hotfix_with_external')

name_zipfile_inst = 'EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0.zip'
path_zipfile_inst = join('.', 'instances')
extension_inst =  join('EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0', 'random')

@click.command()
@click.option('--delete_old_files', prompt = "Delete old files? (Y/N)", default='Y', help='Delete files in existing taxonomy directory')

def main(delete_old_files):
    logger = logging.getLogger(__name__)

    # Delete content if there is content
    if delete_old_files == 'Y':
        if os.path.exists(path_zipfile_taxo):
            logger.info("Deleting files in %s (this might take a while)", path_zipfile_taxo)
            shutil.rmtree(winapi_path(path_zipfile_taxo))
        if os.path.exists(path_zipfile_inst):
            logger.info("Deleting files in %s", path_zipfile_inst)
            shutil.rmtree(path_zipfile_inst)

    if not os.path.exists(path_zipfile_taxo):
        make_path(path_zipfile_taxo)
    if not os.path.exists(path_zipfile_inst):
        make_path(path_zipfile_inst)

    logger.info("Extracting example instance files from %s", url_inst)
    extract(url_inst, name_zipfile_inst, path_zipfiles)

    logger.info("Moving example instance files to %s", path_zipfile_inst)
    move_files(join(path_zipfiles, extension_inst), path_zipfile_inst)

    logger.info("Extracting taxonomy from %s", url_taxo)
    extract(url_taxo, name_zipfile_taxo, path_zipfiles)

    logger.info("Moving taxonomy files to %s", path_zipfile_taxo)
    move_files(join(path_zipfiles, extension_taxo), path_zipfile_taxo)

    # correct eiopa deactivations error
    shutil.copytree(join(path_zipfile_taxo, 'dev.eiopa.europa.eu'), join(path_zipfile_taxo_2, 'dev.eiopa.europa.eu'))

    logger.info("Cleaning up files in %s", path_zipfiles)
    shutil.rmtree(winapi_path(join(path_zipfiles, 'EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_Hotfix_with_external')))
    shutil.rmtree(winapi_path(join(path_zipfiles, 'EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0')))

    logger.info("Thank you for waiting!")

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
    logger = logging.getLogger(__name__)
    if not os.path.exists(path_zipfile):
        logger.info('Making directory %s' % path_zipfile)
        os.makedirs(path_zipfile)

# Extract files
def extract(url_inst, name_zipfile, path_zipfile):
    logger = logging.getLogger(__name__)
    if os.path.isfile(join(path_zipfile, name_zipfile)):
        logger.info('Zip file %s exists, using this one' % str(name_zipfile))
        z = ZipfileLongPaths(join(path_zipfile, name_zipfile))
    else:
        logger.info('Zip file %s does not exists, downloading from Internet' % str(name_zipfile))
        r = requests.get(url_inst + name_zipfile)
        output = open(join(path_zipfile, name_zipfile), "wb")
        output.write(r.content)
        output.close()
        z = ZipfileLongPaths(io.BytesIO(r.content))
    for file in tqdm(iterable=z.namelist(), total=len(z.namelist())):
        try:
            z.extract(member=file, path=path_zipfile)
        except:
            logger.info('Cannot extract %s' % str(file))
    z.close()

# Move files examples
def move_files(source, dest1):
    files = os.listdir(source)
    for f in files:
        if not os.path.exists(join(dest1, f)):
            shutil.move(join(source, f), dest1)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
