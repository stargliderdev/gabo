#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import  QVBoxLayout, QDialog, QButtonGroup, QPushButton, QTextEdit

class DadosWizard(QDialog):
    def __init__(self, text_message,options,parent = None):
        super(DadosWizard,   self).__init__(parent)
        #self.resize(800, 600)
        
        self.setWindowTitle('Faltam Dados.') 
        self.toto = -1

        mainLayout = QVBoxLayout(self)
        messageTextEdit = QTextEdit()
        messageTextEdit.setText(text_message)
        mainLayout.addWidget(messageTextEdit)
        mainLayout.addLayout(self.make_buttons(options) )#[(1,'Software'),(2,'Hardware'),(3,u'Instalações')]))

    def make_buttons(self,data):
        self.salesButtonsGroup = QButtonGroup()
        totoLayout = QVBoxLayout()
        cnt = 0
        for n in data:
            btn = QPushButton(n)
            self.salesButtonsGroup.addButton(btn, cnt)
            cnt +=1
            totoLayout.addWidget(btn)
            
        # self.connect(self.salesButtonsGroup, SIGNAL("buttonClicked(int)"), self.button_group_click)
        self.salesButtonsGroup.buttonClicked.connect(self.button_group_click)
        return totoLayout

    def button_group_click(self,status_id):
        self.toto = status_id
        self.close()

    def closeBtn_click(self):
        self.toto = -1
        self.close()

    def parseField(self, field_name):
        # v2
        dum = self.item_data[field_name]
        if type(dum) == int:
            return str(dum)
        elif dum == None:
            return ''
        else:
            return dum

if __name__ == '__main__':
    pass