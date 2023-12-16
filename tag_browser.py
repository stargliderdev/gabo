#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTableWidget, QDialog, QApplication, QTableWidgetItem, QLineEdit

import ex_grid

import qlib as qc
import parameters as gl
import sqlite_crud

class EditRecordTags(QDialog):
    def __init__(self, tags_data, parent = None):
        super(EditRecordTags,  self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.resize(600, 400)
        self.setWindowTitle('Edita Etiquetas do Registo')
        self.tags_data = tags_data
        masterLayout = QVBoxLayout(self)
        self.searchText = QLineEdit()
        self.searchText.textChanged.connect(self.tag_search_changed)
        masterLayout.addWidget(self.searchText)
        self.tagsGrid = QTableWidget()
        self.tagsGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tagsGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.tagsGrid.verticalHeader().setDefaultSectionSize(20)
        self.tagsGrid.verticalHeader().setVisible(False)
        self.tagsGrid.setAlternatingRowColors(True)
        self.tagsGrid.setStyleSheet("alternate-background-color: #d2e5ff;")
        self.tagsGrid.itemDoubleClicked.connect(self.transfer_click)

        self.tags_string= ''
        self.flag = False
        self.toto = ()
        self.grid = QTableWidget()
        self.grid.setSelectionBehavior(QTableWidget.SelectRows)
        self.grid.setSelectionMode(QTableWidget.SingleSelection)
        self.grid.setEditTriggers(QTableWidget.AllEditTriggers)
        self.grid.verticalHeader().setDefaultSectionSize(20)
        self.grid.setAlternatingRowColors (True)
        self.grid.setAlternatingRowColors(True)
        self.grid.setStyleSheet("alternate-background-color: #effa0f;")
        self.grid.verticalHeader().setVisible(False)
        masterLayout.addLayout(qc.addHLayout([self.tagsGrid,self.grid]))
        # masterLayout.addWidget(self.grid)
        exit_btn=QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn=QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        
        masterLayout.addLayout(qc.addHLayout([valid_btn,exit_btn]))
        self.all_tags_refresh()
        self.current_tags_refresh()

    def valid_click(self):
        sqlite_crud.execute_query('delete from tags_reference where tags_ref_book=?', (gl.record_current_dict['pu_id'],))
        for linha in range(0, self.grid.rowCount()):
            try:
                if str(self.grid.item(linha,0).text()) == '':
                    pass
                else:
                    self.tags_string += str(self.grid.item(linha, 0).text()) + '|'
                    sqlite_crud.execute_query('insert into tags_reference (tags_ref_book, tags_ref_key) values (?,?)',
                                          (gl.record_current_dict['pu_id'], self.grid.item(linha, 0).text().lower()))
            except AttributeError:
                # linha vazia
                pass
        # self.tag_list = self.tag_list.replace(',,',',')
        self.tags_string = self.tags_string.rstrip('|')
        self.tags_string = self.tags_string.lstrip('|')
        sqlite_crud.execute_query('update books set pu_tags=?  where pu_id=?', (self.tags_string.lower(), gl.record_current_dict['pu_id']))
        gl.record_current_dict['pu_tags'] = self.tags_string

        self.flag = True
        self.close()

    def current_tags_refresh(self):
        self.grid.setColumnCount(1)
        self.grid.setColumnWidth(0,200)
        self.grid.setRowCount(25) # é o maximo até ver
        lin = 0
        for n in self.tags_data:
            item = QTableWidgetItem()
            item.setText(n.strip())
            self.grid.setItem(lin, 0, item)
            lin +=1
        self.grid.horizontalHeader().setVisible(False)

    def tag_search_changed(self, text):
        if len(text) > 3:
            search = '\'%%' + text + '%%\''
            # print 'search ',text
            sql = '''select ta_id, ta_name from tags where ta_name like (''' + search + ''') order by ta_name'''
            dataset = sqlite_crud.query_many(sql)
            ex_grid.ex_grid_update (self.grid, {0:['ID','i'],1:['Nome', 's']}, dataset, hidden=0)
            self.grid.horizontalHeader().setVisible(False)
            self.grid.hideColumn(0)
            self.grid.setColumnWidth(1, 200)

    def all_tags_refresh(self):
        self.c_grid = 10
        # sql = '''select ta_id, ta_name from tags order by ta_name'''
        sql = '''select ta_id,ta_name from tags order by ta_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.tagsGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset, hidden=0)
        self.tagsGrid.horizontalHeader().setVisible(False)
        self.tagsGrid.setColumnWidth(0, 80)
        self.tagsGrid.setColumnWidth(1, 350)

    def transfer_click(self):
        a = self.tagsGrid.item(self.tagsGrid.currentRow(), 1).text()
        for linha in range(0, self.grid.rowCount()):
            try:
                if str(self.grid.item(linha,0).text()) == '':
                    item = QTableWidgetItem()
                    item.setText(a.strip())
                    self.grid.setItem(linha, 0, item)
                    break
            except AttributeError:
                # linha vazia
                item = QTableWidgetItem()
                item.setText(a.strip())
                self.grid.setItem(linha, 0, item)
                break

    def tag_search_changed(self, text):
        if len(text) > 2:
            search = '\'%' + text + '%\''
            # print 'search ',text
            sql = '''SELECT  0, ta_name FROM tags WHERE ta_name LIKE ''' + search + ''' ORDER by ta_name '''
            dataset = sqlite_crud.query_many(sql)
            ex_grid.ex_grid_update (self.tagsGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset, hidden=0)
            self.tagsGrid.horizontalHeader().setVisible(False)
            self.tagsGrid.setColumnWidth(0, 80)
            self.tagsGrid.setColumnWidth(1, 350)


    def exit_click(self):
        self.tags_string = ''
        gl.LAST_TAG = ''
        self.close()

def main():
    app = QApplication(sys.argv)
    form = EditRecordTags(['musica portuguesa', 'literatura', 'música', 'manuel faria', 'biografias', 'trovante', 'bandas portuguesas'])
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
