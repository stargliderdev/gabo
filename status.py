#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform
import sys
import datetime
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import parse_html
import parameters as params

__version__ = '0.0.1'

class StatusDialog(QDialog):
    def __init__(self,  parent = None):
        super(StatusDialog,  self).__init__(parent)
        
        self.siteDic ={'Wook':'http://www.wook.pt/product/facets?palavras='} #, 'Bertrand':'http://www.bertrand.pt/?palavra='}
        self.siteList = []
        for key in self.siteDic:
            self.siteList.append(key)

        editSize = 28
        self.list = []
        self.setObjectName('Edita')
        self.resize(800, 600)
        self.setWindowTitle('Procura por ISBN')
        mainLayout = QVBoxLayout(self)
        
       
        displayLayout = QHBoxLayout()
        displayLayout.setSpacing(0)
        
        
        self.outputPlainText = QPlainTextEdit()
        palette = QPalette()
        brush = QBrush(QColor(0, 192, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(0, 192, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(165, 164, 164))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(244, 244, 244))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        font = QFont()
        font.setFamily("Monospace")
        font.setWeight(75)
        font.setBold(True)
        self.outputPlainText.setPalette(palette)
        self.outputPlainText.setFont(font)
        
        
        self.outputPlainText.setUpdatesEnabled(True)
        buttonLayout = QHBoxLayout()    
        self.CancelButton = QPushButton('Fechar')      
        self.OkButton = QPushButton('Cria Ficha')
        self.OkButton.setEnabled(False)
        self.wookBtn = QPushButton('Pesquisa no Wook')
        
       
        buttonLayout.addWidget(self.OkButton)
        buttonLayout.addWidget(self.wookBtn)
        buttonLayout.addWidget(self.CancelButton)
        
        
        mainLayout.addLayout(displayLayout)
        mainLayout.addWidget(self.outputPlainText)
        mainLayout.addLayout(buttonLayout)
        
        # init display
        self.PRINT('Pesquisa por pelo ISBN: '+ params.ISBN)
    
        self.connect(self.wookBtn, SIGNAL("clicked()"), self.getBookDataISBN)
        self.connect(self.OkButton,  SIGNAL("clicked()"), self.exitAndCreateFile)
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.exit)
        #self.getBookDataISBN()
        
    def PRINT(self, text):
        self.outputPlainText.appendPlainText(str(text.decode('utf-8')))

    def getBookDataISBN(self):    
        siteToSearch = 'Wook'
        stringToSearch=params.ISBN
        dumLink= self.siteDic[str(siteToSearch)] + stringToSearch 
        url = dumLink

        try:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            the_page = response.read() 
            #print the_page 
            self.findBookPage(the_page, 'search_produto_imagem')
            #for key in params.bookDataDic:
            self.PRINT(str('Titulo') + ': '  + params.bookDataDic['pu_title'])
            self.PRINT(str(' Autor') + ': '  + params.bookDataDic['pu_author'])
            self.PRINT(str('Editor') + ': '  + params.bookDataDic['pu_editor'])
            self.OkButton.setEnabled(True)
                
        except Exception as detail: 
            print("Error in getBookDataISBN", detail)
        

    def findBookPage(self, page_source, token):
        ## valido só para a wook
        # retira o link da ficha directa to livro
        token_pointer = page_source.find('search_produto_imagem')
        foo =  page_source[token_pointer:]
        dum = foo.find('\'>')
        link_ = foo[foo.find('\''):dum]
        link = 'http://www.wook.pt'+link_[1:]
        print('wook link:', link)
        parse_html.parseWook(link) # faz o parse da pagina em HTML

    def exit(self):
        self.close()
        
    def exitAndCreateFile(self):
        params.newRecord = True
        self.close()
def main():
    params.ISBN = '9789896164461'
    app = QApplication(sys.argv)
    form = StatusDialog()   
    form.show()
    app.exec_()


if __name__ == '__main__':


    main()
