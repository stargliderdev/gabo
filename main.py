#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib

from PyQt5.QtWidgets import QDesktopWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, \
    QTableWidget, QMenu, QPushButton, QFileDialog, QTableWidgetItem, \
    QWidget, QMainWindow, QApplication, QMessageBox, QStyleFactory, QToolButton, QAction
from PyQt5.QtGui import QIcon

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
        gl.db_params = stdio.read_config_file('livros.ini')
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
        print('ending loading datasets!')
        self.status.extend(gl.dsStatus)
        self.types.extend(gl.ds_types)
        self.resize(1200, 768)
        
        self.center()
        gl.DEBUG = True
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.sort_dic = {'Nada': 'livros.pu_id', 'Autor': 'authors.au_name', 'Titulo': 'livros.PU_TITLE',
                         'ISBN': 'livros.pu_isbn', 'Cota/Local': 'livros.pu_cota',
                         'Tipos': ' livros.pu_type ',
                         'Volume': 'livros.pu_volume', 'Ano': 'livros.pu_ed_year, livros.pu_volume '}
        
        self.statusLabel1 = QLabel()
        self.statusLabel1.setText('Versão ' + gl.VERSION)
        
        
        mainLayout = QVBoxLayout(self.centralwidget)
        # barra de pesquisa
        
        self.fieldToSearchCbox = QComboBox()
        self.fieldToSearchCbox.setMaximumWidth(90)
        self.fieldToSearchCbox.setMinimumWidth(90)
        
        self.fieldToSearchCbox.addItems(['Autor', 'Titulo', 'ISBN', 'Cota/Local'])
        self.fieldToSearchCbox.setCurrentIndex(1)
        
        self.string_to_searchEdit = QLineEdit()
        self.string_to_searchEdit.setMaximumWidth(300)
        self.string_to_searchEdit.setMinimumWidth(300)

        searchButton = QToolButton()
        searchButton.setToolTip('Pesquisa texto')
        searchButton.setIcon(QIcon('./img/search.png'))
        self.set_icon_size(searchButton)
        searchButton.clicked.connect(self.search_field_mode_click)
        
        clearSearchBtn = QToolButton()
        clearSearchBtn.setToolTip('Limpa Pesquisa')
        clearSearchBtn.setIcon(QIcon('./img/clear.png'))
        self.set_icon_size(clearSearchBtn)
        clearSearchBtn.clicked.connect(self.clear_field_search)
        search_tags_Btn = QToolButton()
        search_tags_Btn.setToolTip('Pesquisa tags')
        search_tags_Btn.setIcon(QIcon('./img/search_tags.png'))
        self.set_icon_size(search_tags_Btn)
        search_tags_Btn.clicked.connect(self.search_tags_mode_click)
        
        clear_tags_Btn = QToolButton()
        clear_tags_Btn.setToolTip('Limpa Tags')
        clear_tags_Btn.setIcon(QIcon('./img/clear.png'))
        self.set_icon_size(clear_tags_Btn)
        clear_tags_Btn.clicked.connect(self.clear_tags_search)
        
        self.logicTags = QComboBox()
        self.logicTags.setMaximumWidth(90)
        self.logicTags.setMinimumWidth(90)
        self.logicTags.addItems(['OU', 'E'])
        self.tags_to_searchEdit = QLineEdit()
        self.tags_browserBtn = QToolButton()
        self.tags_browserBtn.setToolTip('Gere Etiquetas')
        self.tags_browserBtn.setIcon(QIcon('./img/tags.png'))
        self.set_icon_size(self.tags_browserBtn)
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
        
        # drop tools menu
        toolsDropMenu = QMenu()
        deletedAction = QAction('Ver Apagados', self)
        deletedAction.triggered.connect(self.show_delete_click)
        toolsDropMenu.addAction(deletedAction)
        toolsBtn = QPushButton('Ferramentas')
        toolsBtn.setMenu(toolsDropMenu)
        
        printBtn = QToolButton()
        printBtn.setIcon(QIcon('./img/print.png'))
        self.set_icon_size(printBtn)
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
        
        authors_Btn = QPushButton()
        authors_Btn.setText('Autores')
        authors_Btn.clicked.connect(self.authors_click)
        
        cotas_Btn = QPushButton()
        cotas_Btn.setText('Cotas')
        cotas_Btn.clicked.connect(self.locals_click)
        
        aboutBtn = QToolButton()
        aboutBtn.setToolTip('Acerca')
        aboutBtn.setIcon(QIcon('./img/info.png'))
        self.set_icon_size(aboutBtn)
        aboutBtn.clicked.connect(self.about_click)
        
        closeBtn = QToolButton()
        closeBtn.setToolTip('Sair')
        closeBtn.setIcon(QIcon('./img/close.png'))
        self.set_icon_size(closeBtn)
        closeBtn.clicked.connect(self.closeBtn_click)
        
        self.sortByCbox = QComboBox()
        self.sortByCbox.setCurrentIndex(0)
        self.sortByCbox.addItems(['Nada', 'Autor', 'Titulo', 'Tipos', 'Cota/Local', 'Volume', 'Ano'])
        self.sortByCbox.setCurrentIndex(0)
        self.sortByCbox.currentIndexChanged.connect(self.filter_click)
        self.recordLimitEdt = QLineEdit()
        self.recordLimitEdt.setMaximumWidth(40)
        self.recordLimitEdt.setMaxLength(4)
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.recordLimitEdt.editingFinished.connect(self.limit_change)
        
        self.types_filterCbox = QComboBox()
        self.types_filterCbox.addItems(self.types)
        self.types_filterCbox.setCurrentIndex(0)
        self.types_filterCbox.currentIndexChanged.connect(self.types_change)
        self.status_filterCbox = QComboBox()
        self.status_filterCbox.setCurrentIndex(0)

        self.status_filterCbox.addItems(self.status)
        self.status_filterCbox.currentIndexChanged.connect(self.status_change)
        
        mainLayout.addLayout(qlib.addHLayout(
            [bookAddBtn, bookAddIsbnBtn, self.last_fiveBtn, authors_Btn, cotas_Btn, double1_Btn, clone_Btn, toolsBtn,printBtn, True,
              aboutBtn, closeBtn]))
        mainLayout.addLayout(qlib.addHLayout(
            [self.fieldToSearchCbox, self.string_to_searchEdit, searchButton, clearSearchBtn, 'Ordena:',
             self.sortByCbox,
             True, 'Tipos', self.types_filterCbox, 'Estado', self.status_filterCbox, True]))
        
        mainLayout.addLayout(qlib.addHLayout(
            [self.logicTags, self.tags_to_searchEdit, self.tags_browserBtn, search_tags_Btn, clear_tags_Btn, True,
             'Resultados', self.recordLimitEdt]))
        
        # grid
        self.grid = QTableWidget(self)
        self.grid.setSelectionBehavior(QTableWidget.SelectRows)
        self.grid.setSelectionMode(QTableWidget.SingleSelection)
        
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.verticalHeader().setDefaultSectionSize(20)
        self.grid.setAlternatingRowColors(True)
        self.grid.verticalHeader().setVisible(False)
        self.grid.doubleClicked.connect(self.grid_double_click)
        
        mainLayout.addWidget(self.grid)
        self.string_to_searchEdit.returnPressed.connect(self.filter_click)
        self.fieldToSearchCbox.setCurrentIndex(1)
        # sub menus
        author_pub = QAction("Obras do Autor", self)
        author_pub.triggered.connect(self.author_pub_click)
        self.grid.addAction(author_pub)
        
        local_pub = QAction("Obras nesta Cota", self)
        local_pub.triggered.connect(self.local_pub_click)
        self.grid.addAction(local_pub)
        self.grid.setContextMenuPolicy(2)  # Qt.ActionsContextMenu)
        
        self.last_records_click()
        mainLayout.addWidget(self.statusLabel1)
        try:
            if GetSystemMetrics(1) <= 768:
                self.showMaximized()
        except NameError:
            pass
    
    def types_change(self):
        self.recordLimitEdt.setText('0')
        self.filter_click()
    
    def status_change(self):
        self.recordLimitEdt.setText('0')
        self.filter_click()
    
    def author_pub_click(self):
        a = self.grid.item(self.grid.currentRow(), 2).text()
        self.string_to_searchEdit.setText(a)
        self.fieldToSearchCbox.setCurrentIndex(0)
        self.filter_click()
    
    def local_pub_click(self):
        try:
            a = self.grid.item(self.grid.currentRow(), 5).text()
            self.string_to_searchEdit.setText(a)
            self.fieldToSearchCbox.setCurrentIndex(3)
            self.filter_click()
        except AttributeError:
            pass
    
    def tags_browser_click(self):
        form = tag_browser.BrowserTags()
        form.exec_()
        if not form.tag_list == []:
            self.tags_to_searchEdit.setText(form.tag_list)
            self.string_to_searchEdit.clear()
    
    def double1_click(self):
        # duplica normal
        if self.grid.item(self.grid.currentRow(), 0) is not None:
            print('duplica')
            form = edit_record.EditRecord(int(self.grid.item(self.grid.currentRow(), 0).text()), '', isbn=False, copy=1)
            form.exec_()
            self.refresh_grid()
    
    def clone_click(self):
        # clona
        if self.grid.item(self.grid.currentRow(), 0) is not None:
            form = edit_record.EditRecord(int(self.grid.item(self.grid.currentRow(), 0).text()), '', isbn=False, copy=2)
            form.exec_()
            self.refresh_grid()
       
    def authors_click(self):
        form = authors.BrowserAuthors()
        form.exec_()
        if form.toto != '':
            self.fieldToSearchCbox.setCurrentIndex(0)
            self.string_to_searchEdit.setText(form.toto)
            self.search_field_mode_click()
    
    def locals_click(self):
        import locals
        form = locals.BrowserLocals()
        form.exec_()
        self.search_field_mode_click()
    
    def print_click(self):
        hl = make_report_html.main_grid_report(self.data_set)
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
        self.fieldToSearchCbox.setCurrentIndex(1)
        self.string_to_searchEdit.setText('')
        self.tags_to_searchEdit.setText('')
        self.types_filterCbox.setCurrentIndex(0)
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
        if self.types_filterCbox.currentIndex() != 0:
            sql += ' livros.pu_type = (select ty_id from types where ty_name like \'' + str(
                self.types_filterCbox.currentText()) + '\') and '
        
        if self.status_filterCbox.currentIndex() != 0:
            sql += """ livros.pu_status = (select st_id from status where st_nome like \'""" + str(
                self.status_filterCbox.currentText()) + """"\') and """
        
        sql += """  livros.pu_status = status.st_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
        ORDER BY pu_id DESC LIMIT """ + gl.SHOW_RECORDS + ";"
       
        self.data_set = dbmain.query_many(sql)
       
        self.update_grid()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)

    def show_delete_click(self):
        sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome, livros.pu_cota, livros.pu_volume
        FROM livros, authors, types, status
        WHERE'''
        sql += ' livros.pu_author_id =0 and livros.pu_type > 0 and livros.pu_status > 0 and '
        sql += '''  livros.pu_status = status.st_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type
          ORDER BY pu_id desc;'''
        self.data_set = dbmain.query_many(sql)
        self.update_grid()
    
    def refresh_grid(self):
        # refresh grid by filters
        # if filter empty go to last records
        self.search_field_mode_click()
        if gl.records_in_ds == 0:
            self.search_tags_mode_click()
        if gl.records_in_ds == 0:
            self.last_records_click()
    
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
    

    def make_sql(self):
        # v2
        select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year FROM livros, authors, types, status"
        join_ = " livros.pu_status = status.st_id AND authors.au_id = livros.pu_author_id AND types.ty_id = livros.pu_type "
        where_ = ' WHERE '
        order_ = ''
        search_ = ''
        limit_ = ''
    
        self.key_sort = self.sort_dic[self.sortByCbox.currentText()]
        if not self.string_to_searchEdit.text() == '':
            self.recordLimitEdt.setText('0')
            self.key_search = self.sort_dic[self.fieldToSearchCbox.currentText()]
            if self.fieldToSearchCbox.currentIndex() == 3: # na cota tem de ser exactamente igual
                text_to_search = "\'" + self.string_to_searchEdit.text().lower().strip() + "\'"
            else:
                text_to_search = "\'%" + self.string_to_searchEdit.text().lower().strip() + "%\'"
            
            if len(text_to_search) > 1:
                where_ += '''unaccent(lower(''' + self.key_search + ''')) LIKE  unaccent(''' + text_to_search + ''') AND '''
            else:
                where_ += ''' unaccent(upper(''' + self.key_search + ''')) SIMILAR TO ''' + '''unaccent(''' + text_to_search.upper() + ')' + ''' AND '''
        elif  not self.tags_to_searchEdit.text() =='': # modo para tags
            self.recordLimitEdt.setText('0')
            print ('make_sql',)
            tags = self.tags_to_searchEdit.text().replace("\'", "\\\'")
            tags = tags.split(',')
            in_data = ''
            if self.logicTags.currentIndex() == 0:  # ou
                for n in tags:
                    toto = n.lower().strip()
                    in_data += "unaccent(\'" + toto + "\'),"
                a = dbmain.query_many(
                    '''select ta_id from tags where unaccent(ta_name) in (''' + in_data[:-1] + ''')''')
                i = []
                for t in a:
                    i.append(t[0])
                if i:
                    i = str(i)
                    where_ += '''
                         pu_id in(select * from (select tr_book from tag_ref where tr_tag in(''' + i[
                                                                                                   1:-1] + ''')) as foo) AND '''
                else:
                    where_ += '''pu_id in(select * from (select tr_book from tag_ref where tr_tag in(-1)) as foo) AND '''
            else:
                t = ''
                for n in tags:
                    t = t + "\'" + n.strip() + "\',"
                t = t[:-1]
                c = str(len(tags))
                where_ = ''' where EXISTS (SELECT NULL
                 FROM tag_ref tg
                 JOIN TAGS t ON t.ta_id = tg.tr_tag
                WHERE unaccent(t.ta_name) IN (unaccent(''' + t + '''))
                  AND tg.tr_book = livros.pu_id
             GROUP BY tg.tr_book
               HAVING COUNT(t.ta_name) =''' + c + ''') and '''
        else:  # não procura em nada
            where_ += ''' livros.pu_status = status.st_id AND
          authors.au_id = livros.pu_author_id AND
          types.ty_id = livros.pu_type and '''
            self.key_sort = self.sort_dic[self.sortByCbox.currentText()]
    
        if self.types_filterCbox.currentIndex() != 0:
            where_ += " livros.pu_type = (select ty_id from types where ty_name like \'" + str(
                self.types_filterCbox.currentText()) + '\') and '
    
        if self.status_filterCbox.currentIndex() != 0:
            where_ += " livros.pu_status = (select st_id from status where st_nome like \'" + str(
                self.status_filterCbox.currentText()) + "\') and "
    
        order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
    
        if int(gl.SHOW_RECORDS) > 0: #  int(self.recordLimitEdt.text()) > 0:
            limit_ = 'LIMIT ' + gl.SHOW_RECORDS
            order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
        else:
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
            
            limit_ = 'LIMIT 99999'
        
        return select_ + where_ + join_ + order_ + limit_
    
    def limit_change(self):
        gl.SHOW_RECORDS = self.recordLimitEdt.text()
        try:
            dum = int(gl.SHOW_RECORDS)
        except ValueError:
            gl.SHOW_RECORDS='80'
            self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        data_access.save_param('SHOW_RECORDS', gl.SHOW_RECORDS)
        self.sortByCbox.setCurrentIndex(0)
        self.types_filterCbox.setCurrentIndex(0)
        self.last_fiveBtn.setText('Ultimos ' + gl.SHOW_RECORDS)
        self.filter_click()
    
    def filter_click(self):
        foo = self.make_sql()
        self.data_set = dbmain.query_many(foo)
        gl.records_in_ds = len(self.data_set)
        self.update_grid()
        self.statusLabel1.setText('Registos encontrados:' + str(gl.records_in_ds))
    
    def search_field_mode_click(self):
        gl.records_in_ds = 0
        if not self.string_to_searchEdit.text() == '':
            # self.filter_click()
            sql = self.make_sql()
            self.data_set = dbmain.query_many(sql)
            gl.records_in_ds = len(self.data_set)
            if gl.records_in_ds == 0:
                # self.grid.clear()
                self.grid.setRowCount(0)
            else:
                self.update_grid()
            self.statusLabel1.setText('Registos encontrados:' + str(gl.records_in_ds))
            
    
    def search_tags_mode_click(self):
        if not self.tags_to_searchEdit.text() == '':
            self.string_to_searchEdit.setText('')
            sql = self.make_sql()
            self.data_set = dbmain.query_many(sql)
            if len(self.data_set) == 0:
                self.grid.setRowCount(0)
            else:
                self.update_grid()
            self.statusLabel1.setText('Registos encontrados:' + str(len(self.data_set)))
   
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
        self.data_set = a  # é global para que possa ser utilizado nos relatorios em html
        self.statusLabel1.setText('Registos encontrados:' + str(len(self.data_set)))
        return self.data_set
    
    def grid_double_click(self):
        stack_current_row =self.grid.currentRow()
        form = edit_record.EditRecord(int(self.grid.item(self.grid.currentRow(), 0).text()), '', isbn=False)
        form.exec_()
        if not self.string_to_searchEdit.text() == '':
            self.recordLimitEdt.setText('999')
            foo = self.make_sql()
            self.data_set = dbmain.query_many(foo)
            self.update_grid()
        elif not self.tags_to_searchEdit.text() == '':
            foo = self.make_sql()
            self.data_set = dbmain.query_many(foo)
            self.update_grid()
        else:
            self.last_records_click()
        self.grid.setCurrentCell(stack_current_row,0)
        
    def refresh_search(self):
        pass
    
    def clear_field_search(self):
        self.string_to_searchEdit.clear()
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        self.last_records_click()
        # self.update_grid(self.get_data())
    
    def clear_tags_search(self):
        self.tags_to_searchEdit.clear()
    
    def update_grid(self):
        ex_grid.ex_grid_update(self.grid, {0: ['Num', 'i'], 1: ['Titulo', 's'], 2: ['Autor', 's'], 3: ['Tipo', 's'],
                                           4: ['Estado', 's'], 5: ['Cota', 's'], 6: ['Vol.', 'i'], 7: ['Ano', 'i']},
                               self.data_set)
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
