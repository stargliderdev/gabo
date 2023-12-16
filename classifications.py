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
        data_access.get_classifications()
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
            if not dbmain.find_duplicate('classifications', 'classification_name', text):
                sql = 'INSERT into classifications (classification_name) VALUES (%s);'
                dbmain.execute_query(sql, (text,))
                self.update_combo()
                self.textEdit.clear()
            else:
                void = QMessageBox.warning(None, "Erro", 'Classificação Duplicada',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        dbmain.execute_query('delete from classifications where classification_name=%s', (self.classificationsList.currentItem().text(0), ))
        self.update_combo()

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera Classificação:", self.classificationsList.currentItem().text(0) + " para:",
                                          QLineEdit.Normal,self.classificationsList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query('UPDATE classifications set classification_name=%s WHERE classification_name=%s',
                                 (text,self.classificationsList.currentItem().text(0)))
            self.update_combo()

    def order_click(self):
        text, flag = QInputDialog.getText(None, "Altera ordem da Classificação:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('UPDATE classifications set classification_order=%s where classification_name=%s',
                                 (int(text),self.classificationsList.currentItem().text(0)))
            self.update_combo()

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    data_access.get_classifications()
    app = QApplication(sys.argv)
    form = ClassificationsBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
