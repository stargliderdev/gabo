#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QMessageBox, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout
import dmPostgreSQL as dbmain
import qlib as qc
import data_access
import parameters as gl
import stdio


class DimentionsUI(QDialog):
    def __init__(self,  parent = None):
        super(DimentionsUI, self).__init__(parent)
        self.setWindowTitle('Dimensções')
        masterLayout = QHBoxLayout(self)
        self.textEdit = QLineEdit()
        self.classificationsList = QTreeWidget()
        self.classificationsList.setColumnWidth(0,200)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QtGui.QPixmap("./img/dimentionsUI.png"))
        self.imageLabel.show()
        
        self.dimentiosEdt = QLineEdit()
        # addBtn = QPushButton('Adiciona')
        # addBtn.clicked.connect(self.add_click)
        
        deleteBtn = QPushButton('Apaga')
        # deleteBtn.clicked.connect(self.delete_click)
        
        renameBtn = QPushButton('Renomeia')
        # renameBtn.clicked.connect(self.rename_click)
        
        orderBtn = QPushButton('Ordem')
        # orderBtn.clicked.connect(self.save_click)
        
        exitBtn = QPushButton('Sair')
        exitBtn.setMinimumWidth(400)
        exitBtn.clicked.connect(self.exit_click)
        masterLayout.addWidget(self.imageLabel)
        masterLayout.addLayout(qc.addVLayout([self.dimentiosEdt,True, deleteBtn,exitBtn]))
        



    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    # gl.db_params = stdio.read_config_file('gabo.ini')
    # gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
    #     'db_database'] + \
    #                  ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    # data_access.get_classifications()
    app = QApplication(sys.argv)
    form = DimentionsUI()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
