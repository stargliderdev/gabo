#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTableWidget, QDialog, QApplication

import ex_grid
import dmPostgreSQL as libpg
import qlib as qc
import parameters as gl
import stdio

class EditRecordTags(QDialog):
    def __init__(self, tags_data, parent = None):
        super(EditRecordTags,  self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.resize(450, 380)
        self.setWindowTitle('Edita Etiquetas do Registo')
        self.tags_data = tags_data
        masterLayout = QVBoxLayout(self)
        self.tag_list=''
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
        masterLayout.addWidget(self.grid)
        exit_btn=QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn=QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        
        masterLayout.addLayout(qc.addHLayout([valid_btn,exit_btn]))

        self.tag_refresh()

    def valid_click(self):
        # self.tag_id=[]
        for linha in range(0, self.grid.rowCount()):
            try:
                self.tag_list += str(self.grid.item(linha,1).text()) +','
            except AttributeError:
                # linha vazia
                pass
        self.tag_list = self.tag_list.replace(',,',',')
        self.tag_list = self.tag_list.rstrip(',')
        self.tag_list = self.tag_list.lstrip(',')
        self.flag = True
        self.close()

    def tag_refresh(self):
        # self.c_grid = 10
        ex_grid.ex_grid_update(self.grid, {0:['ID','i'],1:['Nome', 's']}, self.tags_data, hidden=0)
        self.grid.setRowCount(self.grid.rowCount() + 5)
        self.grid.horizontalHeader().setVisible(False)
        self.grid.setColumnWidth(0, 80)
        self.grid.setColumnWidth(1, 350)

    def tag_search_changed(self, text):
        if len(text)>3:
            search = '\'%%' + text + '%%\''
            # print 'search ',text
            sql = '''select ta_id, ta_name from tags where ta_name like unaccent(''' + search + ''') order by ta_name'''
            dataset = libpg.query_many(sql)
            ex_grid.ex_grid_update (self.grid, {0:['ID','i'],1:['Nome', 's']}, dataset, hidden=0)
            self.grid.horizontalHeader().setVisible(False)
            self.grid.hideColumn(0)
            self.grid.setColumnWidth(1, 200)

    def exit_click(self):
        self.tag_list = ''
        gl.LAST_TAG = ''
        self.close()




def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    app = QApplication(sys.argv)
    form = EditRecordTags()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

