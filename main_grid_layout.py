#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
    QComboBox, QMessageBox, QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.Qt import Qt
import dmPostgreSQL as dbmain
import ex_grid
import qlib
import qlib as qc
import data_access
import parameters as gl
import stdio


class MainGridConfig(QDialog):
    def __init__(self,  parent = None):
        super(MainGridConfig, self).__init__(parent)
        self.toto = False
        self.setWindowTitle('Configurar Grelha')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.conditionsCbx = QComboBox()
        self.configGrid = QTableWidget(self)
        self.configGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.configGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.configGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.configGrid.verticalHeader().setDefaultSectionSize(20)
        self.configGrid.setAlternatingRowColors(True)
        self.configGrid.verticalHeader().setVisible(False)
        self.configGrid.setStyleSheet("alternate-background-color: #d2e5ff;")
        
        # addBtn = QPushButton('Adiciona')
        # addBtn.clicked.connect(self.add_click)
        
        # deleteBtn = QPushButton('Apaga')
        # deleteBtn.clicked.connect(self.delete_click)
        
        # renameBtn = QPushButton('Renomeia')
        # renameBtn.clicked.connect(self.rename_click)
        
        saveBtn = QPushButton('Guarda')
        self.fix_size(saveBtn)
        saveBtn.clicked.connect(self.save_click)
        
        exitBtn = QPushButton('Sair')
        self.fix_size(exitBtn)
        exitBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qc.addHLayout([ saveBtn, exitBtn, True]))
        masterLayout.addWidget(self.configGrid)
        self.update_grid()
    
    def fix_size(self, widget_control, size = 50):
        widget_control.setMaximumWidth(size)
        widget_control.setMinimumWidth(size)
        
       
    def update_grid(self):
        self.configGrid.setColumnCount(3)
        self.configGrid.setHorizontalHeaderLabels(['Visivel','Coluna','Tamanho'])
        self.configGrid.setRowCount(len(gl.GRID_COL_NAMES))
        for n in range(0,len(gl.GRID_COL_NAMES)):
            self.configGrid.setCellWidget(n, 0, qlib.checkBoxGrid())
            if gl.GRID_COLUMN_SIZES[n][1] > 0 :
                self.configGrid.cellWidget(n,0) .layout().itemAt(1).widget().setChecked(True)
            else:
                self.configGrid.cellWidget(n,0) .layout().itemAt(1).widget().setChecked(False)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item.setText(gl.GRID_COL_NAMES[n])
            self.configGrid.setItem(n, 1, item)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item.setText(str(gl.GRID_COLUMN_SIZES[n][1]))
            self.configGrid.setItem(n, 2, item)
        self.configGrid.resizeColumnsToContents()
        self.configGrid.setColumnWidth(2,0)
        
    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Estado Fisico:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            if not dbmain.find_duplicate('conditions', 'condition_name', text):
                sql = 'INSERT into conditions (condition_name) VALUES (%s);'
                dbmain.execute_query(sql, (text,))
                self.update_grid()
                self.textEdit.clear()
            else:
                void = QMessageBox.warning(None, "Erro", 'Estado Fisico Duplicado',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        dbmain.execute_query('delete from conditions where condition_name=%s', (self.conditionsList.currentItem().text(0), ))
        self.update_grid()

    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome do Estado Fisico:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('UPDATE conditions set condition_name=%s WHERE condition_name=%s',
                                 (text,self.conditionsList.currentItem().text(0)))
            self.update_grid()

    def save_click(self):
        gl.GRID_COLUMN_SIZES = []
        for n in range(0,len(gl.GRID_COL_NAMES)):
            if self.configGrid.cellWidget(n, 0).layout().itemAt(1).widget().isChecked():  # .isChecked(): #  foi ticado
                if int(self.configGrid.item(n, 2).text()) == 0:
                    gl.GRID_COLUMN_SIZES.append((n,40))
                else:
                    gl.GRID_COLUMN_SIZES.append((n, int(self.configGrid.item(n, 2).text())))
            else:
                gl.GRID_COLUMN_SIZES.append((n,0))
        data_access.save_parameters('GRID_COLUMN_SIZES', str(gl.GRID_COLUMN_SIZES))
        data_access.load_parameters()
        self.toto = True
        self.close()

    def exit_click(self):
        self.toto = False
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    data_access.load_parameters()
    app = QApplication(sys.argv)
    form = MainGridConfig()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
