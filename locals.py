#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QTableWidget, QPushButton, QDialog, QMessageBox

import ex_grid

import qlib as qc
import sqlite_crud


class BrowserLocals(QDialog):
    def __init__(self,  parent = None):
        super(BrowserLocals,  self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle('Locais')
        self.setWindowIcon(QIcon('./img/locals.png'))
        self.toto = ''
        masterLayout = QVBoxLayout(self)
        self.grid = QTableWidget()
        self.grid.setSelectionBehavior(QTableWidget.SelectRows)
        self.grid.setSelectionMode(QTableWidget.SingleSelection)

        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.verticalHeader().setDefaultSectionSize(20)
        self.grid.verticalHeader().setVisible(False)
        self.grid.itemDoubleClicked.connect(self.valid_click)
        masterLayout.addWidget(self.grid)
        self.fromEdt = QLineEdit()
        self.toEdt = QLineEdit()
        changeBtn = QPushButton('Altera')
        changeBtn.clicked.connect(self.change_locals_click)
        exit_btn=QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        valid_btn=QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)
        masterLayout.addLayout(qc.addHLayout(['Do local:', self.fromEdt, 'Para o local:', self.toEdt, changeBtn]))
        masterLayout.addLayout(qc.addHLayout([valid_btn,exit_btn]))

        self.grid_refresh()

    def change_locals_click(self):
        # check souce local exists
        source = self.fromEdt.text().upper()
        target = self.toEdt.text().upper().replace(' ', '')
        # sql = '''select count(pu_local) from books where pu_local = ?'''
        b = QMessageBox.question(self,
                self.tr("Alterar Localização"),
                '''Vou alterar a Localização das Publicações\n''' + '''do local ''' + source + ''' para o local''' + target,
                QMessageBox.StandardButtons(
                    QMessageBox.No |
                    QMessageBox.Yes),
                QMessageBox.No)
        if b == QMessageBox.No:
            pass
        else:
            sql = '''select count(pu_local) from books where upper(pu_local) = ''' + '''\'''' + source + '''\''''
            total_changed = sqlite_crud.query_many(sql)[0][0]
            sql = '''UPDATE books set pu_local=? where pu_local=?'''
            sqlite_crud.execute_query(sql, (target, source))
            QMessageBox.information(None, 'Alterado o local' , 'Foram alterados o local em ' + str(total_changed) + ' publicações.' ,
                                   QMessageBox.StandardButtons(QMessageBox.Cancel |QMessageBox.Ok), QMessageBox.Ok)
            self.grid_refresh()

    def valid_click(self):
        self.toto = self.grid.item(self.grid.currentRow(), 0).text()
        self.close()

    def grid_refresh(self):
        sql = '''select pu_local, count(pu_local)
                  from books
            group by pu_local
            order by pu_local'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.grid, {0:['local', 's'],1:['Livros','i']}, dataset)
        self.grid.setColumnWidth(0, 200)
        self.grid.setColumnWidth(1, 60)


    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()

