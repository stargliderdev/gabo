#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import sys

from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QApplication, QDialog, QInputDialog, \
     QMessageBox, QTreeWidget, QTreeWidgetItem
import dmPostgreSQL as dbmain
import qlib as qc
import data_access
import parameters as gl
import stdio


class TagsSpecialBrowser(QDialog):
    def __init__(self,  parent = None):
        super(TagsSpecialBrowser, self).__init__(parent)
        self.setWindowTitle('Etiquetas Especiais')
        masterLayout = QVBoxLayout(self)
        self.textEdit = QLineEdit()
        self.tagsSpecialList = QTreeWidget()
        
        addBtn = QPushButton('Adiciona')
        addBtn.clicked.connect(self.add_click)
        
        deleteBtn = QPushButton('Apaga')
        deleteBtn.clicked.connect(self.delete_click)
        
        renameBtn = QPushButton('Renomeia')
        renameBtn.clicked.connect(self.rename_click)
        
        orderBtn = QPushButton('Ordem')
        orderBtn.clicked.connect(self.order_click)
        
        exitBtn = QPushButton('Sair')
        exitBtn.setMinimumWidth(400)
        exitBtn.clicked.connect(self.exit_click)
        
        masterLayout.addLayout(qc.addHLayout([addBtn,renameBtn,orderBtn, deleteBtn]))
        masterLayout.addWidget(self.tagsSpecialList)
        masterLayout.addWidget(exitBtn)
        self.update_combo()
        
    def update_combo(self):
        data_access.get_special_tags()
        self.tagsSpecialList.clear()
        self.tagsSpecialList.setHeaderLabels(["Nome", "Ordem", "Chave"])
        items = []
        for n in gl.tag_special_list:
            item = QTreeWidgetItem([n[0], str(n[2]), n[1]])
            items.append(item)
        self.tagsSpecialList.insertTopLevelItems(0, items)
        self.tagsSpecialList.setColumnWidth(0, 200)
        self.tagsSpecialList.setColumnWidth(1, 50)
        self.tagsSpecialList.setColumnWidth(2,1)

    def add_click(self):
        text, flag = QInputDialog.getText(None, "Adiciona Etiqueta Especial:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            if not dbmain.find_duplicate('tags_special', 'tags_special_key', text):
                m = hashlib.md5()
                m.update(text.encode('utf-8'))
                tags_key = str(m.hexdigest())[:8]
                sql = 'INSERT into tags_special (tags_special_name, tags_special_key) VALUES (%s, %s);'
                dbmain.execute_query(sql, (text,tags_key))
                self.update_combo()
                self.textEdit.clear()
            else:
                void = QMessageBox.warning(None, "Erro", 'Etiqueta Duplicada',
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def delete_click(self):
        if self.tagsSpecialList.currentItem() is None:
            pass
        else:
            ask = QMessageBox.warning(None,
                                           "Apagar Etiquetas",
                                           """Atenção\n vou apagar TODAS as referencias a esta etiqueta! \nConfirmas? """,
                                           QMessageBox.StandardButtons(QMessageBox.Cancel | QMessageBox.Yes),
                                           QMessageBox.Cancel)
            if ask == QMessageBox.Yes:
                dbmain.execute_query('delete from tags_reference where tags_ref_key=%s', (self.tagsSpecialList.currentItem().text(2),))
                dbmain.execute_query('delete from tags_special where tags_special_key=%s', (self.tagsSpecialList.currentItem().text(2),))
                self.update_combo()
            else:
                pass


    def rename_click(self):
        text, flag = QInputDialog.getText(None, "Altera nome da Etiqueta:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('UPDATE tags_special set tags_special_name=%s WHERE tags_special_name=%s',
                                 (text,self.tagsSpecialList.currentItem().text(0)))
            self.update_combo()

    def order_click(self):
        text, flag = QInputDialog.getText(None, "Altera ordem da Etiqueta:", "", QLineEdit.Normal,'')
        if flag and not text == '':
            dbmain.execute_query('UPDATE tags_special set tags_special_order=%s where tags_special_name=%s',
                                 (int(text),self.tagsSpecialList.currentItem().text(0)))
            self.update_combo()

    def exit_click(self):
        self.toto = ''
        self.close()


def main():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    # data_access.get_status()
    app = QApplication(sys.argv)
    form = TagsSpecialBrowser()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
