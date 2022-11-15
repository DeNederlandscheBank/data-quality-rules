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
from sys import platform as _platform

# variables
make_folder = True

zipfilesets = {
               'Nationale Staten 1.1.0':
                    {'url_taxo': 'https://www.dnb.nl/media/fivpjdpj/',
                     'taxonomy': 'vns_taxonomy_1-1-0.zip',
                     'url_inst': 'https://www.dnb.nl/media/o10oswji/',
                     'instances': 'vns_sample_instances_1-1-0.zip',
                     'extension': ''},
               'Solvency2 2.6.0':
                    {'url_taxo': 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.6.0/S2/',
                     'taxonomy': 'EIOPA_SolvencyII_XBRL_Taxonomy_2.6.0_hotfix_with_External_Files.zip',
                     'url_inst': 'https://dev.eiopa.europa.eu/Taxonomy/Full/2.6.0/S2/',
                     'instances': 'EIOPA_SolvencyII_XBRL_Instance_documents_2.6.0.zip',
                     'extension': join('EIOPA_SolvencyII_XBRL_Instance_documents_2.6.0', 'random')},
               'Solvency2 2.5.0': 
                    {'url_taxo':  'https://dev.eiopa.europa.eu/Taxonomy/Full/2.5.0/S2/',
                     'taxonomy' : 'EIOPA_SolvencyII_XBRL_Taxonomy_2.5.0_hotfix_with_External_Files.zip',
                     'url_inst':  'https://dev.eiopa.europa.eu/Taxonomy/Full/2.5.0/S2/',
                     'instances': 'EIOPA_SolvencyII_XBRL_Instance_documents_2.5.0.zip',
                     'extension': join('EIOPA_SolvencyII_XBRL_Instance_documents_2.5.0', 'random')},
               'Solvency2 2.4.0': 
                    {'url_taxo':  'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/',
                     'taxonomy':  'EIOPA_SolvencyII_XBRL_Taxonomy_2.4.0_with_external_hotfix.zip',
                     'url_inst':  'https://dev.eiopa.europa.eu/Taxonomy/Full/2.4.0/S2/',
                     'instances': 'EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0.zip',
                     'extension': join('EIOPA_SolvencyII_XBRL_Instance_documents_2.4.0', 'random')},
               'Solvency2 2.3.0':
                    {'url_taxo':  'https://dev.eiopa.europa.eu/Taxonomy/Full/2.3.0/S2/',
                      'taxonomy': 'EIOPA_SolvencyII_XBRL_Taxonomy_2.3.0_Hotfix.zip'}
               }
                    
path_zipfiles = join('.', 'data', 'downloaded files')
path_zipfile_inst = join('.', 'data', 'instances')
path_zipfile_taxo = join('.', 'data', 'taxonomies')

@click.command()

def main():

    logger = logging.getLogger(__name__)
    logger.info("Platform %s", str(_platform))

    if not os.path.exists(path_zipfile_taxo):
        make_path(path_zipfile_taxo)
    if not os.path.exists(path_zipfile_inst):
        make_path(path_zipfile_inst)

    for zipfileset in zipfilesets.values():

        if 'instances' in zipfileset.keys():
            logger.info("Extracting example instance files from %s", zipfileset['url_inst'])
            extract(zipfileset['url_inst'], zipfileset['instances'], path_zipfiles)
            logger.info("Moving example instance files to %s", path_zipfile_inst)
            move_files(join(path_zipfiles, zipfileset['extension']), path_zipfile_inst)
            logger.info("Cleaning up files in %s", path_zipfiles)
            try:
                shutil.rmtree(winapi_path(join(path_zipfiles, zipfileset['instances'][:-4])))
            except:
                logger.warning(".. files in %s not deleted", path_zipfiles)

        if not os.path.isfile(join(path_zipfile_taxo, zipfileset['taxonomy'])):
            if os.path.isfile(join(path_zipfiles, zipfileset['taxonomy'])):
                logger.info('Zip file %s exists, using this one' % str(zipfileset['taxonomy']))
            else:
                logger.info('Zip file %s does not exists, downloading from Internet' % str(zipfileset['taxonomy']))
                r = requests.get(join(zipfileset['url_taxo'], zipfileset['taxonomy']))
                output = open(join(path_zipfiles, zipfileset['taxonomy']), "wb")
                output.write(r.content)
                output.close()
            logger.info("Moving taxonomy to %s", path_zipfile_taxo)
            shutil.copy(join(path_zipfiles, zipfileset['taxonomy']), path_zipfile_taxo)
        else:
            logger.info("taxonomy already exists")

    logger.info("Thank you for waiting!")

# Needed for long paths
class ZipfileLongPaths(zipfile.ZipFile):
    def _extract_member(self, member, targetpath, pwd):
        targetpath = winapi_path(targetpath)
        return zipfile.ZipFile._extract_member(self, member, targetpath, pwd)

# Needed for long paths
def winapi_path(dos_path, encoding=None):
    if (_platform == 'win32') or (_platform == 'win64'):
        path = os.path.abspath(dos_path)
        if path.startswith("\\\\"):
            path = "\\\\?\\UNC\\" + path[2:]
        else:
            path = "\\\\?\\" + path
        return path
    else:
        return dos_path

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
        r = requests.get(join(url_inst, name_zipfile))
        output = open(join(path_zipfile, name_zipfile), "wb")
        output.write(r.content)
        output.close()
        z = ZipfileLongPaths(io.BytesIO(r.content))
    for file in tqdm(iterable=z.namelist(), total=len(z.namelist())):
        if ('ars' in file.lower()) or \
           ('qrs' in file.lower()) or \
           ('arg' in file.lower()) or \
           ('qrg' in file.lower()) or \
           ('qfs' in file.lower()) or \
           ('qfg' in file.lower()):
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
