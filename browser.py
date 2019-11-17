# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton, QApplication,QHBoxLayout,QLineEdit
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets, QWebEngineCookieStore

# try:
#     import ctypes
#     import ctypes.util
#     ctypes.CDLL(ctypes.util.find_library("GL"), mode=ctypes.RTLD_GLOBAL)
# except TypeError:
#     pass

# import parameters as pa

class InternetBrowser(QDialog):
    def __init__(self, website,  parent = None):
        super(InternetBrowser,  self).__init__(parent)
        self.resize(1268, 1024)
        siteUrl = QUrl(website)
        mainLayout = QVBoxLayout(self)
        addressEditLine = QLineEdit()
        dumLayout = QHBoxLayout()
        not_workingBtn = QPushButton('Not Working')
        # self.connect(not_workingBtn,  SIGNAL("clicked()"),  self.not_working_click)

        deleteBtn = QPushButton('Apaga')
        # self.connect(deleteBtn,  SIGNAL("clicked()"),  self.delete_click)

        addressEditLine.setText(siteUrl.toString())
        self.browserWebView = QtWebEngineWidgets.QWebEngineView(self)

        dumLayout.addWidget(not_workingBtn)
        dumLayout.addWidget(deleteBtn)
        dumLayout.addStretch()
        mainLayout.addWidget(addressEditLine)
        mainLayout.addLayout(dumLayout)
        mainLayout.addWidget(self.browserWebView)
        #browserWebView.setGeometry(0, 0, 799, 399)
        self.browserWebView.load(siteUrl)

    def not_working_click(self):
        f = dbmain.execute_query('update items set it_condition = 2  where it_item_number = %s', (str(pa.current_item_number), ) )
        self.close()

    def delete_click(self):
        sql = 'UPDATE item_log set ilog_tracked = %s, ilog_on_spool = %s \
        where ilog_item_number = %s '
        data =(True,False,pa.current_item_number)
        apaga = dbmain.execute_query(sql,data)
        print('Registo:', pa.current_item_number, ' marcado para apagar!')
        self.close()



class BrowserInLine(QDialog):
    def __init__(self, url, title='Teste', parent=None):
        super(BrowserInLine, self).__init__(parent)
        self.setWindowTitle(title)
        self.browserWebView = QtWebEngineWidgets.QWebEngineView(self)
        layout = QVBoxLayout()
        layout.addWidget(self.browserWebView)
        self.printBtn = QPushButton('Matrix Rolad')
        self.printBtn.clicked.connect(self.reload_page)
        self.browserWebView.page().profile().clearHttpCache()
        self.browserWebView.page().profile().clearAllVisitedLinks()
        a = QWebEngineCookieStore.deleteAllCookies()
        # self.printBtn.clicked.connect(self.print_preview_click)
        layout.addWidget(self.printBtn)
        self.setLayout(layout)
        
        # self.browserWebView.load(QUrl("http://google.com/"))
        self.browserWebView.load(QUrl("http://eorder.infornash.com/"))
        # self.browserWebView.load(QUrl("https://www.whoishostingthis.com/tools/user-agent/"))
    
    def reload_page(self):
        self.browserWebView.load(QUrl("http://eorder.infornash.com/"))




if __name__ == '__main__':
    pass

def main():
    app = QApplication(sys.argv)
    form = BrowserInLine('http://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_regexp_test2')
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
