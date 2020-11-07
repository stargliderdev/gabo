#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QTableWidget, QInputDialog, QDialog, QTextEdit, \
    QTextBrowser, QTableWidgetItem

import ex_grid
import dmPostgreSQL as dbmain
import qlib as qc
import parameters as gl
from data_access import save_param, save_last_tags_params


class BrowserTags(QDialog):
    def __init__(self,  parent = None):
        super(BrowserTags,  self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.flag = False
        self.resize(1024, 768)
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
        self.current_tags.setMaximumHeight(60)
        self.current_tags.setMinimumHeight(60)
    
        masterLayout.addLayout(qc.addHLayout([self.grid,self.lastTags_grid]))
        masterLayout.addWidget(self.current_tags)
        exit_btn=QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn=QPushButton('Substitui')
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
        a = self.grid.item(self.grid.currentRow(), 1).text()
        gl.last_tags.insert(0,self.grid.item(self.grid.currentRow(), 1).text())
        self.tag_list = self.current_tags.toPlainText().split(',')
        self.tag_list.append(a)
        xl = ''
        for n in self.tag_list:
            xl += '<font color="blue"><strong>' + n + ',</font>'
        self.current_tags.setHtml(xl)
        self.searchEdit.clear()
        self.searchEdit.setFocus()
        

    def transfer_last_click(self):
        a = self.lastTags_grid.item(self.lastTags_grid.currentRow(), 0).text()
        self.tag_list = self.current_tags.toPlainText().split(',')
        self.tag_list.append(a)
        xl = ''
        for n in self.tag_list:
            xl += '<font color="blue"><strong>' + n + ',</font>'
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
        save_last_tags_params()
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
        lin=0
        self.lastTags_grid.setColumnCount(1)
        self.lastTags_grid.setRowCount(len(gl.last_tags))
        
        for n in gl.last_tags:
            item = QTableWidgetItem()
            item.setText(n)
            self.lastTags_grid.setItem(lin, 0, item)
            lin +=1
        self.lastTags_grid.horizontalHeader().setVisible(False)
        self.lastTags_grid.setColumnWidth(0, 450)
        

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
            dataset = dbmain.query_many(sql)
            ex_grid.ex_grid_update (self.grid, {0:['ID','i'],1:['Nome', 's']}, dataset, hidden=0)
            self.grid.horizontalHeader().setVisible(False)
            self.grid.hideColumn(0)
            self.grid.setColumnWidth(1, 200)

    def exit_click(self):
        self.tag_list = ''
        self.close()


class EditSpecialTags(QDialog):
    def __init__(self, tags_txt, parent=None):
        super(EditSpecialTags, self).__init__(parent)
        self.resize(480, 360)
        self.setWindowTitle('Edita Etiquetas Especiais')
        self.tags_list = tags_txt.split(',')
        masterLayout = QVBoxLayout(self)
        self.tags_string = ''
        self.flag = False
        self.toto = ()
        self.specialTagsGrid = QTableWidget()
        self.specialTagsGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.specialTagsGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.specialTagsGrid.setEditTriggers(QTableWidget.AllEditTriggers)
        self.specialTagsGrid.verticalHeader().setDefaultSectionSize(20)
        self.specialTagsGrid.setAlternatingRowColors(True)
        self.specialTagsGrid.verticalHeader().setVisible(False)
        masterLayout.addWidget(self.specialTagsGrid)
        exit_btn = QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn = QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        
        masterLayout.addLayout(qc.addHLayout([valid_btn, exit_btn]))
        
        self.tag_refresh()
    
    def valid_click(self):
        self.tags_output = ''
        for linha in range(0, self.specialTagsGrid.rowCount()):
            try:
                if self.specialTagsGrid.item(linha, 1).text():
                    self.tags_output += str(self.specialTagsGrid.item(linha, 2).text()) + ':' + str(self.specialTagsGrid.item(linha, 1).text()) + ','
            except AttributeError:
                # linha vazia
                pass
        self.tags_output = self.tags_output.replace(',,', ',')
        self.tags_output = self.tags_output.rstrip(',')
        self.tags_output = self.tags_output.lstrip(',')
        self.flag = True
        for n in self.tags_list:
            if n.find(':')>-1:
                pass
            else:
                self.tags_output += ',' + n
        self.tags_output = self.tags_output.lstrip(',')
        self.close()
    
    def tag_refresh(self):
        tags_data = []
        tags_data_dict = {}
        for n in self.tags_list:
            toto = n.lower().strip()
            t_key = toto.split(':')
            if len(t_key)>1:
                # encontrou uma tag especial
                try:
                    # print(t_key, gl.tag_special_dict[t_key[0]], '|', t_key[1])
                    tags_data_dict [t_key[0]] = (gl.tag_special_dict[t_key[0]], t_key[1], t_key[0])
                except KeyError:
                    pass
        for key in gl.tag_special_dict.keys():
            if key in tags_data_dict:
                tags_data.append(tags_data_dict[key])
            else:
                tags_data.append((gl.tag_special_dict[key], '', key))
        lin = 0
        self.specialTagsGrid.setRowCount(len(tags_data))
        self.specialTagsGrid.setColumnCount(3)
        for n in tags_data:
            item = QTableWidgetItem()
            item.setText(n[0])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.specialTagsGrid.setItem(lin, 0, item)

            item = QTableWidgetItem()
            item.setText(n[1])
            self.specialTagsGrid.setItem(lin, 1, item)

            item = QTableWidgetItem()
            item.setText(n[2])
            self.specialTagsGrid.setItem(lin, 2, item)

            
            
            lin +=1
        # ex_grid.ex_grid_update(self.specialTagsGrid, {0: ['Nome', 's'],1:['Valor', 's'], 2:['ID_key', 's']}, tags_data)
        self.specialTagsGrid.horizontalHeader().setVisible(False)
        self.specialTagsGrid.setAlternatingRowColors(True)
        self.specialTagsGrid.setStyleSheet("alternate-background-color: #e6fa0f;")
        self.specialTagsGrid.setColumnWidth(0, 150)
        self.specialTagsGrid.setColumnWidth(1, 250)
        self.specialTagsGrid.hideColumn(2)
    
    def tag_search_changed(self, text):
        if text.length() > 3:
            search = '\'%%' + text + '%%\''
            # print 'search ',text
            sql = '''select ta_id, ta_name from tags where ta_name like unaccent(''' + search + ''') order by ta_name'''
            dataset = dbmain.query_many(sql)
            ex_grid.ex_grid_update(self.grid, {0: ['ID', 'i'], 1: ['Nome', 's']}, dataset, hidden=0)
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

