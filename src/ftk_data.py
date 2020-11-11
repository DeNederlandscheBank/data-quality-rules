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
import re

# variables
url = 'https://www.dnb.nl/binaries/'

path_zipfiles = join('.', 'data', 'downloaded files')
extension_taxo = join('.', 'data', 'taxonomies')
path_zipfile_inst = join('.', 'data', 'instances')
path_zipfile_taxo = join('.', 'data', 'taxonomies')

zipfilesets = {'FTK 2.1.0': {'taxonomy': 'FTK Taxonomy 2.1.0_tcm46-386386.zip',
                             'instances': 'FTK Sample Intances 2.1.0_tcm46-386385.zip'},
               'FTK 2.0.0': {'taxonomy': 'FTK Taxonomy 2.0.0_tcm46-385304.zip'},
               'FTK 1.0.3': {'taxonomy': 'FTK Taxonomy 1.0.3_tcm46-380895.zip'},
               'FTK 1.0.2': {'taxonomy': 'FTK Taxonomy 1.0.2_tcm46-378975.zip'},
               'FTK 1.0.1': {'taxonomy': 'FTK Taxonomy 1.0.1_tcm46-378554.zip'},
               'FTK 1.0.0': {'taxonomy': 'FTK Taxonomy 1.0.0_tcm46-377322.zip'},
               'FTK 0.9.0': {'taxonomy': 'FTK Taxonomy 0.9.0_tcm46-374198.zip'}
               }
def main():

    logger = logging.getLogger(__name__)
    logger.info("Platform %s", str(_platform))

    if not os.path.exists(path_zipfile_taxo):
        make_path(path_zipfile_taxo)
    if not os.path.exists(path_zipfile_inst):
        make_path(path_zipfile_inst)

    for zipfileset in zipfilesets.values():

        if 'instances' in zipfileset.keys():
            logger.info("Extracting example instance files from %s", url)
            extract(url, zipfileset['instances'], path_zipfiles)
            logger.info("Moving example instance files to %s", path_zipfile_inst)
            move_files(path_zipfiles, path_zipfile_inst, '\.XBRL')

        if not os.path.isfile(join(path_zipfile_taxo, zipfileset['taxonomy'])):
            if os.path.isfile(join(path_zipfiles, zipfileset['taxonomy'])):
                logger.info('Zip file %s exists, using this one' % str(zipfileset['taxonomy']))
            else:
                logger.info('Zip file %s does not exists, downloading from Internet' % str(zipfileset['taxonomy']))
                r = requests.get(join(url, zipfileset['taxonomy']))
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
def extract(url, name_zipfile, path_zipfile):
    logger = logging.getLogger(__name__)
    if os.path.isfile(join(path_zipfile, name_zipfile)):
        logger.info('Zip file %s exists, using this one' % str(name_zipfile))
        z = ZipfileLongPaths(join(path_zipfile, name_zipfile))
    else:
        logger.info('Zip file %s does not exists, downloading from Internet' % str(name_zipfile))
        r = requests.get(join(url, name_zipfile))
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
def move_files(source, dest1, file_ext = None):
    files = os.listdir(source)
    for f in files:
        if file_ext:
            if not re.search(file_ext,f):
                continue
        if not os.path.exists(join(dest1, f)):
            shutil.move(join(source, f), dest1)
        else:
            os.remove(join(source, f))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
