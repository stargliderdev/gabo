#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QTreeWidget, QTreeWidgetItem, QToolButton, QTableWidget

import ex_grid
import qlib as qc
import sqlite_crud
import parameters as gl
import stdio


class PublishersBrowser(QDialog):
    def __init__(self,  parent = None):
        super(PublishersBrowser, self).__init__(parent)
        self.resize(600, 400)
        self.toto = ''
        self.setWindowTitle('Editores(as)')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        # self.publishersList = QTreeWidget()
        # self.publishersList.setColumnWidth(0, 200)
        self.searchEdt = QLineEdit()
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)

        deleteBtn = QPushButton('Apaga')
        deleteBtn.clicked.connect(self.delete_click)
        # validateBtn = QPushButton('Valida')
        # validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        self.searchEdit= QLineEdit()
        self.searchEdit.textChanged.connect(self.text_search_changed)
        searchClearBtn = QToolButton()
        searchClearBtn.setToolTip('Limpa Pesquisa')
        searchClearBtn.setIcon(QIcon('./img/clear.png'))
        # searchClearBtn.clicked.connect(self.search_clear_click)
        # self.collectionList = QTreeWidget()
        # self.collectionList.setColumnWidth(0, 200)
        self.publishersGrid = QTableWidget()
        self.publishersGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.publishersGrid.setSelectionMode(QTableWidget.SingleSelection)

        self.publishersGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.publishersGrid.verticalHeader().setDefaultSectionSize(20)
        self.publishersGrid.verticalHeader().setVisible(False)
        self.publishersGrid.setAlternatingRowColors(True)
        self.publishersGrid.setStyleSheet("alternate-background-color: #99ffcc;")
        self.publishersGrid.itemDoubleClicked.connect(self.validate_click)

        masterLayout.addLayout(qc.addHLayout([renameBtn, deleteBtn, exitBtn]))
        masterLayout.addLayout(qc.addHLayout(['Pesquisa:', self.searchEdit, searchClearBtn]))
        masterLayout.addWidget(self.publishersGrid)
        # masterLayout.addWidget(self.publishersList)
        # self.update_combo()
        self.grid_refresh()

    # def update_combo(self):
    #     sqlite_crud.get_publishers()
    #     self.publishersList.clear()
    #     self.publishersList.setHeaderLabels(["Editor(a)"])
    #     items = []
    #     for n in gl.publishers_tuple:
    #         item = QTreeWidgetItem([n[0]])
    #         items.append(item)
    #     self.publishersList.insertTopLevelItems(0, items)

    def text_search_changed(self, text):
        search = '\'%' + text.lower() + '%\''
        sql = '''select 0, publisher_name
            from publishers
            where (lower(publisher_name)) like ''' + search + '''
            order by publisher_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.publishersGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        self.publishersGrid.setColumnWidth(0, 0)
        self.publishersGrid.setColumnWidth(1, 500)


    def grid_refresh(self):
        sql = '''select  0 , publisher_name from publishers where publisher_name is not null  order by publisher_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.publishersGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        self.publishersGrid.setColumnWidth(0, 0)
        self.publishersGrid.setColumnWidth(1, 500)

    def rename_click(self):
        try:
            dum = self.publishersGrid.item(self.publishersGrid.currentRow(), 1).text()
            text, flag = QInputDialog.getText(None, "Altera nome da Editora:", dum + ' para :', QLineEdit.Normal, dum)
            if flag and not text == '': # and not text == '':
                sqlite_crud.execute_query("delete from publishers WHERE publisher_name =?;", (dum,))
                sqlite_crud.execute_query("UPDATE books set pu_publisher=? WHERE pu_publisher=?;", (text, dum))
                self.grid_refresh()

        except AttributeError:
            pass

    def validate_click(self):
        self.toto = self.publishersGrid.item(self.publishersGrid.currentRow(), 1).text()
        self.close()

    def delete_click(self):
        try:
            dum = self.publishersGrid.item(self.publishersGrid.currentRow(), 1).text()
            sqlite_crud.execute_query('delete from publishers where publisher_name=?', (dum, ))
            sqlite_crud.execute_query('update books set  pu_publisher=\'\' where pu_publisher=?', (dum, ))
            self.grid_refresh()
        except AttributeError:
            pass

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()
