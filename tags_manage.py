#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QTableWidget, QInputDialog, QDialog, QTextEdit, \
    QTextBrowser, QTableWidgetItem, QApplication, QMessageBox, QHBoxLayout, QToolButton

import ex_grid
import qlib as qc
import parameters as gl
import sqlite_crud
import stdio
import sqlite_crud


class BrowserTags(QDialog):
    def __init__(self, from_book=True,  parent = None):
        super(BrowserTags,  self).__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint) #|Qt.WindowStaysOnTopHint) #|Qt.WindowTitleHint)
        self.flag = False
        self.from_book = from_book
        self.resize(600, 400)
        self.setWindowTitle('Gere Etiquetas')
        self.setWindowIcon(QIcon('./img/tags.png'))
        masterLayout = QVBoxLayout(self)
        self.tag_list = []
        self.tag_id = -1
        clearTagsBtn = QToolButton()
        clearTagsBtn.setToolTip('Limpa Pesquisa')
        clearTagsBtn.setIcon(QIcon('./img/clear.png'))
        # self.set_icon_size(clearTagsBtn)
        clearTagsBtn.clicked.connect(self.clear_tags_search)
        if self.from_book:
            # deselectTagsBtn=QPushButton('Des-seleciona')
            # deselectTagsBtn.clicked.connect(self.deselect_click)
            cleanTranfBtn=QPushButton('Limpa Transferidas')
            cleanTranfBtn.clicked.connect(self.clean_transfer)
            addTagBtn=QPushButton('Adiciona Tag')
            addTagBtn.clicked.connect(self.add_new_tag)
            masterLayout.addLayout(qc.addHLayout([ cleanTranfBtn, addTagBtn, clearTagsBtn,True]))
        else:
            deleteTagsBtn = QPushButton('Apaga esta Etiqueta')
            deleteTagsBtn.clicked.connect(self.delete_tag_click)
            masterLayout.addLayout(qc.addHLayout([deleteTagsBtn,clearTagsBtn,True]))
        
        self.searchEdit = QLineEdit()
        self.toto = ()
        self.searchEdit.textChanged.connect(self.tag_search_changed)
        
        self.tagsGrid = QTableWidget()
        self.tagsGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tagsGrid.verticalHeader().setDefaultSectionSize(20)
        self.tagsGrid.verticalHeader().setVisible(False)
        self.tagsGrid.setAlternatingRowColors(True)
        self.tagsGrid.setStyleSheet("alternate-background-color: #d2e5ff;")
        self.tagsGrid.itemDoubleClicked.connect(self.transfer_click)

        self.currentTagsGrid = QTableWidget()
        self.currentTagsGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.currentTagsGrid.verticalHeader().setDefaultSectionSize(20)
        self.currentTagsGrid.verticalHeader().setVisible(False)
        self.currentTagsGrid.setAlternatingRowColors(True)
        self.currentTagsGrid.setStyleSheet("alternate-background-color: #d2e5ff;")
        self.currentTagsGrid.itemDoubleClicked.connect(self.transfer_last_click)
        
        self.current_tags = QTextBrowser()
        self.current_tags.setMaximumHeight(60)
        self.current_tags.setMinimumHeight(60)
        allTagsLayout = QHBoxLayout()
        if self.from_book:
            allTagsLayout.addLayout(qc.addVLayout([self.searchEdit, self.tagsGrid]))
            allTagsLayout.addLayout(qc.addVLayout(['Ultimas', self.currentTagsGrid]))
            # masterLayout.addLayout(qc.addHLayout([self.tagsGrid, self.lastTagsGrid]))
            masterLayout.addLayout(allTagsLayout)
        else:
            masterLayout.addWidget(self.searchEdit)
            masterLayout.addLayout(qc.addHLayout([self.tagsGrid]))
            
            
        # masterLayout.addWidget(self.current_tags)
        exit_btn=QPushButton('Sair')
        exit_btn.clicked.connect(self.exit_click)
        
        valid_btn=QPushButton('Substitui')
        valid_btn.clicked.connect(self.valid_click)
        
        add_btn=QPushButton('Adiciona')
        add_btn.clicked.connect(self.add_click)
        
        if self.from_book:
            masterLayout.addLayout(qc.addHLayout([valid_btn, add_btn, exit_btn]))
        else:
            masterLayout.addLayout(qc.addHLayout([exit_btn]))
        self.tag_refresh()
        if self.from_book:
            self.current_tags_refresh()
        # else:
        #     self.searchEdit.setText(gl.LAST_TAG)
        #     self.tag_search_changed(gl.LAST_TAG)

    def deselect_click(self):
        self.tagsGrid.clearSelection()

    def clean_transfer(self):
        self.current_tags.clear()
    
    def clear_tags_search(self):
        self.searchEdit.clear()
        self.tag_refresh()

    def delete_tag_click(self):
        if self.tagsGrid.currentItem() is None:
            pass
        else:
            ask = QMessageBox.warning(None,
                                      "Apagar Etiquetas",
                                      """Atenção\n vou apagar TODAS as referencias a esta etiqueta! \nConfirmas? """,
                                      QMessageBox.StandardButtons(QMessageBox.Cancel | QMessageBox.Yes),
                                      QMessageBox.Cancel)
            if ask == QMessageBox.Yes:
                a = self.tagsGrid.item(self.tagsGrid.currentRow(), 1).text()
                sql = 'delete from tags_reference where tags_ref_key=? '
                sqlite_crud.execute_query(sql,(a,))
                sql = 'delete from tags where ta_name = ?'
                sqlite_crud.execute_query(sql, (a,))
                self.tag_refresh()
                self.tag_search_changed(self.searchEdit.text())
        
    def add_new_tag(self):
        b, ok = QInputDialog.getText(self, self.tr("Nova Etiqueta"), self.tr("Nova Etiqueta"), QLineEdit.Normal)
        if ok and not b == '' :
            if self.current_tags.toPlainText() == '':
                self.current_tags.setText(b)
            else:
             self.current_tags.setText(self.current_tags.toPlainText() +  '|' + b)
        else:
            print('do nothing')

    def transfer_click(self):
        print('transfer click')
        if self.from_book:
            gl.LAST_TAG = ''
            a = self.tagsGrid.item(self.tagsGrid.currentRow(), 1).text()
            gl.last_tags.insert(0, self.tagsGrid.item(self.tagsGrid.currentRow(), 1).text())
            self.tag_list = self.current_tags.toPlainText().split('|')
            self.tag_list.append(a)
            xl = ''
            for n in self.tag_list:
                xl += '<font color="blue"><strong>' + n + ',</font>'
            self.current_tags.setHtml(xl)
            self.searchEdit.clear()
            self.searchEdit.setFocus()
        else:
            a = self.tagsGrid.item(self.tagsGrid.currentRow(), 1).text()
            gl.last_tags.insert(0, self.tagsGrid.item(self.tagsGrid.currentRow(), 1).text())
            self.tag_list = a
            gl.LAST_TAG = a
            self.close()

    def transfer_last_click(self):
        a = self.currentTagsGrid.item(self.currentTagsGrid.currentRow(), 0).text()
        self.tag_list = self.current_tags.toPlainText().split('|')
        self.tag_list.append(a)
        xl = ''
        for n in self.tag_list:
            xl += '<font color="blue"><strong>' + n + ',</font>'
        self.current_tags.setHtml(xl)
        
    def valid_click(self):
        self.tag_id = 0
        self.tag_list = self.current_tags.toPlainText()
        # self.tag_list = self.tag_list.replace(',,',',')
        self.tag_list = self.tag_list.rstrip('|')
        self.tag_list = self.tag_list.lstrip('|')
        self.flag = True
        self.close()

    def add_click(self):
        self.tag_id = 1
        self.tag_list = self.current_tags.toPlainText()
        # self.tag_list = self.tag_list.replace(',,',',')
        self.tag_list = self.tag_list.rstrip('|')
        self.tag_list = self.tag_list.lstrip('|')
        self.flag = True
        # save_last_tags_params()
        self.close()

    def tag_refresh(self):
        self.c_grid = 10
        # sql = '''select ta_id, ta_name from tags order by ta_name'''
        sql = '''select ta_id,ta_name from tags order by ta_name'''
        dataset = sqlite_crud.query_many(sql)
        ex_grid.ex_grid_update (self.tagsGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset, hidden=0)
        self.tagsGrid.horizontalHeader().setVisible(False)
        self.tagsGrid.setColumnWidth(0, 80)
        self.tagsGrid.setColumnWidth(1, 350)
        
    def current_tags_refresh(self):
        # self.c_grid = 10
        lin = 0
        self.currentTagsGrid.setColumnCount(1)
        self.currentTagsGrid.setRowCount(len(gl.current_tags))
        print(gl.current_tags)
        for n in gl.current_tags:
            item = QTableWidgetItem()
            item.setText(n)
            self.currentTagsGrid.setItem(lin, 0, item)
            lin +=1
        self.currentTagsGrid.horizontalHeader().setVisible(False)
        self.currentTagsGrid.setColumnWidth(0, 450)

    def tag_search_changed(self, text):
        if len(text) > 2:
            search = '\'%%' + text + '%%\''
            # print 'search ',text
            sql = '''SELECT ta_id, ta_name FROM tags WHERE lower(ta_name) LIKE ''' + search + ''' ORDER by ta_name '''
            dataset = sqlite_crud.query_many(sql)
            ex_grid.ex_grid_update (self.tagsGrid, {0:['ID', 'i'], 1:['Nome', 's']}, dataset, hidden=0)
            self.tagsGrid.horizontalHeader().setVisible(False)
            self.tagsGrid.setColumnWidth(0, 80)
            self.tagsGrid.setColumnWidth(1, 350)

    def exit_click(self):
        self.tag_list = []
        self.tag_id = -1
        gl.LAST_TAG = ''
        self.close()

def main():
    gl.current_tags = ['guerra','guerra colonial','história de portugal','história']
    app = QApplication(sys.argv)
    form = BrowserTags(['musica portuguesa', 'literatura', 'música', 'manuel faria', 'biografias', 'trovante', 'bandas portuguesas'])
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

