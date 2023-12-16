#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
      QTreeWidget, QTreeWidgetItem

import qlib as qc
# import sqlite_crud
import parameters as gl
import sqlite_crud
import stdio


class ClassificationsBrowser(QDialog):
    def __init__(self,  parent = None):
        super(ClassificationsBrowser,  self).__init__(parent)
        self.setWindowTitle('Classificações')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.classificationsList = QTreeWidget()
        self.classificationsList.setColumnWidth(0,200)
        
        addBtn = QPushButton('Adiciona')
        addBtn.clicked.connect(self.add_click)
        
        deleteBtn = QPushButton('Apaga')
        deleteBtn.clicked.connect(self.delete_click)
        
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)
        
        orderBtn = QPushButton('Ordem')
        orderBtn.clicked.connect(self.order_click)
        
        exitBtn = QPushButton('Sair')
        exitBtn.setMinimumWidth(400)
        exitBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qc.addHLayout([addBtn,renameBtn,orderBtn, deleteBtn]))
        masterLayout.addWidget(self.classificationsList)
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        sqlite_crud.get_classifications()
        self.classificationsList.clear()
        self.classificationsList.setHeaderLabels(["Classificação", "Ordem"])
        items = []
        for n in gl.classifications_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
        self.classificationsList.insertTopLevelItems(0,items)

    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Classificação:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            # if not sqlite_crud.find_duplicate('classifications', 'classification_name', text):
            sql = 'INSERT into classifications (classification_name) VALUES (?);'
            sqlite_crud.execute_query(sql, (text,))
            self.update_combo()
            self.textEdit.clear()
            # else:
            #     void = QMessageBox.warning(None, "Erro", 'Classificação Duplicada',
            #                                  QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        try:
            self.classificationsList.currentItem().text(0)
            sqlite_crud.execute_query('delete from classifications where classification_name=?', (self.classificationsList.currentItem().text(0), ))
            self.update_combo()
        except AttributeError:
            pass

    def rename_click(self):
        try:
            self.classificationsList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera Classificação:", self.classificationsList.currentItem().text(0) + " para:",
                                              QLineEdit.Normal,self.classificationsList.currentItem().text(0))
            if flag and not text == '':
                sqlite_crud.execute_query('UPDATE classifications set classification_name=? WHERE classification_name=?',
                                     (text,self.classificationsList.currentItem().text(0)))
                self.update_combo()
        except AttributeError:
            pass


    def order_click(self):
        try:
            self.classificationsList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera ordem da Classificação:", "", QLineEdit.Normal,'')
            if flag and not text == '':
                sqlite_crud.execute_query('UPDATE classifications set classification_order=? where classification_name=?',
                                     (int(text),self.classificationsList.currentItem().text(0)))
                self.update_combo()
        except AttributeError:
            pass


    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()
