#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTableWidget, QDialog, QApplication, QLabel, QLineEdit, \
    QFileDialog, QTextEdit, QMessageBox, QInputDialog, QTabWidget, QWidget

import database_init
import qlib as qc
import parameters as gl
import sqlite_crud
import stdio

class EditGlobalSettings(QDialog):
    def __init__(self, status_db=True, parent=None):
        super(EditGlobalSettings, self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.resize(600, 400)
        self.setWindowTitle('Configuração')
        self.setWindowIcon(QIcon('./img/settings.png'))
        gl.STACK_DB_PATH = gl.DB_PATH
        gl.STACK_DB_NAME = gl.DB_FILE
        self.status_db = status_db
        mainLayout = QVBoxLayout(self)
        self.tabuladorTabWidget = QTabWidget()
        self.make_db_tab()
        self.make_settings_tab()
        self.tabuladorTabWidget.addTab(self.tabDatabase, 'Base de dados')
        self.tabuladorTabWidget.addTab(self.tabSettings, 'Configurações')
        mainLayout.addWidget(self.tabuladorTabWidget)

        self.tabuladorTabWidget.addTab(self.tabDatabase, 'Principal')
        self.tabuladorTabWidget.addTab(self.tabSettings, 'Outros')

    def make_settings_tab(self):
        self.tabSettings = QWidget()
        settingsLayout = QVBoxLayout(self.tabSettings)
        dumLayout = QVBoxLayout()
        settingsLayout.addLayout(dumLayout)

    def make_db_tab(self):
        self.tabDatabase = QWidget()
        databaseLayout = QVBoxLayout(self.tabDatabase)
        dumLayout= QVBoxLayout()
        self.infoLabel = QLabel()
        dumLayout.addWidget(self.infoLabel)
        self.databaseLabel = QLabel()
        # self.databaseEdt = QLineEdit()
        self.subjectEdit = QLineEdit()
        self.commentsTextEdit = QTextEdit()
        dumLayout.addWidget(QLabel('Assunto'))
        dumLayout.addWidget(self.subjectEdit)
        dumLayout.addWidget(QLabel('Comentários'))
        dumLayout.addWidget(self.commentsTextEdit)
        self.createDatabaseBtn = QPushButton('Criar base de dados')
        self.createDatabaseBtn.clicked.connect(self.create_database)
        self.setDatabaseBtn = QPushButton('Mudar de Base de Dados')
        self.setDatabaseBtn.clicked.connect(self.set_database_click)
        dumLayout.addWidget(self.databaseLabel)
        dumLayout.addWidget(self.setDatabaseBtn)
        dumLayout.addWidget(self.createDatabaseBtn)
        exit_btn = QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)

        valid_btn = QPushButton('Valida')
        valid_btn.clicked.connect(self.valid_click)

        dumLayout.addLayout(qc.addHLayout([valid_btn, exit_btn]))
        if self.status_db:
            load_settings()
            self.databaseLabel.setText(gl.DB_PATH + gl.DB_FILE)
            self.commentsTextEdit.setText('')
        else:
            self.infoLabel.setText('Não foi encontrada nenhuma Base de Dados!')
        databaseLayout.addLayout(dumLayout)

    def valid_click(self):
        save_settings()
        sql = 'update params set param_data=? where param_data=? '
        sqlite_crud.execute_query(sql, (self.commentsTextEdit.toPlainText(), ''))
        sql = 'update params set param_data=? where param_data=? '
        sqlite_crud.execute_query(sql, (self.subjectEdit.text(), ''))
        self.close()

    def set_database_click(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                   gl.DB_PATH, "DB Files (*.sqlite3);;All Files (*.*)",
                                                   options=options)
        if file_name:
            gl.DB_PATH, gl.DB_FILE = os.path.split(file_name)
            gl.DB_PATH = gl.DB_PATH + '/'
            i = db_info()
            # load_settings()
            database_init.updater()
            self.commentsTextEdit.setText(i)

    def create_database(self):
        gl.DOCUMENTS_DIR = os.path.expanduser('~\\Documents')
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, 'Pasta', gl.DOCUMENTS_DIR, options=options)
        flag = False
        if directory:
            text, ok = QInputDialog.getText(self, 'Nome do Ficheiro', 'Nome da Base de Dados:')
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
            gl.DB_PATH = directory + '/'
            text = text.replace(' ', '_')
            gl.DB_FILE = text.replace('.', '_') + '.sqlite3'
            gl.DB_VERSION = 0
            database_init.updater()
            void = QMessageBox.warning(None, "Sucesso", 'A Base de Dados<br> <b>' + gl.DB_FILE + '</b> <br>foi criada!\nem ' + gl.DB_PATH,
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
            save_settings()
            i = db_info()
        else:
            void = QMessageBox.warning(None, "Erro", 'A Base de Dados não foi criada!',
                                                 QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def exit_click(self):
        gl.DB_PATH = gl.STACK_DB_PATH
        gl.DB_FILE = gl.STACK_DB_NAME
        self.close()


def db_info():
    sql = '''select 'Livros' as a, count(pu_id) as t from books
             union
             select 'Autores' as a, count(au_id) as t from authors
             union
             select 'Tipos' as a, count(ty_id) as t from  types
             union
             select 'Etiquetas' as a, count(ta_id) as t from  tags
             union
             select 'Locais' as a, count(local_id) as t from locals '''

    dum = sqlite_crud.query_many(sql)
    text = ''
    for n in dum:
        text += n[0] + ' : ' + str(n[1]) + '\n'
    sql = '''select param_name,param_data from params where param_level = 1; '''
    dum = sqlite_crud.query_many(sql)
    for n in dum:
        text += n[0] + ' : ' + str(n[1]) + '\n'
    return text



def save_settings():
    config = configparser.ConfigParser()
    config["last_db"] = {
        "path": gl.DB_PATH + '/',
        "file": gl.DB_FILE
    }
    config["main_window"] = {
        "x": "42",
        "y": "42",
        "w": "42",
        "h": "42",
    }
    file_path = "config.ini"
    with open(file_path, "w") as ini_file:
        config.write(ini_file)


def load_settings():
    config = configparser.ConfigParser()
    file_path = "config.ini"
    if stdio.file_ok(file_path):
        config.read(file_path)
        gl.DB_PATH = config.get("last_db", "path")
        gl.DB_FILE = config.get("last_db", "file")
        return True
    else:
        print('Database not set')
        return False


def main():
    app = QApplication(sys.argv)
    form = EditGlobalSettings()
    form.show()
    app.exec_()


if __name__ == '__main__':
    load_settings()
    main()
