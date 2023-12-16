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


class BindingsBrowser(QDialog):
    def __init__(self,  parent = None):
        super(BindingsBrowser, self).__init__(parent)
        # self.resize(600, 400)
        self.setWindowTitle('Encadernações')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.bindingsCbx = QComboBox()
        self.bindingsList = QTreeWidget()
        self.bindingsList.setColumnWidth(0,200)
        
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
        masterLayout.addWidget(self.bindingsList)
        # masterLayout.addLayout(qc.addHLayout([self.bindingsCbx]))
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        data_access.get_bindings()
        self.bindingsCbx.clear()
        self.bindingsCbx.addItems(gl.bindings_list)
        self.bindingsList.clear()
        self.bindingsList.setHeaderLabels(["Encadernação", "Ordem"])
        items = []
        for n in gl.bindings_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
    
        self.bindingsList.insertTopLevelItems(0,items)


    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Encadernação:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            if not dbmain.find_duplicate('bindings', 'binding_name', text):
                sql = 'insert into bindings (binding_name) VALUES (%s);'
                dbmain.execute_query(sql, (text,))
                self.update_combo()
                self.textEdit.clear()
            else:
                result = QMessageBox.warning(None, "Erro", 'Encadernação Duplicada',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        dbmain.execute_query('delete from bindings where binding_name=%s', (self.bindingsList.currentItem().text(0), ))
        self.update_combo()

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera Nome", self.bindingsList.currentItem().text(0) + " para:", QLineEdit.Normal,self.bindingsList.currentItem().text(0))
        if flag and not text == '':
            dbmain.execute_query('update bindings set binding_name=%s where binding_name=%s',
                                 (text,self.bindingsList.currentItem().text(0)))
            self.update_combo()

    def order_click(self):
        text, flag = QInputDialog.getText(None, "Altera ordem do Encadernação:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('update bindings set binding_order=%s where binding_name=%s',
                                 (int(text),self.bindingsList.currentItem().text(0)))
            self.update_combo()

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    data_access.get_bindings()
    app = QApplication(sys.argv)
    form = BindingsBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
