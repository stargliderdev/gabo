#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib

from PyQt5.QtWidgets import QDesktopWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, \
    QTableWidget, QMenu, QPushButton, QFileDialog, QTableWidgetItem, \
    QWidget, QMainWindow, QApplication, QMessageBox, QStyleFactory, QToolButton, QAction
from PyQt5.QtGui import QIcon

import storage

try:
    from win32api import GetSystemMetrics
    import wmi
except ImportError:
    pass

import ex_grid
import mini_browser
import parameters as gl
import dmPostgreSQL as dbmain

import data_access as data_access
import info as info
import qlib
import tag_browser
import edit_record
import stdio
import input_isbn
import authors
import make_report_html
import report_display
import locals
import lib_gabo

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # centra janela no ecran
        self.centralwidget = QWidget(self)
        self.setWindowIcon(QIcon('./img/books.png'))
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle('Livros')
        # vars
        gl.refresh = False
        gl.SQLglobal = ''
        gl.DATAglobal = ''
        gl.current_path = './'
        print('loading datasets...')
        self.status = ['Todos']
        self.types = ['Todos']
        gl.db_params = stdio.read_config_file('gabo.ini')
        if not gl.db_params[0]:
            QMessageBox.critical(None,
                                 "Erro Fatal",
                                 """O ficheiro de configuração não foi encontrado ou está corrompido!""",
                                 QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
            self.close()
        gl.db_params = gl.db_params[1]
        gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params['db_database'] +\
        ' user=' + gl.db_params['db_user'] + ' password=' +gl.db_params['db_password']
        data_access.get_autores()
        data_access.get_status()
        data_access.get_types()
        data_access.get_params()
        data_access.load_preps()
        data_access.get_areas()
        data_access.get_special_tags()
        data_access.get_locals()
        print('ending loading datasets!')
        self.status.extend(gl.dsStatus)
        self.types.extend(gl.ds_types)
        self.resize(1200, 768)
        self.center()
        gl.DEBUG = True
        QApplication.setStyle(QStyleFactory.create('Fusion'))

                
        mainLayout = QVBoxLayout(self.centralwidget)
        # barra de pesquisa
        """ primeira pesquisa"""
        self.mainSearchCbox = QComboBox()
        self.mainSearchCbox.setMaximumWidth(90)
        self.mainSearchCbox.setMinimumWidth(90)
        self.mainSearchCbox.addItems(['Titulo', 'ISBN', 'tag'])
        self.mainSearchCbox.setCurrentIndex(0)
        
        self.mainToSearchEdt = QLineEdit()
        self.mainToSearchEdt.setMaximumWidth(300)
        self.mainToSearchEdt.setMinimumWidth(300)

        mainSearchBtn = QToolButton()
        mainSearchBtn.setToolTip('Pesquisa texto')
        mainSearchBtn.setIcon(QIcon('./img/search.png'))
        # self.set_icon_size(firstSearchBtn)
        mainSearchBtn.clicked.connect(self.main_search_click)
        
        mainSearchClearBtn = QToolButton()
        mainSearchClearBtn.setToolTip('Limpa Pesquisa')
        mainSearchClearBtn.setIcon(QIcon('./img/clear.png'))
        # self.set_icon_size(firstSearchBtn)
        # mainSearchBtn.clicked.connect(self.main_search_clear_click)
        
        authorsBtn = QToolButton()
        authorsBtn.setToolTip('Autores')
        authorsBtn.setIcon(QIcon('./img/authors.png'))
        authorsBtn.clicked.connect(self.authors_click)

        secondClearBtn = QToolButton()
        secondClearBtn.setToolTip('Limpa Pesquisa')
        secondClearBtn.setIcon(QIcon('./img/clear.png'))
        # self.set_icon_size(secondClearBtn)
        secondClearBtn.clicked.connect(self.second_field_clear_click)
        
        cotasBtn = QToolButton()
        cotasBtn.setToolTip('Cotas Locais')
        cotasBtn.setIcon(QIcon('./img/locals.png'))
        cotasBtn.clicked.connect(self.locals_click)
        
        search_tags_Btn = QToolButton()
        search_tags_Btn.setToolTip('Pesquisa tags')
        search_tags_Btn.setIcon(QIcon('./img/search_tags.png'))
        # self.set_icon_size(search_tags_Btn)
        search_tags_Btn.clicked.connect(self.search_tags_mode_click)
        
        clear_tags_Btn = QToolButton()
        clear_tags_Btn.setToolTip('Limpa Tags')
        clear_tags_Btn.setIcon(QIcon('./img/clear.png'))
        # self.set_icon_size(clear_tags_Btn)
        clear_tags_Btn.clicked.connect(self.clear_tags_search)

        self.tags_browserBtn = QToolButton()
        self.tags_browserBtn.setToolTip('Gere Etiquetas')
        self.tags_browserBtn.setIcon(QIcon('./img/tags.png'))
        # self.set_icon_size(self.tags_browserBtn)
        self.tags_browserBtn.clicked.connect(self.tags_browser_click)
        
        # drop add menu
        bookAddBtn = QPushButton('Novo')
        bookAddBtn.setToolTip('Adiciona Livro')
        bookAddBtn.clicked.connect(self.record_add_click)
        
        bookAddIsbnBtn = QPushButton('Pelo ISBN')
        bookAddIsbnBtn.setToolTip('Adiciona livro pelo ISBN')
        bookAddIsbnBtn.clicked.connect(self.record_add_ISBN_click)
        
        self.addBookBtn = QPushButton()
        self.addBookBtn.setToolTip('Adicionar Livro')
        self.addBookBtn.setIcon(QIcon('./img/addbook.png'))
        
        printBtn = QToolButton()
        printBtn.setIcon(QIcon('./img/print.png'))
        # self.set_icon_size(printBtn)
        printBtn.clicked.connect(self.print_click)
        
        self.last_fiveBtn = QPushButton()
        self.last_fiveBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        self.last_fiveBtn.clicked.connect(self.last_records_click)
        
        double1_Btn = QPushButton()
        double1_Btn.setText('Duplica')
        double1_Btn.clicked.connect(self.double1_click)
        
        clone_Btn = QPushButton()
        clone_Btn.setText('&Clona')
        clone_Btn.clicked.connect(self.clone_click)
        
        aboutBtn = QToolButton()
        aboutBtn.setToolTip('Acerca')
        aboutBtn.setIcon(QIcon('./img/info.png'))
        # self.set_icon_size(aboutBtn)
        aboutBtn.clicked.connect(self.about_click)
        
        closeBtn = QToolButton()
        closeBtn.setToolTip('Sair')
        closeBtn.setIcon(QIcon('./img/close.png'))
        # self.set_icon_size(closeBtn)
        closeBtn.clicked.connect(self.closeBtn_click)
        
        self.sortByCbox = QComboBox()
        self.sortByCbox.setCurrentIndex(0)
        self.sortByCbox.addItems(['Nada', 'Autor', 'Titulo', 'Tipos', 'Local', 'Volume', 'Ano'])
        self.sortByCbox.setCurrentIndex(0)
        self.sortByCbox.currentIndexChanged.connect(self.sort_by_change)
        self.recordLimitEdt = QLineEdit()
        self.recordLimitEdt.setMaximumWidth(40)
        self.recordLimitEdt.setMaxLength(4)
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.recordLimitEdt.editingFinished.connect(self.limit_change)
        
        self.typesCbox = QComboBox()
        self.typesCbox.addItems(self.types)
        self.typesCbox.setCurrentIndex(0)
        self.typesCbox.currentIndexChanged.connect(self.types_change)
        self.statusCbox = QComboBox()
        self.statusCbox.setCurrentIndex(0)

        self.statusCbox.addItems(self.status)
        self.statusCbox.currentIndexChanged.connect(self.status_change)
        widthSumBtn = QToolButton()
        widthSumBtn.setToolTip('Sair')
        widthSumBtn.setIcon(QIcon('./img/width_sigma.png'))
        # self.set_icon_size(widthSumBtn)
        widthSumBtn.clicked.connect(self.width_sum_click)
        
        
        mainLayout.addLayout(qlib.addHLayout(
            [bookAddBtn, bookAddIsbnBtn, self.last_fiveBtn, double1_Btn, clone_Btn,  printBtn, True,
             aboutBtn, closeBtn]))
        mainLayout.addLayout(qlib.addHLayout(
            [self.mainSearchCbox, self.mainToSearchEdt, mainSearchBtn, mainSearchClearBtn, self.tags_browserBtn, authorsBtn, cotasBtn,
             widthSumBtn, True,'Ordena:', self.sortByCbox, 'Tipos', self.typesCbox, 'Estado', self.statusCbox,
             True, True,'Resultados', self.recordLimitEdt]))
             
        
        mainLayout.addLayout(qlib.addHLayout(['AUTOR:eça,POR:nenhum,TIPO:todos,ESTADO:todos',True], 400))
        
        # grid
        self.grid = QTableWidget(self)
        self.grid.setSelectionBehavior(QTableWidget.SelectRows)
        self.grid.setSelectionMode(QTableWidget.SingleSelection)
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.verticalHeader().setDefaultSectionSize(20)
        self.grid.setAlternatingRowColors(True)
        self.grid.verticalHeader().setVisible(False)
        self.grid.setStyleSheet("alternate-background-color: #d2e5ff;")
        self.grid.doubleClicked.connect(self.grid_double_click)
        
        mainLayout.addWidget(self.grid)
        # sub menus
        author_pub = QAction("Obras do Autor", self)
        author_pub.triggered.connect(self.author_pub_click)
        self.grid.addAction(author_pub)
        
        local_pub = QAction("Obras nesta Cota", self)
        local_pub.triggered.connect(self.local_pub_click)
        self.grid.addAction(local_pub)
        self.grid.setContextMenuPolicy(2)
        
        self.last_records_click()
        try:
            if GetSystemMetrics(1) <= 768:
                self.showMaximized()
        except NameError:
            pass
    
    def sort_by_change(self):
        self.filter_cbox_change()
    
    def types_change(self):
        self.filter_cbox_change()
    
    def status_change(self):
        self.filter_cbox_change()
        
    def filter_cbox_change(self):
        
        gl.SEARCH_DICT.update(self.filter_options())
        sql = lib_gabo.make_sql(gl.SEARCH_DICT)
        gl.FILTER_DATASET = dbmain.query_many(sql)
        gl.records_in_ds = len(gl.FILTER_DATASET)
        if gl.records_in_ds == 0:
            self.grid.setRowCount(0)
        else:
            self.update_grid()
    
    
    def author_pub_click(self):
        # a = self.grid.item(self.grid.currentRow(), 2).text()
        # self.mainToSearchEdt.setText(a)
        # self.mainSearchCbox.setCurrentIndex(0)
        # # self.filter_click()
        # self.main_search_click()
        pass

        
    def local_pub_click(self):
        try:
            a = self.grid.item(self.grid.currentRow(), 5).text()
            self.mainToSearchEdt.setText(a)
            self.mainSearchCbox.setCurrentIndex(3)
            self.filter_click()
        except AttributeError:
            pass
    
    def tags_browser_click(self):
        form = tag_browser.BrowserTags()
        form.exec_()
        if not form.tag_list == []:
            self.tags_to_searchEdit.setText(form.tag_list)
            self.mainToSearchEdt.clear()
    
    def double1_click(self):
        # duplica normal
        if self.grid.item(self.grid.currentRow(), 0) is not None:
            form = edit_record.EditRecord(int(self.grid.item(self.grid.currentRow(), 0).text()), '', isbn=False, copy=1)
            form.exec_()
            self.refresh_grid()
    
    def clone_click(self):
        # clona
        if self.grid.item(self.grid.currentRow(), 0) is not None:
            form = edit_record.EditRecord(int(self.grid.item(self.grid.currentRow(), 0).text()), '', isbn=False, copy=2)
            form.exec_()
            # self.refresh_grid()
       
    def authors_click(self):
        form = authors.BrowserAuthors()
        form.exec_()
        if form.toto != '':
            # self.aut.setCurrentIndex(0)
            # self.authorToSearchEdt.setText(form.toto)
            # self.author_search_click()
            gl.records_in_ds = 0
        
            gl.LAST_SEARCH_WHERE = 1
            gl.SEARCH_DICT = {'WHERE': 'author', 'WHAT': form.toto}
            gl.SEARCH_DICT.update(self.filter_options())
            sql = lib_gabo.make_sql(gl.SEARCH_DICT)
            gl.FILTER_DATASET = dbmain.query_many(sql)
            gl.records_in_ds = len(gl.FILTER_DATASET)
            if gl.records_in_ds == 0:
                self.grid.setRowCount(0)
            else:
                self.update_grid()
                
    
    def filter_options(self):
        try:
            del gl.SEARCH_DICT['ORDER']
        except KeyError:
            pass
        try:
            del gl.SEARCH_DICT['TYPE']
        except KeyError:
            pass
        try:
            del gl.SEARCH_DICT['STATUS']
        except KeyError:
            pass
    
        l_dict = {}
        if self.sortByCbox.currentIndex() == 0:
            pass
        else:
            l_dict['ORDER'] = self.sortByCbox.currentText()
        if self.typesCbox.currentIndex() == 0:
            pass
        else:
            l_dict['TYPE'] = self.typesCbox.currentText()
        if self.statusCbox.currentIndex() == 0:
            pass
        else:
            l_dict['STATUS'] = self.statusCbox.currentText()
        return l_dict
    
    def locals_click(self):
        form = locals.BrowserLocals()
        form.exec_()
        if not form.toto == '':
            gl.records_in_ds = 0
            gl.LAST_SEARCH_WHERE = 1
            gl.SEARCH_DICT = {'WHERE': 'local', 'WHAT': form.toto}
            gl.SEARCH_DICT.update(self.filter_options())
            sql = lib_gabo.make_sql(gl.SEARCH_DICT)
            gl.FILTER_DATASET = dbmain.query_many(sql)
            gl.records_in_ds = len(gl.FILTER_DATASET)
            if gl.records_in_ds == 0:
                self.grid.setRowCount(0)
            else:
                self.update_grid()

    def width_sum_click(self):
        # self.local_search_click()
        # lib_gabo.calc_width_in_filter()
        form = storage.StoreMangDialog()
        form.exec_()
        
    def print_click(self):
        hl = make_report_html.main_grid_report(gl.FILTER_DATASET)
        form = report_display.DisplayReport(hl)
        form.exec_()
        
    
    def info_click(self):
        dataset = []
        dataset.append(('Livros', str(dbmain.query_one('select count(pu_id) from livros', (True,))[0])))
        dataset.append(('Autores', str(dbmain.query_one('select count(au_id) from authors', (True,))[0])))
        dataset.append(('Por categoria', ''))
        dataset = dataset + (dbmain.query_many('''select types.ty_name, to_char(count(*),'999999999') as a
            from livros,types
            where types.ty_id = pu_name
            group by pu_name,types.ty_name
            order by ty_name asc'''))
        self.grid.setRowCount(len(dataset))
        ex_grid.ex_grid_update(self.grid, {0: ['Tabela', 's'], 1: ['Total', 'sr']}, dataset)
    
    def last_records_click(self):
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.mainSearchCbox.setCurrentIndex(0)
        # self.firstToSearchEdt.setText('')
        # self.tags_to_searchEdit.setText('')
        self.typesCbox.setCurrentIndex(0)
        sql = '''SELECT
          livros.pu_id,
          livros.pu_title,
          authors.au_name,
          types.ty_name,
          status.st_nome,
          livros.pu_cota,
          livros.pu_volume,
          pu_ed_year
        FROM
          livros, authors, types, status
        WHERE'''
        if self.typesCbox.currentIndex() != 0:
            sql += ' livros.pu_type = (select ty_id from types where ty_name like \'' + str(
                self.typesCbox.currentText()) + '\') and '
        
        if self.statusCbox.currentIndex() != 0:
            sql += """ livros.pu_status = (select st_id from status where st_nome like \'""" + str(
                self.statusCbox.currentText()) + """"\') and """
        
        sql += """  livros.pu_status = status.st_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
        ORDER BY pu_id DESC LIMIT """ + gl.SHOW_RECORDS + ";"
       
        gl.FILTER_DATASET = dbmain.query_many(sql)
       
        self.update_grid()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)

    def show_delete_click(self):
        sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome, livros.pu_cota, livros.pu_volume
        FROM livros, authors, types, status  WHERE'''
        sql += ' livros.pu_author_id =0 and livros.pu_type > 0 and livros.pu_status > 0 and '
        sql += '''  livros.pu_status = status.st_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
          ORDER BY pu_id desc;'''
        gl.FILTER_DATASET = dbmain.query_many(sql)
        self.update_grid()
    
    def refresh_grid(self):
        # """refresh grid by filters"""
        # """ if filter empty go to last records"""
        # self.main_search_click()
        # if gl.records_in_ds == 0:
        #     self.search_tags_mode_click()
        # if gl.records_in_ds == 0:
        #     self.last_records_click()
        pass
    
    def about_click(self):
        bc = """<!DOCTYPE html><html lang="pt_pt"><meta name="viewport" content="width=device-width, initial-scale=1">
         <p style="text-align:center;">
         <img src="./info.png" ></p> <p>"""
        bc +="Versão " + gl.VERSION + '<br>'
        bc +="Utilizador " + gl.OWNER
        bc +="""</p></html>"""
        form = mini_browser.BrowserView('SysInfo', bc)
        form.exec_()
        
    def closeBtn_click(self):
        self.close()
    

    def make_sql(self, what='', where_index='nada'):
        # v2.5
        
        # gl.CURRENT_SQL = ''
        # select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year FROM livros, authors, types, status"
        # join_ = " livros.pu_status = status.st_id AND authors.au_id = livros.pu_author_id AND types.ty_id = livros.pu_type "
        # where_ = ' WHERE '
        # order_ = ''
        # search_ = ''
        # limit_ = ''
        # where_index = where_index.lower()
        # self.key_sort = self.sort_dic[self.sortByCbox.currentText().lower()]
        # if not what == '':
        #     self.recordLimitEdt.setText('0')
        #     # self.key_search = self.sort_dic[where_index]
        #     if where_index == 'local': # na cota tem de ser exactamente igual
        #         self.key_search = self.sort_dic['local']
        #         text_to_search = "\'" + what.lower().strip() + "\'"
        #     else:
        #         text_to_search = "\'%" + what.lower().strip() + "%\'"
        #
        #     if len(text_to_search) > 1:
        #         where_ += '''unaccent(lower(''' + self.key_search + ''')) LIKE  unaccent(''' + text_to_search + ''') AND '''
        #     else:
        #         where_ += ''' unaccent(upper(''' + self.key_search + ''')) SIMILAR TO ''' + '''unaccent(''' + text_to_search.upper() + ')' + ''' AND '''
        # elif  not self.tags_to_searchEdit.text() =='': # modo para tags
        #     self.recordLimitEdt.setText('0')
        #     tags = self.tags_to_searchEdit.text().replace("\'", "\\\'")
        #     tags = tags.split(',')
        #     in_data = ''
        #     if self.logicTags.currentIndex() == 0:  # ou
        #         for n in tags:
        #             toto = n.lower().strip()
        #             in_data += "unaccent(\'" + toto + "\'),"
        #         a = dbmain.query_many(
        #             '''select ta_id from tags where unaccent(ta_name) in (''' + in_data[:-1] + ''')''')
        #         i = []
        #         for t in a:
        #             i.append(t[0])
        #         if i:
        #             i = str(i)
        #             where_ += '''
        #                  pu_id in(select * from (select tr_book from tag_ref where tr_tag in(''' + i[1:-1] + ''')) as foo) AND '''
        #         else:
        #             where_ += '''pu_id in(select * from (select tr_book from tag_ref where tr_tag in(-1)) as foo) AND '''
        #     else:
        #         t = ''
        #         for n in tags:
        #             t = t + "\'" + n.strip() + "\',"
        #         t = t[:-1]
        #         c = str(len(tags))
        #         where_ = ''' where EXISTS (SELECT NULL
        #          FROM tag_ref tg
        #          JOIN TAGS t ON t.ta_id = tg.tr_tag
        #         WHERE unaccent(t.ta_name) IN (unaccent(''' + t + '''))
        #           AND tg.tr_book = livros.pu_id
        #      GROUP BY tg.tr_book
        #        HAVING COUNT(t.ta_name) =''' + c + ''') and '''
        # else:  # não procura em nada
        #     where_ += ''' livros.pu_status = status.st_id AND
        #   authors.au_id = livros.pu_author_id AND
        #   types.ty_id = livros.pu_type and '''
        #     self.key_sort = self.sort_dic[self.sortByCbox.currentText().lower()]
        #
        # if self.types_filterCbox.currentIndex() != 0:
        #     where_ += " livros.pu_type = (select ty_id from types where ty_name like \'" + str(
        #         self.types_filterCbox.currentText()) + '\') and '
        #
        # if self.status_filterCbox.currentIndex() != 0:
        #     where_ += " livros.pu_status = (select st_id from status where st_nome like \'" + str(
        #         self.status_filterCbox.currentText()) + "\') and "
        #
        # order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
        #
        # if int(gl.SHOW_RECORDS) > 0: #  int(self.recordLimitEdt.text()) > 0:
        #     limit_ = 'LIMIT ' + gl.SHOW_RECORDS
        #     order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
        # else:
        #     self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        #     limit_ = 'LIMIT 99999'
        # sql = select_ + where_ + join_ + order_ + limit_
        # gl.CURRENT_SQL = sql

        return ''
    
    def limit_change(self):
        gl.SHOW_RECORDS = self.recordLimitEdt.text()
        try:
            dum = int(gl.SHOW_RECORDS)
        except ValueError:
            gl.SHOW_RECORDS='80'
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        data_access.save_param('SHOW_RECORDS', gl.SHOW_RECORDS)
        self.sortByCbox.setCurrentIndex(0)
        self.typesCbox.setCurrentIndex(0)
        self.last_fiveBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        self.filter_click()
    
    

    
    def filter_click(self):
        foo = self.make_sql()
        gl.FILTER_DATASET = dbmain.query_many(foo)
        gl.records_in_ds = len(gl.FILTER_DATASET)
        self.update_grid()
        
    def main_search_click(self):
        if not self.mainToSearchEdt.text() == '':
            print(self.mainSearchCbox.currentText())
            if self.mainSearchCbox.currentIndex() == 0:
                gl.SEARCH_DICT = {'WHERE': 'title', 'WHAT': self.mainToSearchEdt.text()}
            elif self.mainSearchCbox.currentIndex() == 1:
                gl.SEARCH_DICT = {'WHERE': 'isbn', 'WHAT': self.mainToSearchEdt.text()}
            gl.SEARCH_DICT.update(self.filter_options())
            sql = lib_gabo.make_sql(gl.SEARCH_DICT)           
            gl.FILTER_DATASET = dbmain.query_many(sql)
            gl.records_in_ds = len(gl.FILTER_DATASET)
            if gl.records_in_ds == 0:
                self.grid.setRowCount(0)
            else:
                self.update_grid()

    
    def main_search_clear_click(self):
        self.mainToSearchEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
        
    # def author_search_click(self):
    #     gl.records_in_ds = 0
    #     if not self.authorToSearchEdt.text() == '':
    #         gl.LAST_SEARCH_WHERE = 1
    #         # self.firstToSearchEdt.clear()
    #         # self.localToSeachEdt.clear()
    #         # sql = lib_gabo.make_sql_author(self.authorToSearchEdt.text(), self.sortByCbox.currentText().lower(),
    #         #                                self.typesCbox.currentText().lower(), self.statusCbox.currentText().lower())
    #         sql = lib_gabo.make_sql({'WHERE':'author', 'WHAT': })
    #         gl.FILTER_DATASET = dbmain.query_many(sql)
    #         gl.records_in_ds = len(gl.FILTER_DATASET)
    #         if gl.records_in_ds == 0:
    #             self.grid.setRowCount(0)
    #         else:
    #             self.update_grid()
    
    # def local_search_click(self):
    #     gl.records_in_ds = 0
    #     if not self.localToSeachEdt.text() == '':
    #         gl.LAST_SEARCH_WHERE = 2
    #         # self.firstToSearchEdt.clear()
    #         # self.authorToSearchEdt.clear()
    #         sql = lib_gabo.make_sql_local(self.localToSeachEdt.text(),self.sortByCbox.currentText().lower(),
    #                                        self.typesCbox.currentText().lower(), self.statusCbox.currentText().lower() )
    #         gl.FILTER_DATASET = dbmain.query_many(sql)
    #         gl.records_in_ds = len(gl.FILTER_DATASET)
    #         if gl.records_in_ds == 0:
    #             self.grid.setRowCount(0)
    #         else:
    #             self.update_grid()
    
    def third_field_clear_click(self):
        self.localToSeachEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
    
    def search_tags_mode_click(self):
        if not self.tags_to_searchEdit.text() == '':
            self.mainToSearchEdt.setText('')
            sql = self.make_sql()
            gl.FILTER_DATASET = dbmain.query_many(sql)
            if len(gl.FILTER_DATASET) == 0:
                self.grid.setRowCount(0)
            else:
                self.update_grid()
   
    def record_add_ISBN_click(self):
        form = input_isbn.InputIsbn()
        form.exec_()
        self.last_records_click()
    
    def record_add_click(self, isbn=False):
        form = edit_record.EditRecord(-1, '', isbn=False)
        form.exec_()
        self.refresh_grid()
    
    def get_data(self):
        sql = '''SELECT
          livros.pu_id,
          livros.pu_title,
          authors.au_name,
          types.ty_name,
          status.st_nome,
          livros.pu_cota,livros.pu_volume, pu_ed_year
        FROM
          livros, authors, types, status
        WHERE
          livros.pu_status = status.st_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
        ORDER BY
          livros.pu_title ASC LIMIT 50;'''
        a = dbmain.query_many(sql)
        gl.FILTER_DATASET = a  # é global para que possa ser utilizado nos relatorios em html
        return gl.FILTER_DATASET
    
    def grid_double_click(self):
        stack_current_row =self.grid.currentRow()
        form = edit_record.EditRecord(int(self.grid.item(self.grid.currentRow(), 0).text()), '', isbn=False)
        form.exec_()
        # if not self.firstToSearchEdt.text() == '':
        #     # self.recordLimitEdt.setText('999')
        #     foo = self.make_sql(self.firstToSearchEdt.text(), self.firstSearchCbox.currentText())
        # elif not self.authorToSearchEdt.text() == '':
        #     foo = self.make_sql(self.authorToSearchEdt.text(), self.authorSearchBtn.currentText())
        #     gl.FILTER_DATASET = dbmain.query_many(foo)
        #     self.update_grid()
        # elif not self.localToSeachEdt.text() == '':
        #     foo = self.make_sql(self.localToSeachEdt.text(), self.localSearchBtn.currentText())
        #     gl.FILTER_DATASET = dbmain.query_many(foo)
        #     self.update_grid()
        # elif not self.tags_to_searchEdit.text() == '':
        #     foo = self.make_sql()
        #     gl.FILTER_DATASET = dbmain.query_many(foo)
        #     self.update_grid()
        # else:
        #     self.last_records_click()
        # self.grid.setCurrentCell(stack_current_row,0)
        
    def refresh_search(self):
        pass
    
    def second_field_clear_click(self):
        self.authorToSearchEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
    
    def clear_tags_search(self):
        self.tags_to_searchEdit.clear()
    
    def update_grid(self):
        ex_grid.ex_grid_update(self.grid, {0: ['Num', 'i'], 1: ['Titulo', 's'], 2: ['Autor', 's'], 3: ['Tipo', 's'],
                                           4: ['Estado', 's'], 5: ['Cota', 's'], 6: ['Vol.', 'i'], 7: ['Ano', 'i']},
                               gl.FILTER_DATASET)
        self.grid.setColumnWidth(0, 50)
        self.grid.setColumnWidth(1, 450)
        self.grid.setColumnWidth(2, 250)
        self.grid.setColumnWidth(3, 160)
    
    def addCell2Grid(self, line, col, text):
        item = QTableWidgetItem()
        self.grid.setItem(line, col, item)
        item.setText(self.campo2String(text))
    
    def saveFile(self, file2save):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, "Grava Ficheiro", '/home', "Ficheiros CSV (csv)")
        fileName += '.csv'
        f = open(fileName, 'w')
        f.write(file2save)
        f.close()
    
    def exit(self):
        self.close()
    
    def about(self):
        form = info.SystemInfo()
        form.exec_()
    
    def campo2String(self, campo):
        if campo == None:
            return ''
        elif type(campo) == int:
            return str(campo)
        else:
            return campo
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_icon_size(self, obx):
        obx.setMaximumWidth(30)
        obx.setMinimumHeight(30)
        obx.setMaximumHeight(30)
        obx.setMinimumWidth(30)

def internet_on():
    try:
        response = urllib.request.urlopen('http://74.125.113.99', timeout=1)
        return True
    except urllib.error.URLError as err: pass
    return False

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

main()
