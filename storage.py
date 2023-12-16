#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, \
    QTableWidgetItem, QWidget, QCheckBox, QStyleFactory, QToolButton
from PyQt5.Qt import Qt
import locals
import edit_record
import lib_gabo
import qlib as qc


class StoreMangDialog(QDialog):
    def __init__(self, parent=None):
        super(StoreMangDialog, self).__init__(parent)
        self.resize(1024, 768)
        self.setWindowTitle('Analise de Arrumação')
        self.storageGrid = QTableWidget()
        self.storageGrid.verticalHeader().setDefaultSectionSize(20)
        self.storageGrid.setSelectionBehavior(QTableWidget.SelectRows)
        # self.storageGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.storageGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.storageGrid.setAlternatingRowColors(True)
        self.storageGrid.setStyleSheet("alternate-background-color: #e6f2ff;")
        self.storageGrid.setColumnCount(9)
        self.storageGrid.verticalHeader().setVisible(False)
        self.storageGrid.setHorizontalHeaderLabels(
            ['ID', 'Titulo', 'Autor', 'Ano', 'Volume', 'Dim.', 'Obs', 'Local', 'Novo Local'])
        self.storageGrid.horizontalHeader().setVisible(True)
        self.storageGrid.doubleClicked.connect(self.grid_double_click)
        
        masterLayout = QVBoxLayout(self)
        localsBtn = QToolButton()
        localsBtn.setToolTip('locals Locais')
        localsBtn.setIcon(QIcon('./img/locals.png'))
        localsBtn.clicked.connect(self.locals_click)
        
        self.toLocalEdt = QLineEdit()
        addNewLocalBtn = QPushButton('Atribui')
        addNewLocalBtn.clicked.connect(self.set_new_local_click)
        storeTempBtn = QPushButton('Grava Previsão')
        storeTempBtn.clicked.connect(self.record_in_temp)
        masterLayout.addLayout(qc.addHLayout(['Para', self.toLocalEdt, addNewLocalBtn, localsBtn, storeTempBtn, True]))
        self.widthEdt = QLineEdit()
        self.lenghtEdt = QLineEdit()
        self.depthEdt = QLineEdit()
        self.noDimEdt = QLineEdit()
        self.noDimEdt.setMaximumWidth(40)
        self.noDimEdt.setAlignment(Qt.AlignRight)
        self.withDimEdt = QLineEdit()
        self.withDimEdt.setMaximumWidth(40)
        self.withDimEdt.setAlignment(Qt.AlignRight)
        masterLayout.addLayout(qc.addHLayout(['Comprimento', self.widthEdt, 'Altura', self.lenghtEdt,
                                              'Largura', self.depthEdt, 'Sem Dimensões', self.noDimEdt,
                                              'Com Dimensões', self.withDimEdt]))
        masterLayout.addWidget(self.storageGrid)
        
        btnLayout = QHBoxLayout()
        # btnLayout.addWidget(self.sendBtn)
        cancelBtn = QPushButton('Sair')
        cancelBtn.clicked.connect(self.cancel_click)
        btnLayout.addWidget(cancelBtn)
        masterLayout.addLayout(btnLayout)
        self.update_grid()
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        # lib_gabo.calc_width_in_filter()
    
    def update_grid(self):
        dum = lib_gabo.calc_width_in_filter()
        self.refresh_sizes(dum[1])
        hl = dum[0]
        self.storageGrid.setRowCount(len(hl))
        line = 0
        for n in hl:
            item = QTableWidgetItem()
            item.setText(str(n[0]))
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.storageGrid.setItem(line, 0, item)
            item = QTableWidgetItem()
            item.setText(n[1])
            self.storageGrid.setItem(line, 1, item)
            item = QTableWidgetItem()
            item.setText(n[2])
            self.storageGrid.setItem(line, 2, item)
            if n[3] is None:
                pass
            else:
                item = QTableWidgetItem()
                item.setText(str(n[3]))
                self.storageGrid.setItem(line, 3, item)
            item = QTableWidgetItem()
            item.setText(str(n[4]))
            self.storageGrid.setItem(line, 4, item)
            item = QTableWidgetItem()
            item.setText(str(n[7]))
            self.storageGrid.setItem(line, 5, item)
            item = QTableWidgetItem()
            item.setText(n[8])
            self.storageGrid.setItem(line, 6, item)
            item = QTableWidgetItem()
            item.setText(n[5])
            self.storageGrid.setItem(line, 7, item)
            item = QTableWidgetItem()
            item.setText(n[6])
            self.storageGrid.setItem(line, 8, item)
            line += 1
        self.storageGrid.setColumnWidth(0, 40)
        self.storageGrid.setColumnWidth(1, 310)
        self.storageGrid.setColumnWidth(2, 200)
        self.storageGrid.setColumnWidth(3, 50)
        self.storageGrid.setColumnWidth(4, 60)
        self.storageGrid.setColumnWidth(5, 100)
        self.storageGrid.setColumnWidth(6, 0)
        self.storageGrid.setColumnWidth(7, 100)
        self.storageGrid.setColumnWidth(8, 100)
    
    def refresh_sizes(self, data_dict):
        self.widthEdt.setText(str(data_dict['width']) + ' mm/' + str(data_dict['width'] / 10.0) + ' cm')
        self.lenghtEdt.setText(str(data_dict['height']) + ' mm/' + str(data_dict['height'] / 10.0) + ' cm')
        self.depthEdt.setText(str(data_dict['depth']) + ' mm/' + str(data_dict['depth'] / 10.0) + ' cm')
        self.noDimEdt.setText(str(data_dict['no_dim']))
        self.withDimEdt.setText(str(data_dict['depth']))
    
    def validate(self):
        pass
    
    def cancel_click(self):
        self.close()
    
    def grid_double_click(self):
        form = edit_record.EditRecord(int(self.storageGrid.item(self.storageGrid.currentRow(), 0).text()), draft_data=False)
        form.exec_()
        self.update_grid()
    
    def set_new_local_click(self):
        for idx in self.storageGrid.selectionModel().selectedRows():
            self.storageGrid.item(idx.row(), 8).setText(self.toLocalEdt.text())
    
    def record_in_temp(self):
        t = ()
        for idx in self.storageGrid.selectionModel().selectedRows():
            new = self.storageGrid.item(idx.row(), 8).text()
            t += (int(self.storageGrid.item(idx.row(), 0).text()),)
            print(idx.row(), '@', new)
        sql = 'update livros set pu_local_new = ? where pu_id in ' + str(t)
        libpg.execute_query(sql, (new,))
    
    def locals_click(self):
        form = locals.BrowserLocals()
        form.exec_()
        if not form.toto == '':
            self.toLocalEdt.setText(form.toto)


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
