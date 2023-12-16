#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
     QMessageBox, QTreeWidget, QTreeWidgetItem
import dmPostgreSQL as dbmain
import qlib as qc
import data_access
import parameters as gl
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
        data_access.get_status()
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
            if not dbmain.find_duplicate('status', 'status_name', text):
                sql = 'INSERT into status (status_name) VALUES (%s);'
                dbmain.execute_query(sql, (text,))
                self.update_combo()
                self.textEdit.clear()
            else:
                void = QMessageBox.warning(None, "Erro", 'Estado Duplicado',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        dbmain.execute_query('delete from status where status_name=%s', (self.statusList.currentItem().text(0),))
        self.update_combo()

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome da Estado:", self.statusList.currentItem().text(0) + " para:", QLineEdit.Normal,self.statusList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query('UPDATE status set status_name=%s WHERE status_name=%s',
                                 (text,self.statusList.currentItem().text(0)))
            self.update_combo()

    def order_click(self):
        text, flag = QInputDialog.getText(None, "Altera ordem da Estado:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('UPDATE status set status_order=%s where status_name=%s',
                                 (int(text),self.statusList.currentItem().text(0)))
            self.update_combo()

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    # data_access.get_status()
    app = QApplication(sys.argv)
    form = StatusBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
