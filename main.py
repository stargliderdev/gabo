#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import urllib
import datetime

from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QLineEdit, QComboBox, \
    QTableWidget,  QPushButton, QFileDialog, QTableWidgetItem, \
    QWidget, QMainWindow, QApplication, QMessageBox, QStyleFactory, QToolButton, QAction
from PyQt5.QtGui import QIcon

import bindings
import browser
import classifications
import conditions
import languages
import main_grid_layout
import pub_types
import status
import storage
import tags_manage
import tags_special_manage

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
import options_new
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
        self.status = ['Todos']
        self.types = ['Todos']
        gl.db_params = stdio.read_config_file('gabo.ini')
        print('     database engine:' + gl.db_params['db_engine'])
        print('     database server:' + gl.db_params['db_host'])
        print('   database database:' + gl.db_params['db_database'])
        print('database sqlite path:' + gl.db_params['db_path'])
        gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params['db_database'] + \
                         ' user=' + gl.db_params['db_user'] + ' password=' +gl.db_params['db_password']
        if dbmain.check_alive():
            pass
        else:
            QMessageBox.critical(None,
                                 "Erro Fatal",
                                 """A base de dados não foi encontrada!""",
                                 QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
            self.close()
        if gl.db_params == {}:
            QMessageBox.critical(None,
                                 "Erro Fatal",
                                 """O ficheiro de configuração não foi encontrado ou está corrompido!""",
                                 QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
            self.close()
        else:
            print('loading datasets...')
            # gl.db_params = gl.db_params[1]
            data_access.get_autores()
            data_access.get_status()
            data_access.get_types()
            data_access.load_parameters()
            data_access.load_prepositions()
            data_access.get_areas()
            data_access.get_special_tags()
            data_access.get_locals()
            data_access.get_conditions()
            data_access.get_classifications()
            data_access.get_languages()
            data_access.get_bindings()
            print('ending loading datasets!')
        self.status.extend(gl.status_list)
        self.types.extend(gl.types_list)
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
        self.mainSearchCbox.addItems(['Titulo','Autor', 'ISBN', 'Etiqueta'])
        self.mainSearchCbox.setCurrentIndex(0)
    
        self.mainToSearchEdt = QLineEdit()
        self.mainToSearchEdt.setMaximumWidth(300)
        self.mainToSearchEdt.setMinimumWidth(300)
        self.mainToSearchEdt.returnPressed.connect(self.main_search_click)
    
        mainSearchBtn = QToolButton()
        mainSearchBtn.setToolTip('Pesquisa')
        mainSearchBtn.setIcon(QIcon('./img/search.png'))
        # self.set_icon_size(firstSearchBtn)
        mainSearchBtn.clicked.connect(self.main_search_click)
    
        mainSearchClearBtn = QToolButton()
        mainSearchClearBtn.setToolTip('Limpa Pesquisa')
        mainSearchClearBtn.setIcon(QIcon('./img/clear.png'))
        mainSearchClearBtn.clicked.connect(self.main_search_clear_click)
    
        """ tool buttons """
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
    
        tags_specialBtn = QToolButton()
        tags_specialBtn.setToolTip('Gere Etiquetas Especiais')
        # self.tags_specialBtn.setIcon(QIcon('./img/tags.png'))
        # self.set_icon_size(self.tags_browserBtn)
        tags_specialBtn.clicked.connect(self.tags_special_browser_click)
    
        # drop add menu
        bookAddBtn = QPushButton('Novo')
        bookAddBtn.setToolTip('Adiciona Livro')
        bookAddBtn.clicked.connect(self.record_add_click)
    
        bookAddIsbnBtn = QPushButton('Wook')
        bookAddIsbnBtn.setToolTip('Adiciona livro pela WOOK')
        bookAddIsbnBtn.clicked.connect(self.record_add_wook_click)
    
        self.addBookBtn = QPushButton()
        self.addBookBtn.setToolTip('Adicionar Livro')
        self.addBookBtn.setIcon(QIcon('./img/addbook.png'))
    
        printBtn = QToolButton()
        printBtn.setIcon(QIcon('./img/print.png'))
        # self.set_icon_size(printBtn)
        printBtn.clicked.connect(self.print_click)
    
        navigatorBtn = QPushButton('Navegador')
        navigatorBtn.clicked.connect(self.navigator_click)
    
        self.lastRecordsBtn = QPushButton()
        self.lastRecordsBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        self.lastRecordsBtn.clicked.connect(self.last_records_click)
    
        double1_Btn = QPushButton()
        double1_Btn.setText('Duplica')
        double1_Btn.clicked.connect(self.double1_click)
    
        clone_Btn = QPushButton()
        clone_Btn.setText('&Clona')
        clone_Btn.clicked.connect(self.clone_click)
        # tabelas acessórias
        languageBtn = QToolButton()
        languageBtn.setToolTip('Idiomas')
        languageBtn.setIcon(QIcon('./img/languages.png'))
        languageBtn.clicked.connect(self.languages_click)
    
        coverBtn = QToolButton()
        coverBtn.setToolTip('Encadernação')
        coverBtn.setIcon(QIcon('./img/binding.png'))
        coverBtn.clicked.connect(self.binding_click)
    
        statusBtn = QToolButton()
        statusBtn.setToolTip('Situação')
        statusBtn.setIcon(QIcon('./img/status.png'))
        statusBtn.clicked.connect(self.status_click)
    
        conditionBtn = QToolButton()
        conditionBtn.setToolTip('Condição Fisica')
        conditionBtn.setIcon(QIcon('./img/conditions.png'))
        conditionBtn.clicked.connect(self.conditions_click)
    
        ratingBtn = QToolButton()
        ratingBtn.setToolTip('Classificação')
        ratingBtn.setIcon(QIcon('./img/classification.png'))
        ratingBtn.clicked.connect(self.classification_click)
    
        typeBtn = QToolButton()
        typeBtn.setToolTip('Tipo de Publicação')
        typeBtn.setIcon(QIcon('./img/pub_types.png'))
        typeBtn.clicked.connect(self.pub_types_click)
    
        backupBtn = QToolButton()
        backupBtn.setToolTip('Backup da base de dados')
        backupBtn.setIcon(QIcon('./img/info.png'))
        backupBtn.clicked.connect(self.database_backup)
    
        aboutBtn = QToolButton()
        aboutBtn.setToolTip('Acerca')
        aboutBtn.setIcon(QIcon('./img/info.png'))
        aboutBtn.clicked.connect(self.about_click)
    
        closeBtn = QToolButton()
        closeBtn.setToolTip('Sair')
        closeBtn.setIcon(QIcon('./img/close.png'))
        closeBtn.clicked.connect(self.closeBtn_click)
        self.recordLimitEdt = QLineEdit()
        self.recordLimitEdt.setMaximumWidth(40)
        self.recordLimitEdt.setMaxLength(4)
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.recordLimitEdt.editingFinished.connect(self.limit_change)
    
        self.typesCbox = QComboBox()
        self.typesCbox.addItems(gl.TYPES_FILTER_LIST)
        self.typesCbox.setCurrentIndex(0)
        self.typesCbox.currentIndexChanged.connect(self.filter_cbox_change)
        self.statusCbox = QComboBox()
        self.statusCbox.setCurrentIndex(0)
        self.statusCbox.addItems(gl.STATUS_FILTER_LIST)
        self.statusCbox.currentIndexChanged.connect(self.filter_cbox_change)
        # widthSumBtn = QToolButton()
        # widthSumBtn.setToolTip('Espaço')
        # widthSumBtn.setIcon(QIcon('./img/width_sigma.png'))
        # widthSumBtn.clicked.connect(self.width_sum_click)
    
        mangeColumnsBtn = QToolButton()
        mangeColumnsBtn.setToolTip('Colunas visiveis')
        mangeColumnsBtn.setIcon(QIcon('./img/info.png'))
        mangeColumnsBtn.clicked.connect(self.show_columns_click)
    
        mainLayout.addLayout(qlib.addHLayout([bookAddBtn, bookAddIsbnBtn, self.lastRecordsBtn, printBtn, navigatorBtn, True,
                                              languageBtn, coverBtn, statusBtn, conditionBtn, ratingBtn, typeBtn, True,
                                              backupBtn, aboutBtn, closeBtn]))
        mainLayout.addLayout(qlib.addHLayout(
            [self.mainSearchCbox, self.mainToSearchEdt, mainSearchBtn, mainSearchClearBtn, self.tags_browserBtn, authorsBtn, cotasBtn,
             True, 'Tipos', self.typesCbox, 'Estado', self.statusCbox,tags_specialBtn,
             True, 'Registos', self.recordLimitEdt],60))
        mainLayout.addLayout(qlib.addHLayout(
            [ True, mangeColumnsBtn],60))
        # grid
        self.mainGrid = QTableWidget(self)
        self.mainGrid.setSelectionBehavior(QTableWidget.SelectRows)
        self.mainGrid.setSelectionMode(QTableWidget.SingleSelection)
        self.mainGrid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.mainGrid.verticalHeader().setDefaultSectionSize(20)
        self.mainGrid.setAlternatingRowColors(True)
        self.mainGrid.verticalHeader().setVisible(False)
        self.mainGrid.setStyleSheet("alternate-background-color: #d2e5ff;")
        self.mainGrid.doubleClicked.connect(self.grid_double_click)
        self.mainGrid.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
    
        mainLayout.addWidget(self.mainGrid)
        # sub menus
        author_pub = QAction("Obras do Autor", self)
        author_pub.triggered.connect(self.author_pub_click)
        self.mainGrid.addAction(author_pub)
    
        local_pub = QAction("Obras nesta Cota", self)
        local_pub.triggered.connect(self.local_pub_click)
        self.mainGrid.addAction(local_pub)
        self.mainGrid.setContextMenuPolicy(2)
    
        self.last_records_click()
        try:
            if GetSystemMetrics(1) <= 768:
                self.showMaximized()
        except NameError:
            pass
        
    def filter_cbox_change(self):
        if self.typesCbox.currentIndex() == 0:
            gl.SEARCH_DICT['TYPE'] = ''
        else:
            gl.SEARCH_DICT['TYPE'] = self.typesCbox.currentText()
        if self.statusCbox.currentIndex() == 0:
            gl.SEARCH_DICT['STATUS'] = ''
        else:
            gl.SEARCH_DICT['STATUS'] = self.statusCbox.currentText()
        self.update_grid()
    
    def author_pub_click(self):
        author = self.mainGrid.item(self.mainGrid.currentRow(), 2).text()
        gl.RECORDS_IN_DATASET = 0
        gl.LAST_SEARCH_WHERE = 1
        gl.SEARCH_DICT['LAST'] = 0
        gl.SEARCH_DICT['WHERE'] = 'author'
        gl.SEARCH_DICT['WHAT'] = author
        self.update_grid()
        
    def local_pub_click(self):
        locals = self.mainGrid.item(self.mainGrid.currentRow(), 5).text()
        gl.RECORDS_IN_DATASET = 0
        gl.LAST_SEARCH_WHERE = 1
        gl.SEARCH_DICT['LAST'] = 0
        gl.SEARCH_DICT['WHERE'] = 'local'
        gl.SEARCH_DICT['WHAT'] = locals
        self.update_grid()
    
    def tags_browser_click(self):
        form = tags_manage.BrowserTags(from_book=False)
        form.exec_()
        if not form.tag_list == []:
            self.mainToSearchEdt.setText(form.tag_list)
            # self.mainToSearchEdt.clear()
            self.mainSearchCbox.setCurrentIndex(3)
            self.main_search_click()
            
    def tags_special_browser_click(self):
        form = tags_special_manage.TagsSpecialBrowser()
        form.exec_()
    
    def double1_click(self):
        # duplica normal
        if self.mainGrid.item(self.mainGrid.currentRow(), 0) is not None:
            form = edit_record.EditRecord(int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text()), '', draft_data=False, copy=1)
            form.exec_()
            self.update_grid()
    
    def clone_click(self):
        # clona
        if self.mainGrid.item(self.mainGrid.currentRow(), 0) is not None:
            book_id = int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text())
            new_book_id = dbmain.clone_livros(book_id)
            form = edit_record.EditRecord(new_book_id, '', copy=2)
            form.exec_()
            self.update_grid()
       
    def authors_click(self):
        form = authors.BrowserAuthors()
        form.exec_()
        if form.toto != '':
            gl.RECORDS_IN_DATASET = 0
            gl.LAST_SEARCH_WHERE = 1
            gl.SEARCH_DICT['WHERE'] = 'author'
            gl.SEARCH_DICT['WHAT'] = form.toto
            gl.SEARCH_DICT['LAST'] = 0
            self.mainSearchCbox.setCurrentIndex(1)
            self.mainToSearchEdt.setText(form.toto)
            self.update_grid()
            
    def locals_click(self):
        form = locals.BrowserLocals()
        form.exec_()
        if not form.toto == '':
            gl.RECORDS_IN_DATASET = 0
            gl.LAST_SEARCH_WHERE = 1
            gl.SEARCH_DICT['WHERE'] = 'local'
            gl.SEARCH_DICT['WHAT'] = form.toto
            self.update_grid()

    def width_sum_click(self):
        form = storage.StoreMangDialog()
        form.exec_()
        
    def print_click(self):
        hl = make_report_html.main_grid_report(gl.MAIN_DATASET)
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
        self.mainGrid.setRowCount(len(dataset))
        ex_grid.ex_grid_update(self.mainGrid, {0: ['Tabela', 's'], 1: ['Total', 'sr']}, dataset)
    
    def show_columns_click(self):
        gl.GRID_COLUMN_SIZES = []
        for n in range(0,self.mainGrid.columnCount()):
            a = self.mainGrid.columnWidth(n)
            gl.GRID_COLUMN_SIZES.append((n, a))
        form = main_grid_layout.MainGridConfig()
        form.exec_()
        if form.toto:
            for n in range(0, len(gl.GRID_COL_NAMES)):
                self.mainGrid.setColumnWidth(n, gl.GRID_COLUMN_SIZES[n][1])
        else:
            pass
    
    
    def last_records_click(self):
        gl.SHOW_RECORDS = self.recordLimitEdt.text()
        try:
            dum = int(gl.SHOW_RECORDS)
        except ValueError:
            gl.SHOW_RECORDS='80'
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        data_access.save_parameters('SHOW_RECORDS', gl.SHOW_RECORDS)
        self.typesCbox.setCurrentIndex(0)
        self.lastRecordsBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        gl.SEARCH_DICT['LAST'] = int(gl.SHOW_RECORDS)
        self.mainToSearchEdt.clear()
        self.update_grid()

    def show_delete_click(self):
        sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.status_name, livros.pu_cota, livros.pu_volume
        FROM livros, authors, types, status  WHERE'''
        sql += ' livros.pu_author_id =0 and livros.pu_type > 0 and livros.pu_status > 0 and '
        sql += '''  livros.pu_status = status.status_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
          ORDER BY pu_id desc;'''
        gl.MAIN_DATASET = dbmain.query_many(sql)
        self.update_grid()
    


    def about_click(self):
        bc = """<!DOCTYPE html><html lang="pt_pt"><meta name="viewport" content="width=device-width, initial-scale=1">
         """
        bc +="Versão " + gl.VERSION + '<br>'
        bc +="database engine:" + gl.db_params['db_engine'] + '<br>'
        bc +="database sqlite path:" + gl.db_params['db_path'] + '<br>'
        bc +="database host:" + gl.db_params['db_host'] + '<br>'
        bc +="database name:" + gl.db_params['db_database'] + '<br>'
        bc +="database pg_dump:" + gl.db_params['db_pg_dump'] + '<br>'
        bc +="""</p></html>"""
        form = mini_browser.BrowserView('SysInfo', bc)
        form.exec_()
    
    def languages_click(self):
        form = languages.LanguagesBrowser()
        form.exec_()
    
    def binding_click(self):
        form = bindings.BindingsBrowser()
        form.exec_()
    
    def status_click(self):
        form = status.StatusBrowser()
        form.exec_()
    
    def conditions_click(self):
        form = conditions.ConditionsBrowser()
        form.exec_()
        
    def classification_click(self):
        form = classifications.ClassificationsBrowser()
        form.exec_()
    
    def pub_types_click(self):
        form = pub_types.TypesBrowser()
        form.exec_()
    
    def database_backup(self):
        now = datetime.datetime.now()
        date_string = now.strftime('%Y%b%d_%H%M')
        print('db backup')
        if gl.db_params['db_engine'] == 'PSQL':
            # print(gl.db_params['db_pg_dump'])
            # # C:\Program Files\pgAdmin III\1.28\pg_dump.exe -h localhost -U "root" --format custom --blobs --verbose --file "c:\tmp\livros_2022-07-27.backup" "livros"
            # print()
            # print(gl.db_params['db_pg_dump'] + '\pg_dump.exe -h ' + gl.db_params['db_host'] + ' -U ' + gl.db_params['db_user']
            #       + ' --format custom --blobs --verbose --file ' + gl.db_params['backup_dir'] + '\\' + gl.db_params['db_database'] + "_" + date_string +".backup" + ' ' + gl.db_params['db_database'])
            call_pg_dump = gl.db_params['db_pg_dump'] + '\pg_dump.exe -h ' + gl.db_params['db_host'] + ' -U ' + gl.db_params['db_user']\
                + ' --format custom --blobs --verbose --file ' + gl.db_params['backup_dir'] + '\\' + gl.db_params['db_database'] + "_" + date_string + ".backup" + ' ' + gl.db_params['db_database']
    
            os.system(call_pg_dump)
            result = QMessageBox.information(None,
                                             "Cópia de Segurança ","Cópia de Segurança efectuada para\n" + gl.db_params['backup_dir']
                                             + '\nCom o nome:' + gl.db_params['db_database'] + "_" + date_string + ".backup",
                                             QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
            
    def closeBtn_click(self):
        self.close()
    
    def limit_change(self):
        gl.SHOW_RECORDS = self.recordLimitEdt.text()
        try:
            dum = int(gl.SHOW_RECORDS)
        except ValueError:
            gl.SHOW_RECORDS='80'
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        data_access.save_parameters('SHOW_RECORDS', gl.SHOW_RECORDS)
        self.typesCbox.setCurrentIndex(0)
        self.lastRecordsBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        self.update_grid()
    
        
    def clear_search(self):
        self.mainToSearchEdt.clear()
        self.update_grid()
    
    def main_search_click(self):
        """will search in title, tags and ISBN"""
        if not self.mainToSearchEdt.text() == '':
            gl.SEARCH_DICT['LAST'] = 0
            if self.mainSearchCbox.currentIndex() == 0: # title
                gl.SEARCH_DICT['WHERE'] = 'title'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 1: # author
                gl.SEARCH_DICT['WHERE'] = 'author'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 2: # ISBN
                gl.SEARCH_DICT['WHERE'] = 'isbn'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 3: # tags
                gl.SEARCH_DICT['WHERE'] = 'tags_or'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            self.update_grid()
   
    def main_search_clear_click(self):
        self.mainToSearchEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
        
    
    def third_field_clear_click(self):
        self.localToSeachEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
    
    def search_tags_mode_click(self):
        if not self.tags_to_searchEdit.text() == '':
            self.mainToSearchEdt.setText('')
            self.update_grid()
   
    def record_add_wook_click(self):
        form = browser.BrowserInLine("https://www.wook.pt/")
        form.exec_()
        self.last_records_click()
        
    def record_add_click(self):
        gl.record_current_dict = {}
        gl.TAGS_SPECIAL_LEVEL1_DATA = []
        form = edit_record.EditRecord(-1, draft_data=False)
        form.exec_()
        self.update_grid()
    
    def get_data(self):
        sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.status_name,
          livros.pu_cota,livros.pu_volume, pu_ed_year
        FROM
          livros, authors, types, status
        WHERE
          livros.pu_status = status.status_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
        ORDER BY
          livros.pu_title ASC LIMIT 50;'''
        a = dbmain.query_many(sql)
        gl.MAIN_DATASET = a  # é global para que possa ser utilizado nos relatorios em html
        return gl.MAIN_DATASET
    
    
    def grid_double_click(self):
        stack_current_row =self.mainGrid.currentRow()
        form = edit_record.EditRecord(int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text()), draft_data=False)
        form.exec_()
        self.update_grid()

    def on_header_clicked(self, col_index):
        gl.GRID_COL_NAMES = gl.GRID_COL_NAMES_ORG[:]
        if gl.SEARCH_DICT['LAST'] == 0:
            if col_index == gl.COLUMN_SORT[0]:
                pass
            else:
                gl.COLUMN_SORT = (0, 0)
            if gl.COLUMN_SORT[1] == 0:
                gl.COLUMN_SORT = (col_index,1)
                gl.SEARCH_DICT['ORDER'] = gl.FIELDS_ORDER_DIC[gl.GRID_COL_NAMES_ORG[col_index].lower()]
                gl.SEARCH_DICT['ORDER_BY'] = 'DESC'
                gl.GRID_COL_NAMES[col_index] = gl.GRID_COL_NAMES[col_index] + ' ⬇'
            elif gl.COLUMN_SORT[1] == 1:
                gl.COLUMN_SORT = (col_index,2)
                gl.SEARCH_DICT['ORDER'] = gl.FIELDS_ORDER_DIC[gl.GRID_COL_NAMES_ORG[col_index].lower()]
                gl.SEARCH_DICT['ORDER_BY'] = 'ASC'
                gl.GRID_COL_NAMES[col_index] = gl.GRID_COL_NAMES[col_index] + ' ⬆'
            else:
                gl.COLUMN_SORT = (0,0)
                gl.SEARCH_DICT['ORDER'] = ''
                gl.SEARCH_DICT['ORDER_BY'] = 'DESC'
                gl.GRID_COL_NAMES = gl.GRID_COL_NAMES_ORG[:]
        else:
            gl.GRID_COL_NAMES = gl.GRID_COL_NAMES[:]
            gl.COLUMN_SORT = (0, 0)
        self.update_grid()
        self.mainGrid.setHorizontalHeaderLabels(gl.GRID_COL_NAMES)
        
        
    def navigator_click(self):
        try:
            gl.NAVIGATOR_INDEX = []
            a = int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text())
            for line in range(0, self.mainGrid.rowCount()):
                gl.NAVIGATOR_INDEX.append((line, int(self.mainGrid.item(line, 0).text())))
            form = edit_record.EditRecord(int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text()),draft_data=False, navigator= self.mainGrid.currentRow())
            form.exec_()
            self.update_grid()
        except AttributeError:
            pass
    
    def second_field_clear_click(self):
        self.authorToSearchEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
    
    def clear_tags_search(self):
        self.tags_to_searchEdit.clear()
    
    def update_grid(self):
        sql = lib_gabo.make_sql(gl.SEARCH_DICT)
        gl.MAIN_DATASET = dbmain.query_many(sql)
        gl.RECORDS_IN_DATASET = len(gl.MAIN_DATASET)
        if gl.RECORDS_IN_DATASET == 0:
            self.mainGrid.setRowCount(0)
        else:
            ex_grid.ex_grid_update(self.mainGrid, {0: ['Num', 'i'], 1: ['Titulo', 's'], 2: ['Autor', 's'], 3: ['Tipo', 's'],
                                                   4: ['Estado', 's'], 5: ['Cota', 's'], 6: ['Tomo', 'i'], 7: ['Ano', 'i'],
                                                   8: ['Ediçao', 'i'], 9: ['Vol. Série', 'i'], 10: ['Vol. Colec.', 'i'], 11: ['Preço', 'i'],
                                                   12: ['Cópias', 'i']
                                                   },
                                   gl.MAIN_DATASET, grid_column_sizes=gl.GRID_COLUMN_SIZES)
    
    def addCell2Grid(self, line, col, text):
        item = QTableWidgetItem()
        self.mainGrid.setItem(line, col, item)
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
