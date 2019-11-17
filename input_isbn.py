#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextEdit, QCheckBox, QVBoxLayout, QLineEdit, QDialog, QComboBox,\
    QPushButton, QApplication
from PyQt5.Qt import Qt
import qlib
import edit_record
import sys
import isbn_lib
import parameters as gl
import dmPostgreSQL

class InputIsbn(QDialog):
    def __init__(self, parent=None):
        super(InputIsbn, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint)
        self.setWindowTitle('Descarregar dados do Wook por ISBN')
        masterLayout = QVBoxLayout(self)
        self.isbn = QLineEdit()
        self.isbn.setMaxLength(20)

        masterLayout.addLayout(qlib.addHLayout(['ISBN', self.isbn]))
        self.outputPlainText = QTextEdit()
        masterLayout.addWidget(self.outputPlainText)
        # self.searchWhereComboBox = QComboBox()
        # self.searchWhereComboBox.addItems(['Wook','ISBN Search'])
        # masterLayout.addLayout(qlib.addHLayout(['Procurar em', self.searchWhereComboBox, True]))
        self.fill_date_CB = QCheckBox('O Ano é igual á data de edição')
        self.addAuthorChk = QCheckBox('Adiciona autor como etiqueta')
        self.addAuthorChk.setCheckState(2)
        self.check_in_db_CB = QCheckBox('Verifica se já existe na Base de Dados')
        self.check_in_db_CB.setCheckState(2)
        self.set_title_CB = QCheckBox('Capitaliza')
        self.setIntelTitleCx = QCheckBox('Capitalização inteligente (+lento)')
        self.setIntelTitleCx.setCheckState(2)
        self.set_title_upper = QCheckBox('MAIUSCULA')
        self.set_autor_forename = QCheckBox('Autor APELIDO, sobrenome nome;')
        masterLayout.addWidget(self.fill_date_CB)
        masterLayout.addWidget(self.addAuthorChk)
        masterLayout.addWidget(self.check_in_db_CB)
        masterLayout.addWidget(self.set_title_CB)
        masterLayout.addWidget(self.setIntelTitleCx)
        masterLayout.addWidget(self.set_title_upper)
        masterLayout.addWidget(self.set_autor_forename)
        self.search_isbn = QPushButton('Pesquisa')
        self.search_isbn.clicked.connect(self.search_ISBN_click)
        self.cancel_btn = QPushButton('Sair')
        self.cancel_btn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qlib.addHLayout([self.search_isbn, self.cancel_btn]))
        self.show()
    
    def search_ISBN_click(self):
        self.outputPlainText.clear()
        self.outputPlainText.repaint()
        tx = self.isbn.text().strip().replace('-', '')
        self.outputPlainText.setText(tx)
        self.isbn.setText(tx)
        self.isbn.repaint()
        if self.check_in_db_CB.checkState():
            a = dmPostgreSQL.query_one('select pu_id from livros where pu_isbn=%s ', (tx,))
            if a == None:
                self.get_isbn(tx)
            else:
                self.outputPlainText.setText('este ISBN já existe')
                self.outputPlainText.repaint()
        else:
            self.get_isbn(tx) # wook

    def get_isbn(self, tx):
        xl = {}
        try:
            if len(tx) != 13:
                raise ValueError
            if gl.ISBN_SEARCH_SITE == 0:
                # wook
                xl = isbn_lib.get_isbn_wook(tx)
            elif gl.ISBN_SEARCH_SITE == 1:
                xl = isbn_lib.get_isbn_search(tx)
            if not xl['pass']:
                raise ValueError
        except ValueError:
            xl['pass'] = False
            xl['error'] ='Erro de validação do ISBN'
    
        if xl['pass']:
            xl['pu_isbn'] = tx
            # process option
            if self.setIntelTitleCx.checkState():
                self.set_title_CB.setCheckState(0)
                xl['pu_title'] = isbn_lib.text_title(xl['pu_title'])
                xl['pu_sub_title'] = isbn_lib.text_title(xl['pu_sub_title'])
            if self.set_title_CB.checkState():
                xl['pu_title'] = xl['pu_title'].title()
            if self.fill_date_CB.checkState():
                xl['pu_ed_year'] = xl['pu_ed_date'].split('-')[1]
            else:
                xl['pu_ed_year'] = '0'
            if self.set_title_upper.checkState():
                xl['pu_title'] = xl['pu_title'].upper()
            if self.set_autor_forename.checkState():
                xl['pu_author'] = autor_forename(xl['pu_author'])
            if self.addAuthorChk.checkState():
                xl['tag_author'] = True
            else:
                xl['tag_author'] = False
            self.close()
            form = edit_record.EditRecord(-1, xl, isbn=True)
            form.exec_()
        else:
            self.outputPlainText.append(str(xl))
    
    def exit_click(self):
        self.close()
    

def autor_forename(a, caps=True):
    bc = a.split(',')
    xl = ''
    for f in bc:
        b = f.split()
        e = b[-1] + ', '
        if caps:
            e = e.upper()
        for n in range(len(b)-1):
            e = e + b[n] + ' '
        xl = xl + e + ';'
    xl = xl.replace(' ;', ';')
    return xl[:-1]


def main():
    app = QApplication(sys.argv)
    form = InputIsbn()
    form.show()
    app.exec_()


if __name__ == '__main__':
    pass
