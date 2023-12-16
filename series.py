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


class SeriesBrowser(QDialog):
    def __init__(self,  parent = None):
        super(SeriesBrowser, self).__init__(parent)
        self.toto = ''
        self.setWindowTitle('Séries')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.seriesList = QTreeWidget()
        self.seriesList.setColumnWidth(0, 200)
        self.searchEdt = QLineEdit()
       
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)
        
        validateBtn = QPushButton('Valida')
        validateBtn.clicked.connect(self.validate_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qc.addHLayout([validateBtn,renameBtn,exitBtn]))
        masterLayout.addWidget(self.seriesList)
        self.update_combo()
        
    def update_combo(self):
        data_access.get_series()
        self.seriesList.clear()
        self.seriesList.setHeaderLabels(["Série"])
        items = []
        for n in gl.series_tuple:
            item = QTreeWidgetItem([n[0]])
            items.append(item)
        self.seriesList.insertTopLevelItems(0, items)

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome da Colecção:", self.seriesList.currentItem().text(0) + ' para :', QLineEdit.Normal,self.seriesList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query("UPDATE livros set pu_series_name=%s WHERE pu_series_name=%s;",
                                 (text,self.seriesList.currentItem().text(0)))
            self.update_combo()

    def validate_click(self):
        self.toto = self.seriesList.currentItem().text(0)
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
    form = SeriesBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
