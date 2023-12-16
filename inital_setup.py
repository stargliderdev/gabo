#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTableWidget, QDialog, QApplication, QLabel, QLineEdit, \
    QFileDialog, QTextEdit, QInputDialog, QMessageBox

import database_init
import ex_grid

import qlib as qc
import parameters as gl
import settings
import sqlite_crud
import stdio


class InitialSetupDialog(QDialog):
    def __init__(self, status_db=True, parent=None):
        super(InitialSetupDialog, self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.resize(600, 400)
        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon('./img/settings.png'))
        masterLayout = QVBoxLayout(self)
        self.infoLabel = QLabel()
        self.infoLabel.setText('Não foi encontrada nenhuma Base de Dados!')
        masterLayout.addWidget(self.infoLabel)

        self.setDatabaseBtn = QPushButton('...')

        createBtn = QPushButton('Criar')
        createBtn.clicked.connect(self.create_database)
        masterLayout.addWidget(createBtn)

        masterLayout.addStretch()
        exit_btn = QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)

        valid_btn = QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)

        masterLayout.addLayout(qc.addHLayout([valid_btn, exit_btn]))
        gl.DOCUMENTS_DIR = os.path.expanduser('~\\Documents')
        # print('Documentos:' + gl.DOCUMENTS_DIR)

    def create_database(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, 'Directory', gl.DOCUMENTS_DIR, options=options)
        flag = False
        if directory:
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'File name:')
            if ok:
                gl.DB_PATH = directory + '/'
                text = text.replace(' ', '_')
                gl.DB_FILE = text.replace('.', '_') + '.sqlite3'
                if stdio.file_ok(gl.DB_PATH + gl.DB_FILE):
                    ask = QMessageBox.warning(None,
                                           "Duplicado",
                                           """Atenção\n estabase de dados já existe! \nEscrever por cima? """,
                                           QMessageBox.StandardButtons(QMessageBox.Cancel | QMessageBox.Yes),
                                           QMessageBox.Cancel)
                    if ask == QMessageBox.Yes:
                        flag = True
                else:
                    flag = True
        if flag :
            database_init.create_database()
            void = QMessageBox.warning(None, "Sucesso", 'A Base de Dados ' + gl.DB_FILE + ' foi criada!\nem ' + gl.DB_PATH,
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
        else:
            void = QMessageBox.warning(None, "Erro", 'A Base de Dados não foi criada!',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def valid_click(self):
        settings.save_settings()
        self.close()

    def set_database_click(self):
        pass

    def exit_click(self):
        self.close()



def main():
    app = QApplication(sys.argv)
    form = InitialSetupDialog()
    form.show()
    app.exec_()


if __name__ == '__main__':

    main()
