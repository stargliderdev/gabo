#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QComboBox, QMessageBox, QTreeWidget, QTreeWidgetItem
import dmPostgreSQL as dbmain
import qlib as qc
import data_access
import parameters as gl
import stdio


class ConditionsBrowser(QDialog):
    def __init__(self,  parent = None):
        super(ConditionsBrowser,  self).__init__(parent)
        self.setWindowTitle('Estado Fisico')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.conditionsCbx = QComboBox()
        self.conditionsList = QTreeWidget()
        self.conditionsList.setColumnWidth(0,200)
        
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
        masterLayout.addWidget(self.conditionsList)
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        data_access.get_conditions()
        self.conditionsList.clear()
        self.conditionsList.setHeaderLabels(["Estado Fisico", "Ordem"])
        items = []
        for n in gl.conditions_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
        self.conditionsList.insertTopLevelItems(0,items)

    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Estado Fisico:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            if not dbmain.find_duplicate('conditions', 'condition_name', text):
                sql = 'INSERT into conditions (condition_name) VALUES (%s);'
                dbmain.execute_query(sql, (text,))
                self.update_combo()
                self.textEdit.clear()
            else:
                void = QMessageBox.warning(None, "Erro", 'Estado Fisico Duplicado',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        dbmain.execute_query('delete from conditions where condition_name=%s', (self.conditionsList.currentItem().text(0), ))
        self.update_combo()

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome do Estado Fisico:", self.conditionsList.currentItem().text(0) +"para:", QLineEdit.Normal,self.conditionsList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query('UPDATE conditions set condition_name=%s WHERE condition_name=%s',
                                 (text,self.conditionsList.currentItem().text(0)))
            self.update_combo()

    def order_click(self):
        text, flag = QInputDialog.getText(None, "Altera ordem do Estado Fisico:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('UPDATE conditions set condition_order=%s where condition_name=%s',
                                 (int(text),self.conditionsList.currentItem().text(0)))
            self.update_combo()

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    data_access.get_conditions()
    app = QApplication(sys.argv)
    form = ConditionsBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
