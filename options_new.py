#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import  QCheckBox, QVBoxLayout,  QDialog, QPushButton, QApplication,QMessageBox
from PyQt5.Qt import Qt
import qlib
import edit_record
import sys
import isbn_lib
import parameters as gl
import stdio


class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint)
        self.setWindowTitle('Opções')
        masterLayout = QVBoxLayout(self)
        self.yearAsDateCbox = QCheckBox('O Ano é igual á data de edição')
        self.addIsbnCbox = QCheckBox('Adiciona ISBN')
        self.addAuthorAsLabelCbox = QCheckBox('Adiciona autor como etiqueta')
        # self.addAuthorAsLabelCbox.setCheckState(2)
        self.checkInDatabaseCbox = QCheckBox('Verifica se já existe na Base de Dados')
        # self.checkInDatabaseCbox.setCheckState(2)
        self.capitalizeTitleCbox = QCheckBox('Capitaliza Titulo')
        self.smartTitleCbox = QCheckBox('Capitalização do Titulo inteligente (+lento)')
        # self.smartTitleCbox.setCheckState(2)
        self.titleInUpperCbox = QCheckBox('Titulo em Maiusculas')
        self.authorSurnameCbox = QCheckBox('Autor como APELIDO, Nome;')
        self.authorSurnameTitleCbox = QCheckBox('Autor como Apelido, Nome;')
        masterLayout.addWidget(self.yearAsDateCbox)
        masterLayout.addWidget(self.addIsbnCbox)
        masterLayout.addWidget(self.addAuthorAsLabelCbox)
        masterLayout.addWidget(self.checkInDatabaseCbox)
        masterLayout.addWidget(self.capitalizeTitleCbox)
        masterLayout.addWidget(self.smartTitleCbox)
        masterLayout.addWidget(self.titleInUpperCbox)
        masterLayout.addWidget(self.authorSurnameCbox)
        masterLayout.addWidget(self.authorSurnameTitleCbox)
        self.validateOptionsBtn = QPushButton('Valida')
        self.validateOptionsBtn.clicked.connect(self.valida_options_click)

        self.cancelBtn = QPushButton('Sair')
        self.cancelBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qlib.addHLayout([self.validateOptionsBtn, self.cancelBtn]))
        self.refresh()
        
    def refresh(self):
        self.yearAsDateCbox.setCheckState(bool_to_check(gl.year_as_date))
        self.addAuthorAsLabelCbox.setCheckState(bool_to_check(gl.add_author_as_label))
        self.checkInDatabaseCbox.setCheckState(bool_to_check(gl.check_in_database))
        self.capitalizeTitleCbox.setCheckState(bool_to_check(gl.capitalize_title))
        self.smartTitleCbox.setCheckState(bool_to_check(gl.smart_title))
        self.titleInUpperCbox.setCheckState(bool_to_check(gl.title_in_upper))
        self.authorSurnameCbox.setCheckState(bool_to_check(gl.author_surname))
        self.authorSurnameTitleCbox.setCheckState(bool_to_check(gl.author_surname_title))
        self.addIsbnCbox.setCheckState(bool_to_check(gl.add_isbn))
    
    def valida_options_click(self):
        gl.year_as_date = check_to_bool(self.yearAsDateCbox.checkState())
        gl.add_author_as_label = check_to_bool(self.addAuthorAsLabelCbox.checkState())
        gl.check_in_database = check_to_bool(self.checkInDatabaseCbox.checkState())
        gl.capitalize_title = check_to_bool(self.capitalizeTitleCbox.checkState())
        gl.smart_title = check_to_bool(self.smartTitleCbox.checkState())
        gl.title_in_upper = check_to_bool(self.titleInUpperCbox.checkState())
        gl.author_surname = check_to_bool(self.authorSurnameCbox.checkState())
        gl.author_surname_title = check_to_bool(self.authorSurnameTitleCbox.checkState())
        gl.add_isbn = check_to_bool(self.addIsbnCbox.checkState())
        self.close()

    # def get_isbn(self, tx):
    #     xl = {}
    #     try:
    #         if len(tx) != 13:
    #             raise ValueError
    #         if gl.ISBN_SEARCH_SITE == 0:
    #             # wook
    #             xl = isbn_lib.get_isbn_wook(tx)
    #         elif gl.ISBN_SEARCH_SITE == 1:
    #             xl = isbn_lib.get_isbn_search(tx)
    #         if not xl['pass']:
    #             raise ValueError
    #     except ValueError:
    #         xl['pass'] = False
    #         xl['error'] ='Erro de validação do ISBN'
    #
    #     if xl['pass']:
    #         xl['pu_isbn'] = tx
    #         # process option
    #         if self.smartTitleCbox.checkState():
    #             self.capitalizeTitleCbox.setCheckState(0)
    #             xl['pu_title'] = isbn_lib.text_title(xl['pu_title'])
    #             xl['pu_sub_title'] = isbn_lib.text_title(xl['pu_sub_title'])
    #         if self.capitalizeTitleCbox.checkState():
    #             xl['pu_title'] = xl['pu_title'].title()
    #         if self.yearAsDateCbox.checkState():
    #             xl['pu_ed_year'] = xl['pu_ed_date'].split('-')[1]
    #         else:
    #             xl['pu_ed_year'] = '0'
    #         if self.titleInUpperCbox.checkState():
    #             xl['pu_title'] = xl['pu_title'].upper()
    #         if self.authorSurnameCbox.checkState():
    #             xl['pu_author'] = autor_forename(xl['pu_author'])
    #         if self.addAuthorAsLabelCbox.checkState():
    #             xl['tag_author'] = True
    #         else:
    #             xl['tag_author'] = False
    #         self.close()
    #         form = edit_record.EditRecord(-1, xl, draft_data=True)
    #         form.exec_()
    #     else:
    #         self.outputPlainText.setText('Este ISBN não existe!')
    #         b = QMessageBox.question(self,
    #             'Este ISBN não existe',
    #             'Este ISBN não existe na Wook, procurar na internet?',
    #             QMessageBox.StandardButtons(QMessageBox.No | QMessageBox.Yes), QMessageBox.No)
    #         if b == QMessageBox.Yes:
    #             stdio.search_internet('ISBN ' + self.isbn.text())
    
    def exit_click(self):
        self.close()
    


def bool_to_check(boolean):
    if boolean:
        return 2
    else:
        return 0

def check_to_bool(check_state):
    if check_state == 2:
        return True
    else:
        False
        
def main():
    app = QApplication(sys.argv)
    form = OptionsDialog()
    form.show()
    app.exec_()


if __name__ == '__main__':
    xl = isbn_lib.get_isbn_wook('9789722365741')
    
