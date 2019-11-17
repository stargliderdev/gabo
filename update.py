import os
import platform
import sys
import string

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import lib.parameters as params
import lib.dmPostgreSQL as dbmain
import lib.settings as settings
import lib.dataAcess as dataAcces


__version__ = '0.0.1'

def UpdateDB():
    #get db version
    a = "CREATE TABLE public.herois (\
    he_id SERIAL NOT NULL,\
    he_nome VARCHAR(50) NOT NULL,\
    PRIMARY KEY(he_id)\
    ) WITHOUT OIDS;"    
        
