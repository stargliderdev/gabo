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


class CollectionBrowser(QDialog):
    def __init__(self,  parent = None):
        super(CollectionBrowser, self).__init__(parent)
        self.toto = ''
        self.setWindowTitle('Colecções')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.collectionList = QTreeWidget()
        self.collectionList.setColumnWidth(0, 200)
        self.searchEdt = QLineEdit()
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)
        
        validateBtn = QPushButton('Valida')
        validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qc.addHLayout([validateBtn,renameBtn,exitBtn]))
        masterLayout.addWidget(self.collectionList)
        self.update_combo()
        
    def update_combo(self):
        data_access.get_collections()
        self.collectionList.clear()
        self.collectionList.setHeaderLabels(["Colecção"])
        items = []
        for n in gl.collections_tuple:
            item = QTreeWidgetItem([n[0]])
            items.append(item)
        self.collectionList.insertTopLevelItems(0, items)

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome da Colecção:", self.collectionList.currentItem().text(0) + ' para :', QLineEdit.Normal,self.collectionList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query("UPDATE livros set pu_collection=%s WHERE pu_collection=%s;",
                                 (text,self.collectionList.currentItem().text(0)))
            self.update_combo()

    def validate_click(self):
        self.toto = self.collectionList.currentItem().text(0)
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
    form = CollectionBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
