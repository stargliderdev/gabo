#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QDialog, QApplication,  QTableWidget, QVBoxLayout, QLineEdit,  QPushButton, QHBoxLayout, \
    QTableWidgetItem, QWidget, QCheckBox, QStyleFactory

import edit_record
import lib_gabo

class StoreMangDialog(QDialog):
    def __init__(self,  parent=None):
        super(StoreMangDialog, self).__init__(parent)
        self.resize(1024, 768)
        self.setWindowTitle('Analise de Arrumação')
        self.storageGrid = QTableWidget()
        self.storageGrid.verticalHeader().setDefaultSectionSize(20)
        self.storageGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.storageGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.storageGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.storageGrid.setAlternatingRowColors(True)
        self.storageGrid.setStyleSheet("alternate-background-color: #e6f2ff;")
        self.storageGrid.setColumnCount(7)
        self.storageGrid.verticalHeader().setVisible(False)
        self.storageGrid.setHorizontalHeaderLabels(['ID','Titulo', 'Autor','Dimensões','Volume','Ano','Local'])
        self.storageGrid.horizontalHeader().setVisible(True)
        self.storageGrid.doubleClicked.connect(self.grid_double_click)
        
        masterLayout = QVBoxLayout(self)
        masterLayout.addWidget(self.storageGrid)
        self.toEdt = QLineEdit()
        
        # self.sendBtn = QPushButton('Envia')
        # self.sendBtn.clicked.connect(self.send_click)
        
        btnLayout = QHBoxLayout()
        # btnLayout.addWidget(self.sendBtn)
        cancelBtn = QPushButton('Sair')
        cancelBtn.clicked.connect(self.cancel_click)
        btnLayout.addWidget(cancelBtn)
        masterLayout.addLayout(btnLayout)
        self.refresh_grid()
        QApplication.setStyle(QStyleFactory.create('Fusion'))
    
    def refresh_grid(self):
        hl = lib_gabo.calc_width_in_filter()
        self.storageGrid.setRowCount(len(hl))
        line = 0
        for n in hl:
            item = QTableWidgetItem()
            item.setText(str(n[0]))
            self.storageGrid.setItem(line, 0, item)
            item = QTableWidgetItem()
            item.setText(n[1])
            self.storageGrid.setItem(line, 1, item)
            item = QTableWidgetItem()
            item.setText(n[2])
            self.storageGrid.setItem(line, 2, item)
            item = QTableWidgetItem()
            item.setText(n[6])
            self.storageGrid.setItem(line, 3, item)
            item = QTableWidgetItem()
            item.setText(str(n[4]))
            self.storageGrid.setItem(line, 4, item)
            item = QTableWidgetItem()
            item.setText(str(n[5]))
            self.storageGrid.setItem(line, 5, item)
            item = QTableWidgetItem()
            item.setText(n[3])
            self.storageGrid.setItem(line, 6, item)
            line += 1
        self.storageGrid.setColumnWidth(0, 10)
        self.storageGrid.setColumnWidth(1, 310)
        self.storageGrid.setColumnWidth(2, 280)
        self.storageGrid.setColumnWidth(3, 100)
        self.storageGrid.setColumnWidth(4, 20)
        self.storageGrid.setColumnWidth(5, 20)
        self.storageGrid.setColumnWidth(6, 50)
    
    
    def validate(self):
        pass
    def cancel_click(self):
        self.close()
    
    def grid_double_click(self):
        form = edit_record.EditRecord(int(self.storageGrid.item(self.storageGrid.currentRow(), 0).text()), '', draft_data=False)
        form.exec_()
    

def checkBoxGrid(label=''):
    w = QWidget()
    l = QHBoxLayout(w)
    l.setContentsMargins(0, 0, 0, 0)
    l.addStretch()
    c = QCheckBox(label)
    l.addWidget(c)
    l.addStretch()
    return w


def main():
    app = QApplication(sys.argv)
    form = StoreMangDialog()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
    # log_message({'type': 2, 'msg_to': '98938890', 'msg_subject': '', 'msg_body': 'teste de mensagem', 'msg_files': ''})
