#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
     QMessageBox, QTreeWidget, QTreeWidgetItem
import qlib as qc
import sqlite_crud
import parameters as gl
import stdio


class TypesBrowser(QDialog):
    def __init__(self,  parent = None):
        super(TypesBrowser, self).__init__(parent)
        # self.resize(600, 400)
        self.setWindowTitle('Tipos de Publicação')
        self.setWindowIcon(QIcon('./img/pub_types.png'))
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.typesList = QTreeWidget()
        self.typesList.setColumnWidth(0,200)
        
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
        masterLayout.addWidget(self.typesList)
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        sqlite_crud.get_types()
        self.typesList.clear()
        self.typesList.setHeaderLabels(["Tipo de Publicação", "Ordem"])
        items = []
        for n in gl.types_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
    
        self.typesList.insertTopLevelItems(0,items)


    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Tipo de Publicação:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            if not sqlite_crud.find_duplicate('types', 'ty_name', text):
                sql = 'insert into types (ty_name) VALUES (?);'
                sqlite_crud.execute_query(sql, (text,))
                self.update_combo()
                self.textEdit.clear()
            else:
                result = QMessageBox.warning(None, "Erro", 'Tipo Duplicado',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        try:
            self.typesList.currentItem().text(0)
            sqlite_crud.execute_query('delete from types where ty_name=?', (self.typesList.currentItem().text(0), ))
            self.update_combo()
        except AttributeError:
            pass


    def rename_click(self):
        try:

            old_type = self.typesList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera nome do Tipo de Publicação:",
                                              self.typesList.currentItem().text(0) + ' para:' , QLineEdit.Normal,self.typesList.currentItem().text(0))
            if flag and not text == '':
                sqlite_crud.execute_query('delete from types where ty_name=?', (old_type, ))
                sqlite_crud.execute_query('update types set ty_name=? where ty_name=?',(text,old_type))
                sqlite_crud.execute_query('update books set pu_type=? where pu_type=?',(text,old_type))
                self.update_combo()
        except AttributeError:
            pass


    def order_click(self):
        try:
            self.typesList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera ordem do Tipo de Publicação:", "", QLineEdit.Normal,'')
            if flag and not text == '':
                sqlite_crud.execute_query('update types set ty_order=? where ty_name=?',
                                     (int(text),self.typesList.currentItem().text(0)))
                self.update_combo()
        except AttributeError:
            pass

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    sqlite_crud.get_types()
    app = QApplication(sys.argv)
    form = TypesBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
