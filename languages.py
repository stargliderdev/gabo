#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QComboBox,  QTreeWidget, QTreeWidgetItem

import qlib as qc
import sqlite_crud
import parameters as gl
import stdio


class LanguagesBrowser(QDialog):
    def __init__(self,  parent = None):
        super(LanguagesBrowser,  self).__init__(parent)
        # self.resize(600, 400)
        self.setWindowTitle('Idiomas')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.languagesCbx = QComboBox()
        self.languagesList = QTreeWidget()
        self.languagesList.setColumnWidth(0,200)
        
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
        masterLayout.addWidget(self.languagesList)
        # masterLayout.addLayout(qc.addHLayout([self.languagesCbx]))
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        sqlite_crud.get_languages()
        self.languagesCbx.clear()
        self.languagesCbx.addItems(gl.languages_list)
        self.languagesList.clear()
        self.languagesList.setHeaderLabels(["Idioma", "Ordem"])
        items = []
        for n in gl.languages_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
        self.languagesList.insertTopLevelItems(0,items)


    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Idioma:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            # if not dbmain.find_duplicate('languages', 'language_name', text):
            sql = 'insert into languages (language_name) VALUES (?);'
            sqlite_crud.execute_query(sql, (text,))
            self.update_combo()
            self.textEdit.clear()
            # else:
            #     result = QMessageBox.warning(None, "Erro", 'Idioma Duplicado',
            #                                  QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        try:
            self.languagesList.currentItem().text(0)
            sqlite_crud.execute_query('delete from languages where language_name=?', (self.languagesList.currentItem().text(0), ))
            self.update_combo()
        except AttributeError:
            pass
        
    def rename_click(self):
        try:
            self.languagesList.currentItem().text(0)
            old_text, flag = QInputDialog.getText(None, "Altera nome do Idioma:",
                                              self.languagesList.currentItem().text(0) + " para:", QLineEdit.Normal,self.languagesList.currentItem().text(0))
            if flag and not old_text == '':
                # sqlite_crud.execute_query('update languages set language_name=? where language_name=?', (text,self.languagesList.currentItem().text(0)))
                sqlite_crud.execute_query('update books set pu_language=? where pu_language=?', (old_text,self.languagesList.currentItem().text(0)))
                # apaga a linguagem antiga
                sqlite_crud.execute_query('delete from languages where language_name=?', (self.languagesList.currentItem().text(0),))
                self.update_combo()
        except AttributeError:
            pass

    def order_click(self):
        try:
            self.languagesList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera ordem do Idioma:", "", QLineEdit.Normal,'')
            if flag and not text == '':
                sqlite_crud.execute_query('update languages set language_order=? where language_name=?',
                                     (int(text),self.languagesList.currentItem().text(0)))
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
    sqlite_crud.get_languages()
    app = QApplication(sys.argv)
    form = LanguagesBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
