#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QTreeWidget, QTreeWidgetItem, QToolButton, QTableWidget

import ex_grid
import qlib as qc
import sqlite_crud
import parameters as gl

class SeriesBrowser(QDialog):
    def __init__(self,  parent = None):
        super(SeriesBrowser, self).__init__(parent)
        self.resize(600, 400)
        self.toto = ''
        self.setWindowTitle('Séries')
        self.setWindowIcon(QIcon('./img/series.png'))
        masterLayout = QVBoxLayout(self)
        self.searchEdit = QLineEdit()
        self.searchEdit.textChanged.connect(self.text_search_changed)
        searchClearBtn = QToolButton()
        searchClearBtn.setToolTip('Limpa Pesquisa')
        searchClearBtn.setIcon(QIcon('./img/clear.png'))
        searchClearBtn.clicked.connect(self.search_clear_click)
        self.seriesGrid = QTableWidget()
        self.seriesGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.seriesGrid.setSelectionMode(QTableWidget.SingleSelection)

        self.seriesGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.seriesGrid.verticalHeader().setDefaultSectionSize(20)
        self.seriesGrid.verticalHeader().setVisible(False)
        self.seriesGrid.setAlternatingRowColors(True)
        self.seriesGrid.setStyleSheet("alternate-background-color: #F5F4F2;")
        self.seriesGrid.itemDoubleClicked.connect(self.validate_click)
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)

        validateBtn = QPushButton('Valida')
        validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        masterLayout.addLayout(qc.addHLayout([validateBtn,renameBtn,exitBtn]))
        masterLayout.addLayout(qc.addHLayout([self.searchEdit, searchClearBtn]))
        masterLayout.addWidget(self.seriesGrid)
        self.grid_refresh()
     
    def search_clear_click(self):
        self.grid_refresh()

    def grid_refresh(self):
        # sql = '''select  0 , pu_serie from books where pu_serie is not null  group by pu_serie order by pu_serie'''
        sql = '''select  0 , serie_name from series where serie_name is not null  order by serie_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.seriesGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        self.seriesGrid.setColumnWidth(0, 0)
        self.seriesGrid.setColumnWidth(1, 500)

    def update_combo(self):
        sqlite_crud.get_series()
        self.seriesList.clear()
        self.seriesList.setHeaderLabels(["Série"])
        items = []
        for n in gl.series_tuple:
            item = QTreeWidgetItem([n[0]])
            items.append(item)
        self.seriesList.insertTopLevelItems(0, items)

    def text_search_changed(self, text):
        search = '\'%' + text.lower() + '%\''
        sql = '''select 0, serie_name
            from series
            where (lower(serie_name)) like ''' + search + '''
            order by serie_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.seriesGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        self.seriesGrid.setColumnWidth(0, 0)
        self.seriesGrid.setColumnWidth(1, 500)

    def rename_click(self):
        try:
            dum = self.seriesGrid.item(self.seriesGrid.currentRow(), 1).text()
            text, flag = QInputDialog.getText(None, "Altera nome da Série:", dum + ' para :', QLineEdit.Normal)
            if flag:
                sqlite_crud.execute_query("delete from collections WHERE collection_name =?;", (dum,))
                sqlite_crud.execute_query("UPDATE books set pu_serie_name=? WHERE pu_serie_name=?;", (text, dum))
                self.grid_refresh()
        except AttributeError:
            pass

    def validate_click(self):
        try:
            self.toto = self.seriesGrid.item(self.seriesGrid.currentRow(), 1).text()
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
