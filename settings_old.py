#!/usr/bin/python
# -*- coding: utf-8 -*-

from configobj import ConfigObj
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import parameters as param
import sys

def load_settings():
    try:
        config = ConfigObj('livros.config')
        param.db_host = config['db_host']
        param.db_database = config['db_database']
        param.db_user = config['db_user']
        param.db_password = config['db_password']
        dum = config['windowSize']
        param.windowSize = (int(dum[0]), int(dum[1]))
        dum = config['windowPos']
        param.windowPos = (int(dum[0]), int(dum[1]))
        param.backup_dir = config['backup_dir']
        return True
    except Exception as e:


        print('Erro ao carregar settings',  e)
        return False

def save_init_settings():
    config = ConfigObj()
    config.filename = '../etc/livros.config'
    config['db_host'] = '192.168.0.102'
    config['db_database'] ='livros'
    config['db_user'] = 'sysdba'
    config['db_password'] = 'masterkey'
    config.write()

def save_settings():
    config = ConfigObj()
    config.filename = '../etc/livros.config'
    config['db_host'] = param.path_artigos
    config['db_file'] = param.path_familias
    config.write()


def load_settings():
    import configparser

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Specify the path to your INI configuration file
    file_path = "config.ini"

    # Read the INI file
    config.read(file_path)

    # Access values from the configuration
    value1 = config.get("Section1", "key1")
    value2 = config.get("Section1", "key2")
    value3 = config.get("Section2", "key3")

    # Print the values
    print("Value 1:", value1)
    print("Value 2:", value2)
    print("Value 3:", value3)

if __name__ == "__main__": 
    save_init_settings()
