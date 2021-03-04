# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton, QApplication, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets #, QWebEngineCookieStore

import edit_record
import options_new
import isbn_lib

class BrowserInLine(QDialog):
    def __init__(self, url, title='Wook', parent=None):
        super(BrowserInLine, self).__init__(parent)
        self.setWindowTitle(title)
        self.resize(1200, 768)
        self.wook = {}
        layout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        self.crawlBtn = QPushButton('Adiciona')
        self.crawlBtn.clicked.connect(self.reload_page)
        self.optionBtn = QPushButton('Opções')
        self.optionBtn.clicked.connect(self.options_click)
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        
        buttonLayout.addWidget(self.crawlBtn)
        buttonLayout.addWidget(self.optionBtn)
        buttonLayout.addWidget(exitBtn)
        self.browserWebView = QtWebEngineWidgets.QWebEngineView(self)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.browserWebView)
        self.browserWebView.page().profile().clearHttpCache()
        self.browserWebView.page().profile().clearAllVisitedLinks()
        self.setLayout(layout)
        self.browserWebView.load(QUrl(url))
    
    def reload_page(self):
        self.browserWebView.page().toHtml(self.add_book_click)

    def add_book_click(self, html):
        if isbn_lib.parse_wook(html):
            form = edit_record.EditRecord(-1,draft_data=True)
            form.exec_()
        else:
            QMessageBox.information(None,"Erro",'Não foi encontrado nenhum livro na página!',QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
        # self.close()
    
    def options_click(self):
        form = options_new.OptionsDialog()
        form.exec_()

    def exit_click(self):
        self.wook = {}
        self.close()


if __name__ == '__main__':
    pass

def main():
    app = QApplication(sys.argv)
    form = BrowserInLine("https://www.wook.pt/")
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
