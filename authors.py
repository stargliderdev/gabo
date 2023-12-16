#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QTableWidget, QPushButton, QApplication, QDialog, QInputDialog

import ex_grid
import dmPostgreSQL as dbmain
import qlib as qc
import data_access
import parameters as gl

class BrowserAuthors(QDialog):
    def __init__(self,  parent = None):
        super(BrowserAuthors,  self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle('Autores')
        masterLayout = QVBoxLayout(self)
        self.searchEdit = QLineEdit()
        self.toto = ''
        self.searchEdit.textChanged.connect(self.grid_search_changed)
        
        masterLayout.addWidget(self.searchEdit)
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
        exitBtn=QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        
        valid_btn=QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        
        edit_btn=QPushButton('Altera')
        edit_btn.clicked.connect(self.edit_click)
        masterLayout.addLayout(qc.addHLayout([valid_btn, edit_btn, exitBtn]))
        if not gl.AUTHOR_SEARCH_MASK == '':
            self.searchEdit.setText(gl.AUTHOR_SEARCH_MASK)
            self.grid_search_changed(gl.AUTHOR_SEARCH_MASK)
        else:
            self.grid_refresh()
        self.searchEdit.setFocus()
        
    def valid_click(self):
        try:
            self.toto = self.authorGrid.item(self.authorGrid.currentRow(), 1).text()
            gl.AUTHOR_SEARCH_MASK = self.searchEdit.text()
            self.close()
        except AttributeError:
            pass


    def edit_click(self):
        self.toto = ''
        if self.authorGrid.item(self.authorGrid.currentRow(),0) is None:
            pass
        else:
            au_id = int(self.authorGrid.item(self.authorGrid.currentRow(), 0).text())
            text, flag = QInputDialog.getText(None, "Edita nome do Autor:","",
                                              QLineEdit.Normal, self.authorGrid.item(self.authorGrid.currentRow(), 1).text())
    
            if flag:
                dbmain.execute_query('update authors set au_name=%s where au_id=%s ', (text, au_id))
                self.grid_search_changed(self.searchEdit.text())
                data_access.get_autores()
            else:
                print('faz nada')

    def grid_refresh(self):
        self.c_grid = 10
        sql = '''select pu_author_id, authors.au_name,count(*) as a
            from livros,authors
            where authors.au_id = pu_author_id and au_id > 0
            group by pu_author_id,authors.au_name
            order by authors.au_name'''
        dataset = dbmain.query_many(sql)
        ex_grid.ex_grid_update (self.authorGrid, {0:['ID', 'i'], 1:['Nome', 's'], 2:['Livros', 'i']}, dataset)
        self.authorGrid.setColumnWidth(0, 0)
        self.authorGrid.setColumnWidth(1, 500)
        self.authorGrid.setColumnWidth(2, 60)

    def grid_search_changed(self, text):
        search = '\'%%' + text.lower() + '%%\''
        sql = '''select pu_author_id, authors.au_name,count(*) as a
            from livros,authors
            where authors.au_id = pu_author_id and unaccent(lower(au_name)) like unaccent(''' + search + ''')
            group by pu_author_id,authors.au_name
            order by authors.au_name'''
        dataset = dbmain.query_many(sql)
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

