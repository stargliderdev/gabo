#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QTableWidget, QPushButton, QDialog, QMessageBox

import ex_grid
import dmPostgreSQL as dbmain
import qlib as qc


class BrowserLocals(QDialog):
    def __init__(self,  parent = None):
        super(BrowserLocals,  self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle('Locais')
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
        masterLayout.addLayout(qc.addHLayout(['Da cota:', self.fromEdt, 'Para a cota:', self.toEdt, changeBtn]))
        masterLayout.addLayout(qc.addHLayout([valid_btn,exit_btn]))

        self.grid_refresh()

    def change_locals_click(self):
        # check souce local exists
        sql = '''select count(pu_cota) from livros where pu_cota = %s'''
       
        a = dbmain.query_one(sql, (self.fromEdt.text().upper(),))
        flag = True
        if not a[0] > 0:
            print('sem source')
            b = QMessageBox.question(
                self,
                self.tr("Cota inisistente"),
                self.tr("""A Cota de origem não existe!
            Continuar?"""),
                QMessageBox.StandardButtons(
                    QMessageBox.No |
                    QMessageBox.Yes),
                QMessageBox.No)
            if b == QMessageBox.No:
                flag == False
        if flag:
            sql = '''UPDATE livros set pu_cota=%s where pu_cota=%s'''
            dbmain.execute_query(sql, ( self.toEdt.text().upper(),self.fromEdt.text().upper()))
            self.grid_refresh()

    def valid_click(self):
        self.toto = self.grid.item(self.grid.currentRow(), 1).text()
        self.close()

    def grid_refresh(self):
        sql = '''select pu_cota, count(pu_cota)
                  from livros
            group by pu_cota
            order by pu_cota'''
        dataset = dbmain.query_many(sql)
        ex_grid.ex_grid_update (self.grid, {0:['Cota', 's'],1:['Livros','i']}, dataset)
        self.grid.setColumnWidth(0, 200)
        self.grid.setColumnWidth(1, 60)


    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    pass

if __name__ == '__main__':
    main()

