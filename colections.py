#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QTreeWidget, QTreeWidgetItem, QToolButton, QTableWidget

import ex_grid
import qlib as qc
# import sqlite_crud
import parameters as gl
import sqlite_crud
import stdio


class CollectionBrowser(QDialog):
    def __init__(self,  parent = None):
        super(CollectionBrowser, self).__init__(parent)
        self.resize(600, 400)
        self.toto = ''
        self.setWindowTitle('Colecções')
        self.setWindowIcon(QIcon('./img/collections.png'))
        masterLayout = QVBoxLayout(self)
        self.searchEdit= QLineEdit()
        self.searchEdit.textChanged.connect(self.text_search_changed)
        searchClearBtn = QToolButton()                                           
        searchClearBtn.setToolTip('Limpa Pesquisa')                              
        searchClearBtn.setIcon(QIcon('./img/clear.png'))                         
        searchClearBtn.clicked.connect(self.search_clear_click)                  
        # self.collectionList = QTreeWidget()
        # self.collectionList.setColumnWidth(0, 200)
        self.collectionGrid = QTableWidget()
        self.collectionGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.collectionGrid.setSelectionMode(QTableWidget.SingleSelection)

        self.collectionGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.collectionGrid.verticalHeader().setDefaultSectionSize(20)
        self.collectionGrid.verticalHeader().setVisible(False)
        self.collectionGrid.setAlternatingRowColors(True)
        self.collectionGrid.setStyleSheet("alternate-background-color: #F5F4F2")
        self.collectionGrid.itemDoubleClicked.connect(self.validate_click)
        masterLayout.addWidget(self.collectionGrid)
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)

        validateBtn = QPushButton('Valida')
        validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        masterLayout.addLayout(qc.addHLayout([validateBtn,renameBtn,exitBtn]))
        masterLayout.addLayout(qc.addHLayout([self.searchEdit, searchClearBtn]))
        masterLayout.addWidget(self.collectionGrid)
        self.grid_refresh()

    def search_clear_click(self):
        self.grid_refresh()

    def grid_refresh(self):
        sql = '''select  0 , collection_name from collections where collection_name is not null  order by collection_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.collectionGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        self.collectionGrid.setColumnWidth(0, 0)
        self.collectionGrid.setColumnWidth(1, 500)

    def text_search_changed(self, text):
        search = '\'%' + text.lower() + '%\''
        sql = '''select 0, collection_name
            from collections
            where (lower(collection_name)) like ''' + search + '''
            order by collection_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.collectionGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        self.collectionGrid.setColumnWidth(0, 0)
        self.collectionGrid.setColumnWidth(1, 500)

    def rename_click(self):
        try:
            dum = self.collectionGrid.item(self.collectionGrid.currentRow(), 1).text()
            text, flag = QInputDialog.getText(None, "Altera nome da Colecção:", dum + ' para :', QLineEdit.Normal)
            if flag: # and not text == '':
                sqlite_crud.execute_query("delete from collections WHERE collection_name =?;", (dum,))
                sqlite_crud.execute_query("UPDATE books set pu_collection=? WHERE pu_collection=?;", (text, dum))
                self.grid_refresh()
        except AttributeError:
            pass

    def validate_click(self):
        try:
            self.toto = self.collectionGrid.item(self.collectionGrid.currentRow(), 1).text()
            # gl.AUTHOR_SEARCH_MASK = self.searchEdit.text()
            self.close()
        except AttributeError:
            pass
        self.close()
    
    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()
