#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QTableWidget, QInputDialog, QDialog, QTextEdit, \
    QTextBrowser, QTableWidgetItem

import qlib as qc
import parameters as gl


class EditSpecialTags(QDialog):
    def __init__(self, pub_id, parent=None):
        super(EditSpecialTags, self).__init__(parent)
        self.resize(480, 360)
        self.setWindowTitle('Edita Etiquetas Especiais')
        self.tags_list = '' # tags_txt.split(',')
        self.pub_id = pub_id
        self.tags_level = 1
        # self.tags_data = tags_data
        masterLayout = QVBoxLayout(self)
        self.tags_string = ''
        self.flag = False
        # self.toto = ()
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
    

    
    def tag_refresh(self):
        tags_dict = {}
        
        for f in gl.tags_special_level1_data:
            tags_dict[f[0]] = f[1]

        for n in gl.tag_special_dict.keys():
            if n in tags_dict:
                pass
            else:
                gl.tags_special_level1_data.append((n,'',gl.tag_special_dict[n]))

        lin = 0
        self.specialTagsGrid.setRowCount(len(gl.tags_special_level1_data))
        self.specialTagsGrid.setColumnCount(3)
        
        for n in gl.tags_special_level1_data:
            item = QTableWidgetItem()
            item.setText(n[2])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.specialTagsGrid.setItem(lin, 0, item)
            
            item = QTableWidgetItem()
            item.setText(n[1])
            self.specialTagsGrid.setItem(lin, 1, item)
            
            item = QTableWidgetItem()
            item.setText(n[0])
            self.specialTagsGrid.setItem(lin, 2, item)
            
            lin += 1
        # ex_grid.ex_grid_update(self.specialTagsGrid, {0: ['Nome', 's'],1:['Valor', 's'], 2:['ID_key', 's']}, tags_data)
        self.specialTagsGrid.horizontalHeader().setVisible(False)
        self.specialTagsGrid.setAlternatingRowColors(True)
        self.specialTagsGrid.setStyleSheet("alternate-background-color: #e6fa0f;")
        self.specialTagsGrid.setColumnWidth(0, 150)
        self.specialTagsGrid.setColumnWidth(1, 250)
        self.specialTagsGrid.hideColumn(2)
    
    # def tag_search_changed(self, text):
    #     if text.length() > 3:
    #         search = '\'%%' + text + '%%\''
    #         # print 'search ',text
    #         sql = '''select ta_id, ta_name from tags where ta_name like unaccent(''' + search + ''') order by ta_name'''
    #         dataset = dbmain.query_many(sql)
    #         ex_grid.ex_grid_update(self.grid, {0: ['ID', 'i'], 1: ['Nome', 's']}, dataset, hidden=0)
    #         self.grid.horizontalHeader().setVisible(False)
    #         self.grid.setColumnWidth(0, 80)
    #         self.grid.setColumnWidth(1, 200)
    
    def valid_click(self):
        self.tags_output = ''
        gl.tags_special_level1_data = []
        for linha in range(0, self.specialTagsGrid.rowCount()):
            try:
                if self.specialTagsGrid.item(linha, 1).text():
                    gl.tags_special_level1_data.append((self.specialTagsGrid.item(linha, 2).text(),
                                                        self.specialTagsGrid.item(linha, 1).text(),
                                                        self.specialTagsGrid.item(linha, 0).text() ))
            except AttributeError:
                # linha vazia
                pass
        self.flag = True
        gl.update_special_tags = True
        self.close()
    
    
    def exit_click(self):
        self.flag = False
        self.close()
