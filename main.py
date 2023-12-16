#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import datetime
from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QLineEdit, QComboBox, \
    QTableWidget, QPushButton, QFileDialog, QTableWidgetItem, \
    QWidget, QMainWindow, QApplication, QMessageBox, QStyleFactory, QToolButton, QAction, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon

import bindings
import classifications
import colections
import conditions
import languages
import main_grid_layout
import pub_types
import series
import settings
import setup
import status
import storage
import tags_manage
import tags_special_manage

import ex_grid
import parameters as gl

import sqlite_crud as sqlite_crud
import info as info
import qlib
import edit_record
import stdio
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
        # gl.db_params = stdio.read_config_file('gabo.ini')
        if settings.load_settings():
            pass
        HAS_DATABASE = sqlite_crud.check_alive()
        if not HAS_DATABASE:
            QMessageBox.information (None,
                                 "Erro Fatal",
                                 """A base de dados não foi encontrada!""",
                                 QMessageBox.StandardButtons(QMessageBox.Ok), QMessageBox.Ok)
            form = settings.EditGlobalSettings()
            form.exec_()
            settings.load_settings()
        
        sqlite_crud.load_parameters()
        sqlite_crud.load_words()
        sqlite_crud.get_types()
        sqlite_crud.get_status()
        sqlite_crud.get_authors()
        sqlite_crud.get_locals()
        sqlite_crud.get_conditions()
        sqlite_crud.get_classifications()
        sqlite_crud.get_languages()
        sqlite_crud.get_covers()

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
        self.mainSearchCbox.addItems(['Titulo', 'Autor', 'ISBN', 'Etiqueta', 'Colecção', 'Série'])
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

        localsBtn = QToolButton()
        localsBtn.setToolTip('Locais')
        localsBtn.setIcon(QIcon('./img/locals.png'))
        localsBtn.clicked.connect(self.locals_click)

        collectionBtn = QToolButton()
        collectionBtn.setToolTip('Colecções')
        collectionBtn.setIcon(QIcon('./img/collections.png'))
        collectionBtn.clicked.connect(self.collection_click)

        seriesBtn = QToolButton()
        seriesBtn.setToolTip('Series')
        seriesBtn.setIcon(QIcon('./img/series.png'))
        seriesBtn.clicked.connect(self.series_click)

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
        self.tags_browserBtn.setToolTip('Etiquetas')
        self.tags_browserBtn.setIcon(QIcon('./img/tags.png'))
        # self.set_icon_size(self.tags_browserBtn)
        self.tags_browserBtn.clicked.connect(self.tags_browser_click)

        # drop add menu
        bookAddBtn = QPushButton('Novo')
        bookAddBtn.setIcon(QIcon('./img/add_book.png'))
        bookAddBtn.setToolTip('Adiciona Livro')
        bookAddBtn.clicked.connect(self.record_add_click)

        bookAddIsbnBtn = QPushButton('Internet')
        bookAddIsbnBtn.setToolTip('Adiciona livro pela WOOK')
        bookAddIsbnBtn.clicked.connect(self.open_external_browser)

        self.addBookBtn = QPushButton()
        self.addBookBtn.setToolTip('Adicionar Livro')
        self.addBookBtn.setIcon(QIcon('./img/addbook.png'))

        printBtn = QToolButton()
        printBtn.setIcon(QIcon('./img/print.png'))
        # self.set_icon_size(printBtn)
        printBtn.clicked.connect(self.print_click)

        navigatorBtn = QPushButton('Navegador')
        navigatorBtn.clicked.connect(self.navigator_click)

        self.lastRecordsBtn = QPushButton('Registos')
        self.lastRecordsBtn.setIcon(QIcon('./img/refresh.png'))
        # self.lastRecordsBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
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
        typeBtn.setToolTip('Tipos de Publicação')
        typeBtn.setIcon(QIcon('./img/pub_types.png'))
        typeBtn.clicked.connect(self.pub_types_click)

        # backupBtn = QToolButton()
        # backupBtn.setToolTip('Backup da base de dados')
        # backupBtn.setIcon(QIcon('./img/info.png'))
        # backupBtn.clicked.connect(self.database_backup)

        # aboutBtn = QToolButton()
        # aboutBtn.setToolTip('Acerca')
        # aboutBtn.setIcon(QIcon('./img/info.png'))
        # aboutBtn.clicked.connect(self.settings_click)

        databaseBtn = QToolButton()
        databaseBtn.setToolTip('Bases de Dados')
        databaseBtn.setIcon(QIcon('./img/settings.png'))
        databaseBtn.clicked.connect(self.settings_click)

        closeBtn = QToolButton()
        closeBtn.setToolTip('Sair')
        closeBtn.setIcon(QIcon('./img/close.png'))
        closeBtn.clicked.connect(self.closeBtn_click)
        self.recordLimitEdt = QLineEdit()
        self.recordLimitEdt.setMaximumWidth(40)
        self.recordLimitEdt.setMaxLength(4)
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.recordLimitEdt.editingFinished.connect(self.limit_change)

        mangeColumnsBtn = QToolButton()
        mangeColumnsBtn.setToolTip('Colunas visiveis')
        mangeColumnsBtn.setIcon(QIcon('./img/columns.png'))
        mangeColumnsBtn.clicked.connect(self.show_columns_click)

        mainLayout.addLayout(qlib.addHLayout([bookAddBtn, bookAddIsbnBtn,  printBtn, navigatorBtn, True,databaseBtn, closeBtn,]))
        mainLayout.addLayout(qlib.addHLayout([self.mainSearchCbox, self.mainToSearchEdt, mainSearchBtn, mainSearchClearBtn, 32,
             authorsBtn,self.tags_browserBtn, localsBtn, 64,collectionBtn, seriesBtn,64,languageBtn, coverBtn, statusBtn,
            conditionBtn, ratingBtn, typeBtn, mangeColumnsBtn, True, self.lastRecordsBtn,  self.recordLimitEdt], 60))

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

        local_pub = QAction("Obras nesta local", self)
        local_pub.triggered.connect(self.local_pub_click)
        self.mainGrid.addAction(local_pub)
        self.mainGrid.setContextMenuPolicy(2)

        if HAS_DATABASE:
            self.last_records_click()
        if gl.SCREEN_HEIGHT == 768:
            self.showMaximized()
        self.statusBar = self.statusBar()
        self.statusBarLabel = QLabel('Base de Dados: ' + gl.DB_PATH+ gl.DB_FILE )
        self.statusBar.addWidget(self.statusBarLabel)

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
            form = edit_record.EditRecord(int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text()), '',
                                          draft_data=False, copy=1)
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
            gl.SEARCH_DICT['LAST'] = 0
            # self.mainSearchCbox.setCurrentIndex(4)
            self.mainToSearchEdt.setText(form.toto)
            self.update_grid()

    def collection_click(self):
        form = colections.CollectionBrowser()
        form.exec_()
        if not form.toto == '':
            gl.RECORDS_IN_DATASET = 0
            gl.LAST_SEARCH_WHERE = 1
            gl.SEARCH_DICT['WHERE'] = 'collection'
            gl.SEARCH_DICT['WHAT'] = form.toto
            gl.SEARCH_DICT['LAST'] = 0
            self.mainSearchCbox.setCurrentIndex(4)
            self.mainToSearchEdt.setText(form.toto)
            self.update_grid()

    def series_click(self):
        form = series.SeriesBrowser()
        form.exec_()
        if not form.toto == '':
            gl.RECORDS_IN_DATASET = 0
            gl.LAST_SEARCH_WHERE = 1
            gl.SEARCH_DICT['WHERE'] = 'serie'
            gl.SEARCH_DICT['WHAT'] = form.toto
            gl.SEARCH_DICT['LAST'] = 0
            self.mainSearchCbox.setCurrentIndex(5)
            self.mainToSearchEdt.setText(form.toto)
            self.update_grid()

    def width_sum_click(self):
        form = storage.StoreMangDialog()
        form.exec_()

    def print_click(self):
        hl = make_report_html.main_grid_report(gl.MAIN_DATASET)
        form = report_display.DisplayReport(hl)
        form.exec_()

    def show_columns_click(self):
        gl.GRID_COLUMN_SIZES = []
        for n in range(0, self.mainGrid.columnCount()):
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
            gl.SHOW_RECORDS = '10000'
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        # sqlite_crud.save_parameters('SHOW_RECORDS', gl.SHOW_RECORDS)
        # self.typesCbox.setCurrentIndex(0)
        # self.lastRecordsBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        gl.SEARCH_DICT['LAST'] = int(gl.SHOW_RECORDS)
        self.mainToSearchEdt.clear()
        self.update_grid()

    def settings_click(self):
        form = settings.EditGlobalSettings()
        form.exec_()
        sqlite_crud.get_authors()
        sqlite_crud.load_words()
        sqlite_crud.get_types()
        sqlite_crud.get_status()
        sqlite_crud.get_locals()
        sqlite_crud.get_conditions()
        sqlite_crud.get_classifications()
        sqlite_crud.get_languages()
        sqlite_crud.get_covers()
        sqlite_crud.load_parameters()
        self.update_grid()
        self.statusBarLabel.setText('Base de Dados: ' + gl.DB_PATH + gl.DB_FILE)
        self.last_records_click()

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
        # if gl.db_params['db_engine'] == 'PSQL':
        #     # print(gl.db_params['db_pg_dump'])
        #     # # C:\Program Files\pgAdmin III\1.28\pg_dump.exe -h localhost -U "root" --format custom --blobs --verbose --file "c:\tmp\livros_2022-07-27.backup" "livros"
        #     # print()
        #     # print(gl.db_params['db_pg_dump'] + '\pg_dump.exe -h ' + gl.db_params['db_host'] + ' -U ' + gl.db_params['db_user']
        #     #       + ' --format custom --blobs --verbose --file ' + gl.db_params['backup_dir'] + '\\' + gl.db_params['db_database'] + "_" + date_string +".backup" + ' ' + gl.db_params['db_database'])
        #     call_pg_dump = gl.db_params['db_pg_dump'] + '\pg_dump.exe -h ' + gl.db_params['db_host'] + ' -U ' + \
        #                    gl.db_params['db_user'] \
        #                    + ' --format custom --blobs --verbose --file ' + gl.db_params['backup_dir'] + '\\' + \
        #                    gl.db_params['db_database'] + "_" + date_string + ".backup" + ' ' + gl.db_params[
        #                        'db_database']

            # os.system(call_pg_dump)
            # result = QMessageBox.information(None,
            #                                  "Cópia de Segurança ",
            #                                  "Cópia de Segurança efectuada para\n" + gl.db_params['backup_dir']
            #                                  + '\nCom o nome:' + gl.db_params[
            #                                      'db_database'] + "_" + date_string + ".backup",
            #                                  QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)

    def closeBtn_click(self):
        self.close()

    def limit_change(self):
        gl.SHOW_RECORDS = self.recordLimitEdt.text()
        try:
            dum = int(gl.SHOW_RECORDS)
        except ValueError:
            gl.SHOW_RECORDS = '80'
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        sqlite_crud.save_parameters('SHOW_RECORDS', gl.SHOW_RECORDS)
        # self.typesCbox.setCurrentIndex(0)
        # self.lastRecordsBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        self.update_grid()

    def clear_search(self):
        self.mainToSearchEdt.clear()
        self.update_grid()

    def main_search_click(self):
        """will search in title, tags and ISBN"""
        if not self.mainToSearchEdt.text() == '':
            gl.SEARCH_DICT['LAST'] = 0
            if self.mainSearchCbox.currentIndex() == 0:  # title
                gl.SEARCH_DICT['WHERE'] = 'title'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
            elif self.mainSearchCbox.currentIndex() == 1:  # author
                gl.SEARCH_DICT['WHERE'] = 'author'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
            elif self.mainSearchCbox.currentIndex() == 2:  # ISBN
                gl.SEARCH_DICT['WHERE'] = 'isbn'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 3:  # tags
                gl.SEARCH_DICT['WHERE'] = 'tags_or'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text()
            elif self.mainSearchCbox.currentIndex() == 4:  # colecção
                gl.SEARCH_DICT['WHERE'] = 'collection'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
            elif self.mainSearchCbox.currentIndex() == 5:
                gl.SEARCH_DICT['WHERE'] = 'serie'
                gl.SEARCH_DICT['WHAT'] = self.mainToSearchEdt.text().lower()
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

    def open_external_browser(self):
        # form = browser.BrowserInLine("https://www.wook.pt/")
        # form.exec_()
        # self.last_records_click()
        stdio.search_internet()

    def record_add_click(self):
        gl.record_current_dict = {}
        gl.TAGS_SPECIAL_LEVEL1_DATA = []
        form = edit_record.EditRecord(-1)
        form.exec_()
        self.update_grid()

    def get_data(self):
        sql = '''SELECT pu_id, pu_title, au_name, ty_name, status_name,
          pu_local,pu_volume, pu_year
        FROM
          livros, authors, types, status
        WHERE
          pu_status = status.status_id AND
          types.ty_id = livros.pu_type
        ORDER BY
          pu_title ASC LIMIT 50;'''
        a = sqlite_crud.query_many(sql)
        gl.MAIN_DATASET = a  # é global para que possa ser utilizado nos relatorios em html
        return gl.MAIN_DATASET

    def grid_double_click(self):
        stack_current_row = self.mainGrid.currentRow()
        form = edit_record.EditRecord(int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text()))
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
                gl.COLUMN_SORT = (col_index, 1)
                gl.SEARCH_DICT['ORDER'] = gl.FIELDS_ORDER_DIC[gl.GRID_COL_NAMES_ORG[col_index].lower()]
                gl.SEARCH_DICT['ORDER_BY'] = 'ASC'
                gl.GRID_COL_NAMES[col_index] = gl.GRID_COL_NAMES[col_index] + ' ⬇'
            elif gl.COLUMN_SORT[1] == 1:
                gl.COLUMN_SORT = (col_index, 2)
                gl.SEARCH_DICT['ORDER'] = gl.FIELDS_ORDER_DIC[gl.GRID_COL_NAMES_ORG[col_index].lower()]
                gl.SEARCH_DICT['ORDER_BY'] = 'DESC'
                gl.GRID_COL_NAMES[col_index] = gl.GRID_COL_NAMES[col_index] + ' ⬆'
            else:
                gl.COLUMN_SORT = (0, 0)
                gl.SEARCH_DICT['ORDER'] = ''
                gl.SEARCH_DICT['ORDER_BY'] = 'ASC'
                gl.GRID_COL_NAMES = gl.GRID_COL_NAMES_ORG[:]
        else:
            gl.GRID_COL_NAMES = gl.GRID_COL_NAMES[:]
            gl.COLUMN_SORT = (0, 0)
        self.update_grid()
        self.mainGrid.setHorizontalHeaderLabels(gl.GRID_COL_NAMES)

    def navigator_click(self):
        gl.NAVIGATOR_INDEX = []
        try:
            current_record = int(self.mainGrid.item(self.mainGrid.currentRow(), 0).text())
        except AttributeError:
            current_record = int(self.mainGrid.item(0, 0).text())
        for line in range(0, self.mainGrid.rowCount()):
            gl.NAVIGATOR_INDEX.append((line, int(self.mainGrid.item(line, 0).text())))
        form = edit_record.EditRecord(current_record,navigator=current_record)
        form.exec_()
        self.update_grid()

    def second_field_clear_click(self):
        self.authorToSearchEdt.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()

    def clear_tags_search(self):
        self.tags_to_searchEdit.clear()

    def update_grid(self):
        sql = lib_gabo.make_sql(gl.SEARCH_DICT)
        gl.MAIN_DATASET = sqlite_crud.query_many(sql)
        gl.RECORDS_IN_DATASET = len(gl.MAIN_DATASET)
        if gl.RECORDS_IN_DATASET == 0:
            self.mainGrid.setRowCount(0)
        else:
            ex_grid.ex_grid_update(self.mainGrid,
                                   {0: ['Num', 'i'], 1: ['Titulo', 's'], 2: ['Autor', 's'], 3: ['Tipo', 's'],
                                    4: ['Estado', 's'], 5: ['Local', 's'], 6: ['Tomo', 'i'], 7: ['Ano', 'i'],
                                    8: ['Ediçao', 'i'], 9: ['Vol. Série', 'i'], 10: ['Vol. Colec.', 'i'],
                                    11: ['Preço', 'i'],
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
    except urllib.error.URLError as err:
        pass
    return False


def main():
    setup.get_system_info()
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

main()
