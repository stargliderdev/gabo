#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QTableWidget, QPushButton, QDialog, QInputDialog, \
    QToolButton

import ex_grid
import qlib as qc

import parameters as gl
import sqlite_crud


class BrowserAuthors(QDialog):
    def __init__(self,  parent = None):
        super(BrowserAuthors,  self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle('Autores')
        self.setWindowIcon(QIcon('./img/authors.png'))
        masterLayout = QVBoxLayout(self)
        self.searchEdit = QLineEdit()
        self.toto = ''
        self.searchEdit.textChanged.connect(self.grid_search_changed)
        searchClearBtn = QToolButton()
        searchClearBtn.setToolTip('Limpa Pesquisa')
        searchClearBtn.setIcon(QIcon('./img/clear.png'))
        searchClearBtn.clicked.connect(self.search_clear_click)
        exitBtn=QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)

        valid_btn=QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)

        edit_btn=QPushButton('Altera')
        edit_btn.clicked.connect(self.edit_click)
        masterLayout.addLayout(qc.addHLayout([valid_btn, edit_btn, exitBtn]))
        masterLayout.addLayout(qc.addHLayout([self.searchEdit, searchClearBtn]))
        self.authorGrid = QTableWidget()
        self.authorGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.authorGrid.setSelectionMode(QTableWidget.SingleSelection)

        self.authorGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.authorGrid.verticalHeader().setDefaultSectionSize(20)
        self.authorGrid.verticalHeader().setVisible(False)
        self.authorGrid.setAlternatingRowColors(True)
        self.authorGrid.setStyleSheet("alternate-background-color: #99ffcc;")
        self.authorGrid.itemDoubleClicked.connect(self.valid_click)
        masterLayout.addWidget(self.authorGrid)
        if not gl.AUTHOR_SEARCH_MASK == '':
            self.searchEdit.setText(gl.AUTHOR_SEARCH_MASK)
            self.grid_search_changed(gl.AUTHOR_SEARCH_MASK)
        else:
            self.grid_refresh()
        self.searchEdit.setFocus()

    def search_clear_click(self):
        self.searchEdit.clear()

    def valid_click(self):
        try:
            self.toto = self.authorGrid.item(self.authorGrid.currentRow(), 1).text()
            gl.AUTHOR_SEARCH_MASK = self.searchEdit.text()
            self.close()
        except AttributeError:
            pass

    def edit_click(self):
        # re-escrever
        self.toto = ''
        if self.authorGrid.item(self.authorGrid.currentRow(),0) is None:
            pass
        else:
            old_name = self.authorGrid.item(self.authorGrid.currentRow(), 0).text()
            text, flag = QInputDialog.getText(None, "Edita nome do Autor:","",
                                              QLineEdit.Normal, self.authorGrid.item(self.authorGrid.currentRow(), 1).text())
    
            if flag:
                sqlite_crud.execute_query('update authors set au_name=? where au_name=?', (text, old_name))
                sqlite_crud.execute_query('update books set pu_author=? where pu_author=?', (text, old_name))
                self.grid_search_changed(self.searchEdit.text())
                sqlite_crud.get_authors()
            else:
                print('faz nada')

    def grid_refresh(self):
        self.c_grid = 10
        sql = '''select au_name, au_name, count(*) as a
            from authors, books
            where au_name = pu_author --and au_id > 0
            group by au_name
            order by au_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.authorGrid, {0:['ID', 'i'], 1:['Nome', 's'], 2:['Livros', 'i']}, dataset)
        self.authorGrid.setColumnWidth(0, 0)
        self.authorGrid.setColumnWidth(1, 500)
        self.authorGrid.setColumnWidth(2, 60)

    def grid_search_changed(self, text):
        search = '\'%' + text.lower() + '%\''
        sql = '''select pu_author, pu_author, count(*) as a
            from books
            where lower(pu_author) like ''' + search + '''
            group by pu_author
            order by pu_author'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.authorGrid, {0:['ID', 'i'], 1:['Nome', 's'], 2:['Livros', 'i']}, dataset)
        self.authorGrid.setColumnWidth(0, 0)
        self.authorGrid.setColumnWidth(1, 500)
        self.authorGrid.setColumnWidth(2, 60)

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()

