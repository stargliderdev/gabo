#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFrame, QLabel, QCheckBox, QVBoxLayout, \
    QWidget,QHBoxLayout
from PyQt5.Qt import Qt


# versão 1.0 2 NOV 2014
def setSize(toolButton, s=20):
    toolButton.setMaximumWidth(s)
    toolButton.setMinimumWidth(s)
    toolButton.setMaximumHeight(s)
    toolButton.setMinimumHeight(s)
    return toolButton

def checkBoxGrid(label=''):
    w = QWidget()
    l = QHBoxLayout(w)
    l.setContentsMargins(0,0,0,0)
    l.addStretch()
    c = QCheckBox(label)
    l.addWidget(c)
    l.addStretch()
    return w


def addHLayout(listobj1,label_size=80, label_align=Qt.AlignVCenter|Qt.AlignRight):
    dumLayout = QHBoxLayout()
    for n in listobj1:
        if (type(n)==str) or (type(n) == str):
            toto = QLabel(n)
            toto.setMinimumWidth(label_size)
            toto.setMaximumWidth(label_size)
            toto.setAlignment(label_align)
            dumLayout.addWidget(toto)
        elif type(n) == bool:
            dumLayout.addStretch()
        elif type(n) == int:
            dumLayout.addSpacing(n)
        else:
            dumLayout.addWidget(n)
    return dumLayout


def addVLayout(listobj1):
    dumLayout = QVBoxLayout()
    for n in listobj1:
        if (type(n)==str) or (type(n) == str):
            dumLayout.addWidget(QLabel(n))
        elif type(n) == bool:
            dumLayout.addStretch()
        else:
            dumLayout.addWidget(n)
    return dumLayout

def HLine():
    toto = QFrame()
    toto.setFrameShape(QFrame.HLine)
    toto.setFrameShadow(QFrame.Sunken)
    return toto