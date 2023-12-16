#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
     QTreeWidget, QTreeWidgetItem
import dmPostgreSQL as dbmain
import qlib as qc
import data_access
import parameters as gl
import stdio


class PublishersBrowser(QDialog):
    def __init__(self,  parent = None):
        super(PublishersBrowser, self).__init__(parent)
        self.toto = ''
        self.setWindowTitle('Editores(as)')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.publishersList = QTreeWidget()
        self.publishersList.setColumnWidth(0, 200)
        self.searchEdt = QLineEdit()
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)
        
        validateBtn = QPushButton('Valida')
        validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qc.addHLayout([validateBtn,renameBtn,exitBtn]))
        masterLayout.addWidget(self.publishersList)
        self.update_combo()
        
    def update_combo(self):
        data_access.get_publishers()
        self.publishersList.clear()
        self.publishersList.setHeaderLabels(["Editor(a)"])
        items = []
        for n in gl.publishers_tuple:
            item = QTreeWidgetItem([n[0]])
            items.append(item)
        self.publishersList.insertTopLevelItems(0, items)

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome de(a) Editor(a):", self.publishersList.currentItem().text(0) + ' para :', QLineEdit.Normal,self.publishersList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query("UPDATE livros set pu_publisher=%s WHERE pu_publisher=%s;",
                                 (text,self.publishersList.currentItem().text(0)))
            self.update_combo()

    def validate_click(self):
        self.toto = self.publishersList.currentItem().text(0)
        self.close()
    
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
    form = PublishersBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
