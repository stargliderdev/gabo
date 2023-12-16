#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication, QTextBrowser, QTextEdit, QDateEdit, QCheckBox
from PyQt5.QtGui import QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt
from prettytable import PrettyTable
import libpg
import qlib as qc

class ShowInTerminal(QDialog):
    def __init__(self,str_table, window_title='', parent=None):
        super(ShowInTerminal, self).__init__(parent)
        self.cc_data = {}
        self.resize(1024, 768)
        self.setWindowTitle(window_title)
        
        palette = QPalette()
        brush = QBrush(QColor(0, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(0, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(165, 164, 164))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(244, 244, 244))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        font = QFont('courier new', 10)
        font.setWeight(80)
        font.setBold(False)
        
        # self.resize(800, 600)
        mainLayout = QVBoxLayout(self)
        # butoes
        calculateBtn = QPushButton('HTML')
        # calculateBtn.clicked.connect(self.calculate_click)
        
        exitBtn = QPushButton('Sair')
        exitBtn.clicked.connect(self.exit_click)
        mainLayout.addLayout(qc.addHLayout([ exitBtn, True]))
        
        self.reportText = QTextBrowser()
        # self.reportText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.reportText.setPalette(palette)
        self.reportText.setFont(font)
        mainLayout.addWidget(self.reportText)
        self.reportText.setPlainText(str(str_table))

    

    def exit_click(self):
        self.close()



    
    
def main():
    
    app = QApplication(sys.argv)
    form = ShowInTerminal()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
