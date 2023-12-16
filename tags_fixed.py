#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QTableWidget, QInputDialog, QDialog, QTextEdit, \
    QTextBrowser, QTableWidgetItem

import qlib as qc
import parameters as gl


class EditFixedTags(QDialog):
    def __init__(self, pub_id, parent=None):
        super(EditFixedTags, self).__init__(parent)
        self.resize(480, 360)
        self.setWindowTitle('Edita Caracteristicas')
        self.tags_list = '' # tags_txt.split(',')
        self.pub_id = pub_id
        self.tags_level = 1
        # self.tags_data = tags_data
        masterLayout = QVBoxLayout(self)
        self.tags_string = ''
        self.flag = False
        # self.toto = ()
        self.fixedTagsGrid = QTableWidget()
        self.fixedTagsGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.fixedTagsGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.fixedTagsGrid.setEditTriggers(QTableWidget.AllEditTriggers)
        self.fixedTagsGrid.verticalHeader().setDefaultSectionSize(20)
        self.fixedTagsGrid.setAlternatingRowColors(True)
        self.fixedTagsGrid.verticalHeader().setVisible(False)
        masterLayout.addWidget(self.fixedTagsGrid)
        exit_btn = QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn = QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        
        masterLayout.addLayout(qc.addHLayout([valid_btn, exit_btn]))
        
        self.tag_refresh()
    

    
    def tag_refresh(self):
        tags_dict = {}
        
        for f in gl.FIXED_TAGS_DATA:
            tags_dict[f[0]] = f[1]

        for n in gl.tag_special_dict.keys():
            if n in tags_dict:
                pass
            else:
                gl.FIXED_TAGS_DATA.append((n, '', gl.tag_special_dict[n]))

        lin = 0
        self.fixedTagsGrid.setRowCount(len(gl.FIXED_TAGS_DATA))
        self.fixedTagsGrid.setColumnCount(3)
        
        for n in gl.FIXED_TAGS_DATA:
            item = QTableWidgetItem()
            item.setText(n[2])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.fixedTagsGrid.setItem(lin, 0, item)
            
            item = QTableWidgetItem()
            item.setText(n[1])
            self.fixedTagsGrid.setItem(lin, 1, item)
            
            item = QTableWidgetItem()
            item.setText(n[0])
            self.fixedTagsGrid.setItem(lin, 2, item)
            
            lin += 1
        # ex_grid.ex_grid_update(self.specialTagsGrid, {0: ['Nome', 's'],1:['Valor', 's'], 2:['ID_key', 's']}, tags_data)
        self.fixedTagsGrid.horizontalHeader().setVisible(False)
        self.fixedTagsGrid.setAlternatingRowColors(True)
        self.fixedTagsGrid.setStyleSheet("alternate-background-color: #e6fa0f;")
        self.fixedTagsGrid.setColumnWidth(0, 150)
        self.fixedTagsGrid.setColumnWidth(1, 250)
        self.fixedTagsGrid.hideColumn(2)
    

    def valid_click(self):
        self.tags_output = ''
        gl.FIXED_TAGS_DATA = []
        for linha in range(0, self.fixedTagsGrid.rowCount()):
            # try:
            # if self.fixedTagsGrid.item(linha, 1).text():
            gl.FIXED_TAGS_DATA.append((self.fixedTagsGrid.item(linha, 2).text(),
                                           self.fixedTagsGrid.item(linha, 1).text(),
                                           self.fixedTagsGrid.item(linha, 0).text()))
            # except AttributeError:
                # linha vazia
                # pass
        self.flag = True
        gl.update_special_tags = True
        self.close()
    
    
    def exit_click(self):
        self.flag = False
        self.close()
