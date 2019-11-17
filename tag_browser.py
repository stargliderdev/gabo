#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QTableWidget, QInputDialog, QDialog,QTextEdit, QTextBrowser

import ex_grid
import dmPostgreSQL as dbmain
import qlib as qc
import parameters as gl

class BrowserTags(QDialog):
    def __init__(self,  parent = None):
        super(BrowserTags,  self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.flag = False
        self.resize(800, 400)
        self.setWindowTitle('Etiquetas')
        masterLayout = QVBoxLayout(self)
        self.tag_list = []
        self.tag_id = -1
        deselect_tags_Btn=QPushButton('Des-seleciona')
        deselect_tags_Btn.clicked.connect(self.deselect_click)
        
        clean_tranf_Btn=QPushButton('Limpa Transferidas')
        clean_tranf_Btn.clicked.connect(self.clean_transfer)
        
        add_tag_Btn=QPushButton('Adiciona Tag')
        add_tag_Btn.clicked.connect(self.add_new_tag)
        
        masterLayout.addLayout(qc.addHLayout([deselect_tags_Btn,clean_tranf_Btn,add_tag_Btn,True]))
        self.searchEdit = QLineEdit()
        self.toto = ()
        self.searchEdit.textChanged.connect(self.tag_search_changed)
        masterLayout.addWidget(self.searchEdit)
        self.grid = QTableWidget()
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.verticalHeader().setDefaultSectionSize(20)
        self.grid.verticalHeader().setVisible(False)
        self.grid.itemDoubleClicked.connect(self.transfer_click)

        self.lastTags_grid = QTableWidget()
        self.lastTags_grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lastTags_grid.verticalHeader().setDefaultSectionSize(20)
        self.lastTags_grid.verticalHeader().setVisible(False)
        self.lastTags_grid.itemDoubleClicked.connect(self.transfer_last_click)
        
        self.current_tags = QTextBrowser()
        self.current_tags.setMaximumHeight(90)
        self.current_tags.setMinimumHeight(90)
    
        masterLayout.addLayout(qc.addHLayout([self.grid,self.lastTags_grid]))
        masterLayout.addWidget(self.current_tags)
        exit_btn=QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn=QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        
        add_btn=QPushButton('Adiciona')
        add_btn.clicked.connect(self.add_click)
        
        masterLayout.addLayout(qc.addHLayout([valid_btn,add_btn,exit_btn]))
        
        self.tag_refresh()
        self.last_tag_refresh()

    def deselect_click(self):
        self.grid.clearSelection()

    def clean_transfer(self):
        self.current_tags.clear()

    def add_new_tag(self):
        b, ok = QInputDialog.getText(self, self.tr("Nova Etiqueta"), self.tr("Nova Etiqueta"), QLineEdit.Normal)
        if ok and not b == '' :
            if self.current_tags.toPlainText() == '':
                self.current_tags.setText(b)
            else:
             self.current_tags.setText(self.current_tags.toPlainText() +  ',' + b)
        else:
            print('do nothing')

    def transfer_click(self):
        # self.tag_list.append(self.grid.item(self.grid.currentRow(), 1).text())
        a = self.grid.item(self.grid.currentRow(), 1).text()
        gl.last_tags.insert(0,(0,self.grid.item(self.grid.currentRow(), 1).text()))
        # xl = self.current_tags.toPlainText() + ',' + a
        self.tag_list = self.current_tags.toPlainText().split(',')
        self.tag_list.append(a)
        xl = ''
        for n in self.tag_list:
            xl += '<font color="blue"><strong>' + n + ',</font>'
        self.current_tags.setHtml(xl)
        self.searchEdit.clear()
        self.searchEdit.setFocus()


    def transfer_last_click(self):
        # self.tag_list.append(self.lastTags_grid.item(self.lastTags_grid.currentRow(), 1).text())
        a = self.lastTags_grid.item(self.lastTags_grid.currentRow(), 1).text()
        self.tag_list = self.current_tags.toPlainText().split(',')
        self.tag_list.append(a)
        xl = ''
        for n in self.tag_list:
            xl += '<font color="blue"><strong>' + n + ',</font>'
    
        # print(xl)
        self.current_tags.setHtml(xl)
        
    def valid_click(self):
        self.tag_id = 0
        self.tag_list = self.current_tags.toPlainText()
        self.tag_list = self.tag_list.replace(',,',',')
        self.tag_list = self.tag_list.rstrip(',')
        self.tag_list = self.tag_list.lstrip(',')
        self.flag = True
        self.close()

    def add_click(self):
        self.tag_id = 1
        self.tag_list = self.current_tags.toPlainText()
        self.tag_list = self.tag_list.replace(',,',',')
        self.tag_list = self.tag_list.rstrip(',')
        self.tag_list = self.tag_list.lstrip(',')
        self.flag = True
        self.close()

    def tag_refresh(self):
        self.c_grid = 10
        sql = '''select ta_id, ta_name from tags order by ta_name'''
        dataset = dbmain.query_many(sql)
        ex_grid.ex_grid_update (self.grid, {0:['ID','i'],1:['Nome', 's']}, dataset, hidden=0)
        self.grid.horizontalHeader().setVisible(False)
        self.grid.setColumnWidth(0, 80)
        self.grid.setColumnWidth(1, 350)
        
    def last_tag_refresh(self):
        self.c_grid = 10
        ex_grid.ex_grid_update (self.lastTags_grid, {0:['ID','i'], 1:['Nome', 's']}, gl.last_tags, hidden=0)
        self.grid.horizontalHeader().setVisible(False)
        self.grid.setColumnWidth(0, 80)
        self.grid.setColumnWidth(1, 350)
        

        

    def tag_search_changed(self, text):
        if len(text)>3:
            search = '\'%%' + text + '%%\''
            # print 'search ',text
            sql = '''select ta_id, ta_name from tags where unaccent(ta_name) like unaccent(''' + search + ''') order by ta_name'''
            dataset = dbmain.query_many(sql)
            ex_grid.ex_grid_update (self.grid, {0:['ID','i'],1:['Nome', 's']}, dataset, hidden=0)
            self.grid.horizontalHeader().setVisible(False)
            self.grid.setColumnWidth(0, 80)
            self.grid.setColumnWidth(1, 350)

    def exit_click(self):
        self.tag_list = ''
        self.tag_id = -1
        self.close()


class EditRecordTags(QDialog):
    def __init__(self, tags_data, parent = None):
        super(EditRecordTags,  self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.resize(400, 350)
        self.setWindowTitle('Edita Etiquetas do Registo')
        self.tags_data = tags_data
        masterLayout = QVBoxLayout(self)
        self.tag_list=''
        self.flag = False
        self.searchEdit = QLineEdit()
        self.toto = ()
        self.searchEdit.textChanged.connect(self.tag_search_changed)
        
        masterLayout.addWidget(self.searchEdit)
        self.grid = QTableWidget()
        self.grid.setSelectionBehavior(QTableWidget.SelectRows)
        self.grid.setSelectionMode(QTableWidget.SingleSelection)
        self.grid.setEditTriggers(QTableWidget.AllEditTriggers)
        self.grid.verticalHeader().setDefaultSectionSize(20)
        self.grid.setAlternatingRowColors (True)
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
        if text.length()>3:
            search = '\'%%' + text + '%%\''
            # print 'search ',text
            sql = '''select ta_id, ta_name from tags where ta_name like unaccent(''' + search + ''') order by ta_name'''
            dataset = dbmain.query_many(sql)
            ex_grid.ex_grid_update (self.grid, {0:['ID','i'],1:['Nome', 's']}, dataset, hidden=0)
            self.grid.horizontalHeader().setVisible(False)
            self.grid.setColumnWidth(0, 80)
            self.grid.setColumnWidth(1, 200)

    def exit_click(self):
        self.tag_list = ''
        self.close()

def main():
    app = QApplication()
    form = BrowserTags()
    form.show()
    app.exec_()

if __name__ == '__main__':
    pass

