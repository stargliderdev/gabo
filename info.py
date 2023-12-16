#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform
import sys
import string
import time

#import HTML
from PyQt5.QtWidgets import QTabWidget,QDesktopWidget, QLabel, QCheckBox, QVBoxLayout, QLineEdit, QComboBox,QTableWidget, \
    QWidget,QMainWindow,QApplication,QMessageBox, QStyleFactory, QToolButton, QAction, QStatusBar, QInputDialog, QDialog

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import Qt


import parameters as param


__version__ = '0.0.2'


class SystemInfo(QDialog):
    def __init__(self,  parent = None):
        super(SystemInfo,  self).__init__(parent)

        self.resize(800, 600)
        self.textOutputHtml=[]
        
        self.setWindowTitle('Informações')
        mainLayout = QVBoxLayout(self)
        self.buttonsLayout = QHBoxLayout()
        
        self.outputPlainText = QTextEdit()
        self.outputPlainText.setReadOnly(True) 
        self.outputPlainText.setObjectName('pu_obs')
        mainLayout.addWidget(self.outputPlainText)
                
        #mainLayout.addLayout(self.buttonsLayout)
        
        self.PRINT(self.sistemInfo())

        self.PRINT(self.databaseInfo())
        self.PRINT(self.databaseCountInfo())
    
    def sistemInfo(self):
        self.textToDisplay = []

        where = os.getcwd()
        #what = os.uname()
        used = os.times()
        now = time.time()
        means = time.ctime(now)
        if not sys.platform == 'win32':
            self.textToDisplay.append(("Sistema Operativo: " ,  'Linux'))            
            unumber = os.getuid()
            pnumber = os.getpid()
            what = os.uname()
            self.textToDisplay.append(("User number: " , str(unumber)))
            self.textToDisplay.append(("Process ID: " ,  str(pnumber)))
            self.textToDisplay.append(('Kernel:',  str(what[2])))
            self.textToDisplay.append(('ARCH:',  str(what[4])))
            self.textToDisplay.append(('Local Host:', str(what[1])))        
        else:
            self.textToDisplay.append(("Sistema Operativo: " ,  'Windows'))

        self.textToDisplay.append(("Current Directory: " ,  str(where)))
        
        
        self.textToDisplay.append(("Carga: " ,  str(used[0])))
        
        self.textToDisplay.append(("Time is now:" ,  str(means)))
        self.textToDisplay.append(('PyQt4 version: ' ,   PYQT_VERSION_STR))
        self.textToDisplay.append(('PYQT VERSION: ' ,  str(PYQT_VERSION)))
        self.textToDisplay.append(('Python: ' ,  str(sys.version_info[0])+ '.' +str(sys.version_info[1]) + '.' +str(sys.version_info[2]) + '\n'))
        import psycopg2
        self.textToDisplay.append(('psycopg2:' ,  str(psycopg2.__version__)))
        
        return self.textToDisplay    
    
    def databaseInfo(self):
        self.textToDisplay = []
        self.textToDisplay.append(('Server:' ,  param.db_host ))        
        self.textToDisplay.append(('database:' ,  param.db_database ))
        return self.textToDisplay    

    def databaseCountInfo(self):
        self.textToDisplay = []
        tables = [["livros", 'pu_id'], ['authors', 'au_id'], ['collection', 'col_id'], ['publishers', 'pb_id'], ['assuntos', 'as_id']]

        for g in tables:
            data = (g[1],)
            a = dbmain.OutputQueryOne('select count(?) as soma from  ' +  g[0] ,data)
            dum = "{0:10d}".format(a.output[0])
            self.textToDisplay.append(('Tabela ',   "{0:<15}".format(g[0])+ dum ))

        return self.textToDisplay
    
    def PRINT(self, text):
        for n in text:
            self.outputPlainText.append(n[0]+n[1])
        
def main():

    app = QApplication(sys.argv)
    form = SystemInfo()
    form.show()
    app.exec_()

if __name__ == '__main__':
    pass
    # settings.load_settings()
    # main()
