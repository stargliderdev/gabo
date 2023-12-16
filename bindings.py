#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
try:
    from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog, QInputDialog, \
        QComboBox,  QTreeWidget, QTreeWidgetItem
except ModuleNotFoundError:
    pass
import qlib as qc
import sqlite_crud
import parameters as gl


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
        sqlite_crud.get_covers()
        self.bindingsCbx.clear()
        self.bindingsCbx.addItems(gl.covers_list)
        self.bindingsList.clear()
        self.bindingsList.setHeaderLabels(["Encadernação", "Ordem"])
        items = []
        for n in gl.covers_tuple:
            item = QTreeWidgetItem([n[0], str(n[1])])
            items.append(item)
        self.bindingsList.insertTopLevelItems(0,items)

    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Encadernação:", "", QLineEdit.Normal, '')
        if flag and not text == '':
            # if not dbmain.find_duplicate('bindings', 'binding_name', text):
            sql = 'insert into covers (cover_name) VALUES (?);'
            sqlite_crud.execute_query(sql, (text,))
            self.update_combo()
            self.textEdit.clear()
            # else:
            #     result = QMessageBox.warning(None, "Erro", 'Encadernação Duplicada',
            #                                  QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        try:
            self.bindingsList.currentItem().text(0)
            sqlite_crud.execute_query('delete from covers where cover_name=?', (self.bindingsList.currentItem().text(0), ))
            self.update_combo()
        except AttributeError:
            pass

    def rename_click(self):
        try:
            old_cover = self.bindingsList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera Nome", self.bindingsList.currentItem().text(0) + " para:", QLineEdit.Normal,self.bindingsList.currentItem().text(0))
            if flag and not text == '':
                sqlite_crud.execute_query('delete from covers where cover_name=?', (old_cover, ))
                sqlite_crud.execute_query('update covers set cover_name=? where cover_name=?',(text,old_cover))
                sqlite_crud.execute_query('update books set pu_cover=? where pu_cover=?',(text,old_cover))
                self.update_combo()
        except AttributeError:
            pass

    def order_click(self):
        try: 
            self.bindingsList.currentItem().text(0)
            text, flag = QInputDialog.getText(None, "Altera ordem do Encadernação:", "", QLineEdit.Normal,'')
            if flag and not text == '':
                sqlite_crud.execute_query('update covers set cover_order=? where cover_name=?', (int(text),self.bindingsList.currentItem().text(0)))
                self.update_combo()
        except AttributeError:
            pass
        
    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass


if __name__ == '__main__':
    main()
