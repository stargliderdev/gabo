# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QDialog,QPushButton,QApplication,QCheckBox
from PyQt5.Qt import Qt
import sys
import qlib

class BrowserView(QDialog):
    def __init__(self, title, html, size = (400,300),confirm=(False,''), parent = None):
        """ mostra uma variavel contendo html num browser """
        super(BrowserView,  self).__init__(parent)
        self.setWindowFlags(Qt.Dialog|Qt.WindowTitleHint)
        self.setStyleSheet("background-color:#fffff0;")
        self.resize(size[0],size[1])
        self.ret = 0
        self.setWindowTitle(title)
        self.browserWebView = QTextEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(self.browserWebView)
        self.closeBtn = QPushButton('Fecha')
        self.exitBtn = QPushButton('Cancelar')
        self.confirmChk = QCheckBox(confirm[1])
        if confirm[0]:
            layout.addWidget(self.confirmChk)
            self.closeBtn.setEnabled(False)
            self.confirmChk.stateChanged.connect(self.confirm_state_changed)
            layout.addLayout(qlib.addHLayout([self.closeBtn,self.exitBtn]))
            self.exitBtn.clicked.connect(self.close_click)
        else:
            self.closeBtn.setEnabled(True)
            self.closeBtn.setFocus()
            layout.addWidget(self.closeBtn)
        self.closeBtn.clicked.connect(self.close_click)
        self.setLayout(layout)
        self.browserWebView.setHtml(html)
        self.browserWebView.setReadOnly(True)
    
    def confirm_state_changed(self):
        if self.confirmChk.checkState()==2:
            self.closeBtn.setEnabled(True)
        else:
            self.closeBtn.setEnabled(False)
            
    def close_click(self):
        self.ret=self.confirmChk.checkState()
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bc1 ="""<!DOCTYPE html><html lang="pt_pt"><meta name="viewport" content="width=device-width, initial-scale=1">
    <p style="text-align:center;">
    <img src="./info.png" ></p> <p>Versão 10-12-2018 </p></html>"""
    form = BrowserView('test',bc1,confirm=(True,'Understand!'))
    form.show()
    app.exec_()
    print(form.ret)