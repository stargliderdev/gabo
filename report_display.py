# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QDialog,QApplication, QPushButton, QHBoxLayout,QVBoxLayout, QFileDialog
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import QFileInfo
from PyQt5 import QtWebEngineWidgets

import qlib

class DisplayReport(QDialog):
    def __init__(self, html_report, parent=None):
        super(DisplayReport, self).__init__(parent)
        mainLayout = QVBoxLayout(self)
        self.resize(1024, 768)
        self.printBtn = QPushButton('Print')
        self.printBtn.clicked.connect(self.print_page)
        
        self.printPreviewBtn = QPushButton('Preview')
        self.printPreviewBtn.clicked.connect(self.filePrintPreview)
        
        self.printToPdfBtn = QPushButton('To PDF')
        self.printToPdfBtn.clicked.connect(self.print_to_pdf)
        
        self.exitBtn = QPushButton('Exit')
        self.exitBtn.clicked.connect(self.exit_click)
        
        mainLayout.addLayout(qlib.addHLayout([self.printBtn, self.printPreviewBtn, self.printToPdfBtn, True, self.exitBtn]))
        
        
        self.reportTextEdit = QtWebEngineWidgets.QWebEngineView(self)
        self.reportTextEdit.setHtml(html_report)
        self.printer = QPrinter()
        mainLayout.addWidget(self.reportTextEdit)

    def print_page(self):
        dlg = QPrintDialog(self.printer)
        if dlg.exec_():
            self.reportTextEdit.page().print(self.printer, self.print_completed)

    def print_completed(self, success):
        pass  # Do something in here, maybe update the status bar?
    
    def print_to_pdf(self):
        self.reportTextEdit.page().printToPdf('./teste_to_pdf.pdf')
    
    def filePrintPreview(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def filePrint(self):
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)

        if self.reportTextEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QPrintDialog.Accepted:
            self.reportTextEdit.print_(printer)

        del dlg

    def printPreview(self, printer):
        self.reportTextEdit.print_(printer)

    def filePrintPdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None,
                "PDF files (*.pdf);;All Files (*)")

        if fn:
            if QFileInfo(fn).suffix() =='':
                fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.reportTextEdit.document().print_(printer)
    
    def exit_click(self):
        self.close()
    
if __name__ == '__main__':
    pass
