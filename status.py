#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
      QTreeWidget, QTreeWidgetItem

import qlib as qc
import parameters as gl
import sqlite_crud
import stdio


class StatusBrowser(QDialog):
    def __init__(self,  parent = None):
        super(StatusBrowser, self).__init__(parent)
        self.setWindowTitle('Estados das Publicações')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.statusList = QTreeWidget()
        self.statusList.setColumnWidth(0, 200)
        
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
        masterLayout.addWidget(self.statusList)
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        sqlite_crud.get_status()
        self.statusList.clear()
        self.statusList.setHeaderLabels(["Estado", "Ordem"])
        items = []
        for n in gl.status_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
        self.statusList.insertTopLevelItems(0, items)

    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Estado:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            # if not sqlite_crud.find_duplicate('status', 'status_name', text):
            sql = 'INSERT into status (status_name) VALUES (?);'
            sqlite_crud.execute_query(sql, (text,))
            self.update_combo()
            self.textEdit.clear()
            # else:
            #     void = QMessageBox.warning(None, "Erro", 'Estado Duplicado',
            #                                  QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        try:
            self.statusList.currentItem().text(0)
            sqlite_crud.execute_query('delete from status where status_name=?', (self.statusList.currentItem().text(0),))
            self.update_combo()
        except AttributeError:
            pass
        
    def rename_click(self):
        try:
            self.statusList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera nome da Estado:", self.statusList.currentItem().text(0) + " para:", QLineEdit.Normal,self.statusList.currentItem().text(0))
            if flag and not text == '':
                sqlite_crud.execute_query('UPDATE status set status_name=? WHERE status_name=?',
                                     (text,self.statusList.currentItem().text(0)))
                self.update_combo()
        except AttributeError:
            pass

    def order_click(self):
        try:
            self.statusList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera ordem da Estado:", "", QLineEdit.Normal,'')
            if flag and not text == '':
                sqlite_crud.execute_query('UPDATE status set status_order=? where status_name=?',
                                     (int(text),self.statusList.currentItem().text(0)))
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
    # sqlite_crud.get_status()
    app = QApplication(sys.argv)
    form = StatusBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
