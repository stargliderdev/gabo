#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QTreeWidget, QTreeWidgetItem, QToolButton, QTableWidget, QComboBox, QTableWidgetItem
from PyQt5.Qt import Qt
import ex_grid
import lib_gabo
import qlib as qc
# import sqlite_crud
import parameters as gl
import settings
import sqlite_crud
import stdio


class CollectionBrowser(QDialog):
    def __init__(self,  parent = None):
        super(CollectionBrowser, self).__init__(parent)
        self.resize(400, 900)
        self.toto = ''
        self.setWindowTitle('Colecções')
        self.setWindowIcon(QIcon('./img/collections.png'))
        masterLayout = QVBoxLayout(self)
        self.mainSearchCbox = QComboBox()
        # self.mainSearchCbox.setMaximumWidth(90)
        # self.mainSearchCbox.setMinimumWidth(90)
        self.mainSearchCbox.addItems(['Titulo', 'Autor', 'ISBN', 'Etiqueta', 'Colecção', 'Série'])
        self.mainSearchCbox.setCurrentIndex(0)

        self.mainToSearchEdt = QLineEdit()
        # self.mainToSearchEdt.setMaximumWidth(300)
        # self.mainToSearchEdt.setMinimumWidth(300)
        self.mainToSearchEdt.textChanged.connect(self.text_search_changed)


        # self.searchEdit= QLineEdit()
        # self.searchEdit.textChanged.connect(self.text_search_changed)
        searchClearBtn = QToolButton()
        searchClearBtn.setToolTip('Limpa Pesquisa')
        searchClearBtn.setIcon(QIcon('./img/clear.png'))
        searchClearBtn.clicked.connect(self.search_clear_click)
        # self.collectionList = QTreeWidget()
        # self.collectionList.setColumnWidth(0, 200)
        self.mobileGrid = QTableWidget()
        self.mobileGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.mobileGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.mobileGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.mobileGrid.verticalHeader().setDefaultSectionSize(20)
        self.mobileGrid.verticalHeader().setVisible(False)
        self.mobileGrid.setAlternatingRowColors(True)
        self.mobileGrid.setStyleSheet("alternate-background-color: #F5F4F2;")
        self.mobileGrid.setColumnCount(1)
        self.mobileGrid.setHorizontalHeaderLabels(['Titulo', 'Autor'])
        self.mobileGrid.horizontalHeader().setVisible(True)
        self.mobileGrid.itemDoubleClicked.connect(self.validate_click)
        masterLayout.addWidget(self.mobileGrid)

        validateBtn = QPushButton('Valida')
        validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        masterLayout.addLayout(qc.addHLayout([self.mainSearchCbox,exitBtn]))
        masterLayout.addLayout(qc.addHLayout([self.mainToSearchEdt, searchClearBtn]))
        masterLayout.addWidget(self.mobileGrid)
        # self.grid_refresh()

    def search_clear_click(self):
        self.grid_refresh()

    def text_search_changed(self, text):
        """will search in title, tags and ISBN"""
        print('SEARCH', text)
        if  len(self.mainToSearchEdt.text()) > 2:
            gl.SEARCH_DICT['LAST'] = 0
            if self.mainSearchCbox.currentIndex() == 0:  # title
                gl.SEARCH_DICT['WHERE'] = 'title'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
            elif self.mainSearchCbox.currentIndex() == 1:  # author
                gl.SEARCH_DICT['WHERE'] = 'author'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
                gl.SEARCH_DICT['ORDER'] = 'pu_author'
                gl.SEARCH_DICT['ORDER_BY'] = 'ASC'
            elif self.mainSearchCbox.currentIndex() == 2:  # ISBN
                gl.SEARCH_DICT['WHERE'] = 'isbn'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 3:  # tags
                gl.SEARCH_DICT['WHERE'] = 'tags_or'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 4:  # colecção
                gl.SEARCH_DICT['WHERE'] = 'collection'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
            elif self.mainSearchCbox.currentIndex() == 5:
                gl.SEARCH_DICT['WHERE'] = 'serie'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
            # self.update_grid()

            sql = lib_gabo.make_sql(gl.SEARCH_DICT)
            dataset = sqlite_crud.query_many(sql)
            self.mobileGrid.setRowCount(len(dataset))
            line = 0
            for n in dataset:
                print(n)
                item = QTableWidgetItem()
                item.setText(str(n[1]))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.mobileGrid.setItem(line, 0, item)
                line +=1
                item = QTableWidgetItem()
                font = QFont()
                font.setBold(True)
                item.setFont(font)
                item.setForeground(QColor(0, 171, 255))
                item.setText(n[2])
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.mobileGrid.setItem(line, 0, item)
                line +=1
        # self.mobileGrid.setColumnWidth(0, 40)
        # self.mobileGrid.setColumnWidth(1, 310)

        # search = '\'%' + text.lower() + '%\''rr
        # sql = '''select 0, collection_name
        #     from collections
        #     where (lower(collection_name)) like ''' + search + '''
        #     order by collection_name'''
        # dataset = sqlite_crud.query_many(sql)
        # ex_grid.ex_grid_update (self.mobileGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset)
        # self.mobileGrid.setColumnWidth(0, 0)
        # self.mobileGrid.setColumnWidth(1, 500)

    def rename_click(self):
        self.close()
    def validate_click(self):
        self.close()

    def exit_click(self):
        self.close()


def main():
    settings.load_settings()
    app = QApplication(sys.argv)
    form = CollectionBrowser()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
