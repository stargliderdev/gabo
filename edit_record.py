#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QLabel, QCheckBox, QVBoxLayout, QLineEdit, QComboBox, QDateEdit, \
    QWidget, QDialog, QHBoxLayout, QToolButton, QPushButton, QTextEdit, QMessageBox, QPlainTextEdit,QTextBrowser

from PyQt5.Qt import Qt

import isbn_lib
import parameters as pa
import dmPostgreSQL as dbmain
import data_access as data_access
import missing_data
from qlib import setSize,addHLayout,HLine
import tag_browser
import stdio


class EditRecord(QDialog):
    def __init__(self,id,data,isbn=True,copy=0,parent=None):
        super(EditRecord, self).__init__(parent)
        self.setWindowTitle('Edita Livros')
        self.resize(800, 600)
        self.error_list = []
        pa.userError = ''
        self.toto = False
        self.id = id
        
        mainLayout = QVBoxLayout(self)
        self.buttonsLayout = QHBoxLayout()
        # tabs
        self.titleLayout = QVBoxLayout()
        self.makeButtons()
        self.make_title()
        self.tabuladorTabWidget = QTabWidget()
        self.makeTab2()
        self.makeTab4()
        self.tabuladorTabWidget.addTab(self.tab4, 'Etiquetas')
        self.tabuladorTabWidget.addTab(self.tab2, 'Observações')
        mainLayout.addLayout(self.buttonsLayout)
        mainLayout.addWidget(HLine())
        mainLayout.addLayout(self.titleLayout)
        mainLayout.addWidget(self.tabuladorTabWidget)
        
        if self.id == -1:
            self.item_data = -1
            self.record_add()
            if isbn:
                self.add_from_isbn(data)
        else:
            if copy == 0:
                self.item_data = data_access.get_livro_data(self.id)
                self.refresh_datafields()
            elif copy == 1:
                self.item_data = data_access.get_livro_data(self.id)
                self.refresh_datafields()
                self.duplicar_registo()
            elif copy == 2:
                self.item_data = data_access.get_livro_data(self.id)
                toto = self.item_data
                self.refresh_datafields()
                self.duplicar_registo()
                read_record(self.pu_title, 'pu_title', toto)
                read_record(self.pu_isbn, 'pu_isbn', toto)
                read_record(self.pu_cota, 'pu_cota', toto)
        self.pu_title.setFocus()
        
        self.stored = True
        if self.pu_cota.text() == '':
            self.pu_cota.setText(pa.ON_LOCAL)
    
    def make_title(self):
        self.pu_title = QLineEdit()
        titleCapitalize = QToolButton()
        setSize(titleCapitalize)
        titleCapitalize.setIcon(QIcon('./img/blue.png'))
        titleCapitalize.setToolTip('Capitaliza Titulo')
        titleCapitalize.clicked.connect(self.title_caps)
        
        self.pu_volume = QLineEdit()
        self.pu_volume.setMaximumWidth(40)
        self.pu_volume.setMaxLength(3)
        
        self.pu_ed_year = QLineEdit()
        self.pu_ed_year.setMaximumWidth(60)
        self.pu_ed_year.setMaxLength(4)
        
        self.titleLayout.addLayout(addHLayout(['Titulo:', self.pu_title,titleCapitalize]))
        self.titleLayout.addLayout(addHLayout(['Volume:', self.pu_volume, 'Ano',self.pu_ed_year, True]))
        self.pu_sub_title = QLineEdit()
        self.pu_sub_title.setMaxLength(255)
        subTitleCapitalize = QToolButton()
        setSize(subTitleCapitalize)
        subTitleCapitalize.setIcon(QIcon('./img/blue.png'))
        subTitleCapitalize.setToolTip('Capitaliza sub-titulo')
        subTitleCapitalize.clicked.connect(self.sub_title_caps)
        self.titleLayout.addLayout(addHLayout(['Sub-titulo:', self.pu_sub_title,subTitleCapitalize]))
        labelpu_author_id = QLabel('Autor:')
        labelpu_author_id.setAlignment(Qt.AlignRight)
        
        self.pu_author_id = QComboBox(self)
        self.pu_author_id.setEditable(True)
        authorToTagBtn = QToolButton()
        setSize(authorToTagBtn)
        authorToTagBtn.setIcon(QIcon('./img/green.png'))
        authorToTagBtn.setToolTip('Adiciona autor ás etiquetas')
        authorToTagBtn.clicked.connect(self.add_author_to_tags)
        self.titleLayout.addLayout(addHLayout(['Autor:', self.pu_author_id,authorToTagBtn]))
        
        self.pu_type = QComboBox()
        self.pu_type.setEditable(True)
        typeToTagBtn = QToolButton()
        setSize(typeToTagBtn)
        typeToTagBtn.setIcon(QIcon('./img/green.png'))
        typeToTagBtn.setToolTip('Adiciona tipo ás etiquetas')
        typeToTagBtn.clicked.connect(self.add_type_to_tags)
        self.pu_cota = QLineEdit()
        self.pu_cota.setObjectName('pu_cota')
        self.pu_cota.setMaxLength(10)
        self.pu_status = QComboBox()
        self.pu_status.setEditable(True)
        
        self.titleLayout.addLayout(addHLayout(['Tipo:', self.pu_type,typeToTagBtn, 'Estado:', self.pu_status]))
        
        self.pu_isbn = QLineEdit()
        self.pu_isbn.setMaxLength(20)
        
        self.pu_isbn10 = QLineEdit()
        self.pu_isbn10.setMaxLength(10)
        
        self.pu_isbn10.setObjectName('pu_isbn10')
        self.pu_depLegal = QLineEdit()
        self.pu_depLegal.setMaxLength(20)
        
        self.titleLayout.addLayout(addHLayout(['ISBN:', self.pu_isbn, 'Cota:', self.pu_cota]))
    
    def makeTab1(self):
        self.tab1 = QWidget()
        mainTab1Layout = QVBoxLayout(self.tab1)
        tab1Layout = QVBoxLayout()
        self.pu_author_others = QLineEdit()
        self.pu_author_others.setMaxLength(150)
        
        tab1Layout.addLayout(addHLayout(['Outros Autores', self.pu_author_others]))
        
        self.pu_translator = QComboBox()
        self.pu_translator.setMinimumWidth(300)
        self.pu_translator.setEditable(True)
        
        self.pu_translator.addItems(pa.dsTradutores)
        
        self.pu_language = QComboBox()
        self.pu_language.setMinimumWidth(100)
        self.pu_language.setEditable(True)
        tab1Layout.addLayout(addHLayout(['Tradutor:', self.pu_translator, 'Lingua:', self.pu_language]))
        
        self.pu_edition_number = QLineEdit()
        self.pu_edition_number.setObjectName('pu_edition_number-int')
        self.pu_edition_number.setAlignment(Qt.AlignRight)
        self.pu_edition_number.setMinimumWidth(40)
        
        self.pu_edition_number.setInputMask('nnnnnn')
        self.pu_edition_number.setMaxLength(6)
        
        tab1Layout.addLayout(addHLayout(['Editor(a):', self.pu_editor_id, 'Edição Num.:', self.pu_edition_number]))
        
        self.pu_ed_date = QLineEdit()
        self.pu_ed_date.setMaxLength(10)
        self.pu_ed_date.setMaximumWidth(50)
        
        self.pu_ed_local = QLineEdit()
        self.pu_ed_local.setMaxLength(40)
        
        tab1Layout.addLayout(addHLayout(['Data:', self.pu_ed_date, 'Local:', self.pu_ed_local]))
        
        # junta
        mainTab1Layout.addLayout(tab1Layout)
        mainTab1Layout.addStretch()
    
    def makeTab2(self):
        self.tab2 = QWidget()
        mainTab2Layout = QVBoxLayout(self.tab2)
        tab2Layout = QVBoxLayout()
        self.pu_obs = QTextEdit()
        tab2Layout.addWidget(self.pu_obs)
        
        mainTab2Layout.addLayout(tab2Layout)
    
    def makeTab3(self):
        self.tab3 = QWidget()
        mainTab3Layout = QVBoxLayout(self.tab3)
        tab3Layout = QVBoxLayout()
        self.pu_sinopse = QTextEdit()
        tab3Layout.addWidget(self.pu_sinopse)
        
        mainTab3Layout.addLayout(tab3Layout)
    
    def makeTab4(self):
        self.tab4 = QWidget()
        mainTab4Layout = QVBoxLayout(self.tab4)
        tab4Layout = QVBoxLayout()
        self.tags = QTextBrowser()
        self.tags.setMaximumHeight(90)
        self.tags.setReadOnly(False)
        addTags = QToolButton()
        addTags.setText('Lista Etiquetas')
        addTags.clicked.connect(self.add_tags_click)
        
        editTags = QToolButton()
        editTags.setText('Edita Etiquetas')
        editTags.clicked.connect(self.edit_tags_click)
        self.pu_sinopse = QTextEdit()
        tab4Layout.addLayout(addHLayout([addTags, editTags, True]))
        tab4Layout.addWidget(self.tags)
        tab4Layout.addWidget(self.pu_sinopse)
        mainTab4Layout.addLayout(tab4Layout)
    
    def makeButtons(self):
        self.btnGrava = QPushButton()
        self.btnGrava.setText('Grava')
        self.buttonsLayout.addWidget(self.btnGrava)
        self.btnGrava.clicked.connect(self.record_save)
        
        self.btnNovo = QPushButton('Novo')
        self.buttonsLayout.addWidget(self.btnNovo)
        self.btnNovo.clicked.connect(self.record_add)
        
        self.btnDuplica = QPushButton()
        self.btnDuplica.setText('Duplica')
        self.buttonsLayout.addWidget(self.btnDuplica)
        self.btnDuplica.clicked.connect(self.duplicar_registo)
        
        self.get_wookBtn = QPushButton('Wook')
        self.get_wookBtn.clicked.connect(self.get_wook_click)
        self.buttonsLayout.addWidget(self.get_wookBtn)
        
        
        self.btnSai = QPushButton()
        self.btnSai.setText('Sair')
        self.buttonsLayout.addWidget(self.btnSai)
        self.buttonsLayout.addStretch()
        self.btnSai.clicked.connect(self.exit_form)
    
    
    def get_wook_click(self):
        xl = isbn_lib.get_isbn_wook(self.pu_isbn.text())
        dum = self.tags.toPlainText().rstrip(',')
        tags_txt = dum.split(',')
        tags_data = []
        for n in tags_txt:
            toto = n.lower().strip()
            if toto != '':
                a = dbmain.query_one('select ta_id from tags where ta_name = %s', (toto,))
                tags_data.append((a, toto))
        tags_data.append((0,''))
        tags_data.append((0,''))
        tags_data.append((0, xl['pu_author']))
        tags_data.append((0, 'data:' + xl['pu_ed_date']))
        tags_data.append((0, 'ed:' + xl['pu_editor']))
        tags_data.append((0, xl['pu_lang']))
        tags_data.append((0, xl['pu_media']))
        tags_data.append((0, 'pag:' + xl['pu_pages']))
        tags_data.append((0, xl['pu_size']))
        
        form = tag_browser.EditRecordTags(tags_data)
        form.exec_()
        if form.flag:
            if form.tag_list == '':
                pass
            else:
                self.tags.setText('<font color="blue"><strong>' + form.tag_list)
    
    
    def add_from_isbn(self, data):
        t = []
        self.pu_title.setText(data['pu_title'])
        self.pu_isbn.setText(data['pu_isbn'])
        t.append('ed:' + data['pu_editor'].lower())
        t.append('data:' + data['pu_ed_date'])
        t.append('pag:' + data['pu_pages'])
        t.append(data['pu_media'].lower())
        t.append(data['pu_size'])
        if data['tag_author']:
            t.append(data['pu_author'].lower())
        self.pu_author_id.setEditText(data['pu_author'])
        self.pu_sinopse.setText(self.cleanTags(data['pu_sinopse']))
        if not data['pu_ed_year'] == '0':
            self.pu_ed_year.setText(data['pu_ed_year'])
        self.tags.setHtml('<font color="blue"><strong>' + ','.join(t))
    
    
    def exit_form(self):
        self.toto = False
        if not self.stored:
            responde = QMessageBox.warning(None,
                                           "Sair Antes de Gravar",
                                           """Atenção o registo ainda não foi gravado! Sair sem gravar? """,
                                           QMessageBox.StandardButtons(QMessageBox.Cancel | QMessageBox.Yes),
                                           QMessageBox.Cancel)
            if responde == QMessageBox.Yes:
                self.toto = True
                self.close()
        else:
            self.toto = True
            self.close()
    
    def record_save(self):
        # só grava não haver nenhuma alteração ás tabelas externas'
        """ insere """
        pa.ON_LOCAL = self.pu_cota.text().upper().strip()
        pa.TYPE = self.pu_type.currentIndex()
        pa.STATUS = self.pu_status.currentIndex()
        if self.item_data == -1:
            if self.check_new_record():
                # print 'insere registo'
                self.insert_record()
                self.toto = True
                self.close()
            else:
                form = missing_data.DadosWizard('\n'.join(self.error_list), ['Corrigir', 'Continuar mesmo assim'])
                form.exec_()
                
                if form.toto == 0:
                    print('Corrige')
                elif form.toto == 1:
                    print('continua')
                    self.fill_defaults()
                    self.check_new_record()
                    self.insert_record()
                    self.toto = True
                    self.close()
        else:
            if self.check_update_record():
                self.update_record()
                self.toto = True  # refresh
                self.close()
            else:
                result = QMessageBox.information(None, \
                                                 "Faltam os seguintes dados.",
                                                 '\n'.join(self.error_list),
                                                 QMessageBox.StandardButtons( \
                                                     QMessageBox.Close), QMessageBox.Close)
    
    def check_update_record(self):
        self.error_list = []
        if str(self.pu_title.text()) == '':
            self.error_list.append('Falta o titulo.')
        self.check_autor()
        self.check_genere()
        try:
            a = int(self.pu_volume.text())
        except ValueError:
            self.pu_volume.setText('1')
        
        if not self.error_list:
            return True
        else:
            return False
    
    def check_new_record(self):
        self.error_list = []
        if self.pu_title.text() == '':
            self.error_list.append('Falta o titulo.')
        self.pu_title.setText(self.pu_title.text().title())
        self.check_autor()
        self.check_genere()
        self.check_ISBN()
        self.check_status()
        try:
            a = int(self.pu_volume.text())
        except ValueError:
            self.pu_volume.setText('1')
        if not self.error_list:
            return True
        else:
            return False
    
    def check_ISBN(self):
        """ impede/informa quando há um ISBN duplicado """
        isbn = str(self.pu_isbn.text())
        if isbn != '':
            a = dbmain.query_one('select pu_isbn from livros where pu_isbn =%s', (isbn,))
            if a != None:
                if self.askForNew("ISBN duplicado.", "Já existe outra publicação com este ISBN\nAdiciono mais esta? ",
                                  isbn):
                    pass
                else:
                    self.error_list.append('O ISBN está duplicado')
    
    def check_autor(self):
        # autor
        dum = self.pu_author_id.currentText().strip()
        if len(dum) > 150:
            self.error_list.append('Nome do Autor com mais de 150 caracteres!')
        else:
            if dum == '':
                self.error_list.append('Não foi definido o Autor.')
            else:
                dum = stdio.authors_process(dum)
                if dum.lower() not in pa.autores_dict:
                    if self.askForNew("Foi encontrada um novo Autor", "Adicionar este Autor?", dum):
                        dbmain.execute_query('INSERT INTO authors (au_name) VALUES(%s); ', (dum,))
                        self.pu_author_id.setEditText(dum)
                        data_access.get_autores()
                    else:
                        self.error_list.append('Não foi definido o Autor.')
    
    def check_genere(self):
        # types
        dum = self.pu_type.currentText().strip()
        if dum == '':
            self.error_list.append('Não foi definido o Tipo.')
        else:
            if dum.lower() not in pa.types_dict:
                recordFlag = False
                if self.askForNew("Foi encontrada um novo types", "Adicionar este types?", dum):
                    self.pu_type.setEditText(dum)
                    dbmain.execute_query('INSERT INTO types (ty_name) VALUES(%s); ', (dum,))
                    data_access.get_types()
                else:
                    self.error_list.append('Não foi definido o Tipo.')
    
    def check_status(self):
        # editora
        dum = self.pu_status.currentText().strip()
        if dum == '':
            self.error_list.append('Não foi definido o Estado.')
        else:
            if dum.lower() not in pa.status_dict:
                recordFlag = False
                if self.askForNew("Foi encontrad um novo Estado.", "Adiciono este Estado/Lista?", dum):
                    self.pu_status.setEditText(dum)
                    dbmain.execute_query('INSERT INTO status (st_nome) VALUES(%s); ', (dum,))
                    data_access.get_status()
                else:
                    self.error_list.append('Não foi definido o Estado.')
    
    def askForNew(self, caption, prefix, text):
        if QMessageBox.information(None,
                                   "" + caption + "",
                                   "" + prefix + '\n' + text + "",
                                   QMessageBox.StandardButtons( \
                                           QMessageBox.Cancel | \
                                           QMessageBox.Ok),
                                   QMessageBox.Ok) == QMessageBox.Ok:
            return True
        else:
            return False
    
    def record_add(self):
        self.stored = False
        self.update_combo_boxes()
        self.init_record()
        self.btnDuplica.setDisabled(True)
    
    def record_clone(self):
        self.duplicaRegisto()
    
    def add_author_to_tags(self):
        self.tags.setHtml(self.tags.toHtml() + ',<font color="blue"><strong>' +self.pu_author_id.currentText().lower())
    
    def add_type_to_tags(self):
        self.tags.setHtml(self.tags.toHtml() + ',<font color="blue"><strong>' +self.pu_type.currentText().lower())
    
    def title_caps(self):
        a = isbn_lib.text_title(self.pu_title.text())
        self.pu_title.setText(a)
    
    def sub_title_caps(self):
        a = isbn_lib.text_title(self.pu_sub_title.text())
        self.pu_sub_title.setText(a)
    
    def add_tags_click(self):
        form = tag_browser.BrowserTags()
        form.exec_()
        if form.tag_list == '':
            pass
        else:
            if form.flag:
                if form.tag_id == 0:  # limpa todas as tags
                    self.tags.setHtml('<font color="blue"><strong>' + form.tag_list)
                else:
                    self.tags.setHtml('<font color="blue"><strong>' + self.tags.toPlainText() + ',' + form.tag_list)
    
    def edit_tags_click(self):
        dum = self.tags.toPlainText().rstrip(',')
        tags_txt = dum.split(',')
        tags_data = []
        for n in tags_txt:
            toto = n.lower().strip()
            if toto != '':
                a = dbmain.query_one('select ta_id from tags where ta_name = %s', (toto,))
                tags_data.append((a, toto))
        form = tag_browser.EditRecordTags(tags_data)
        form.exec_()
        if form.flag:
            if form.tag_list == '':
                pass
            else:
                self.tags.setHtml('<font color="blue"><strong>' + form.tag_list)
    
    def procField(self, aString):
        if aString == None:
            return ''
        else:
            return aString
    
    def fill_defaults(self):
        if str(self.pu_author_id.currentText().strip()) == '':
            self.pu_author_id.setEditText('Sem Autor')
        if str(self.pu_subject.currentText().strip()) == '':
            self.pu_subject.setEditText('Não Defenido')
        if str(self.pu_translator.currentText().strip()) == '':
            self.pu_translator.setEditText('Sem Tradutor')
        if str(self.pu_type.currentText().strip()) == '':
            self.pu_type.setEditText('Não Defenido')
        if str(self.pu_media.currentText().strip()) == '':
            self.pu_media.setEditText('Não Defenido')
        if str(self.pu_collection.currentText().strip()) == '':
            self.pu_collection.setEditText('Não Defenido')
        if str(self.pu_media_format.currentText().strip()) == '':
            self.pu_media_format.setEditText('Não Defenido')
        if str(self.pu_editor_id.currentText().strip()) == '':
            self.pu_editor_id.setEditText('Não Defenido')
    
    def init_record(self):
        self.item_data = -1
        self.pu_title.setText('')
        self.pu_sub_title.setText('')
        self.pu_isbn.setText('')
        self.pu_cota.setText('')
        self.pu_author_id.setEditText('')
        self.pu_ed_year.clear()
        self.tags.setText('')
        self.tags_stack = ''
        self.pu_volume.setText('1')
        self.pu_sinopse.clear()
        self.pu_obs.clear()
        
    def duplicar_registo(self):
        self.item_data = -1
        self.pu_title.setText('')
        self.pu_sub_title.setText('')
        self.pu_isbn.setText('')
        self.pu_sinopse.clear()
        self.pu_obs.clear()
        if int(self.pu_volume.text()) > 1:
            self.pu_volume.setText(str(int(self.pu_volume.text()) + 1))
        else:
            self.pu_volume.setText('1')
    
    def update_combo_boxes(self):
        # limpa os campos
        self.pu_author_id.clear()
        self.pu_author_id.addItems(pa.dsAutores)
        self.pu_type.clear()
        self.pu_type.addItems(pa.ds_types)
        self.pu_status.clear()
        self.pu_status.addItems(pa.dsStatus)
        self.pu_type.setCurrentText(pa.STATUS)
        self.pu_type.setCurrentText(pa.TYPE)
    
    def refresh_datafields(self):
        self.update_combo_boxes()
        read_record(self.pu_title, 'pu_title', self.item_data)
        read_record(self.pu_sub_title, 'pu_sub_title', self.item_data)
        read_record(self.pu_author_id, 'au_name', self.item_data)
        read_record(self.pu_isbn, 'pu_isbn', self.item_data)
        read_record(self.pu_cota, 'pu_cota', self.item_data)
        read_record(self.pu_type, 'ty_name', self.item_data)
        read_record(self.pu_volume, 'pu_volume', self.item_data)
        self.pu_status.setCurrentIndex(self.item_data['st_id'] - 1)
        read_record(self.pu_obs, 'pu_obs', self.item_data)
        read_record(self.pu_sinopse, 'pu_sinopse', self.item_data)
        read_record(self.pu_ed_year, 'pu_ed_year', self.item_data)
        self.tags_stack = self.get_tags_from_record()
        self.tags.setHtml('<font color="blue"><strong>' + self.tags_stack)
    
    def get_tags_from_record(self):
        sql = 'SELECT tags.ta_name FROM tag_ref INNER JOIN public.tags ON (public.tag_ref.tr_tag = public.tags.ta_id)\
        where tag_ref.tr_book = ' + str(self.id)
        a = dbmain.query_many(sql )
        tags = ''
        for n in a:
            ##print type(n[0])
            tags += n[0].lower() + ','
        return tags.rstrip(',')
    
    def insert_record(self):
        sql = '''insert into livros (
        pu_author_id, pu_cota , pu_type, pu_isbn , pu_obs,
        pu_sinopse, pu_status, pu_title, pu_volume,pu_ed_year, pu_sub_title)
        VALUES ((select au_id from authors where lower(au_name)=%s),%s,(select ty_id from types where lower(ty_name)=%s)
        ,%s,%s,%s,(select st_id from status where lower(st_nome)=%s),%s,%s,%s,%s)'''
        data = (stdio.authors_process(self.pu_author_id.currentText()).lower(),self.pu_cota.text().upper(),)
        data += (self.pu_type.currentText().lower(),self.pu_isbn.text().strip(),)
        data += (self.pu_obs.toPlainText(),)
        data += (self.pu_sinopse.toPlainText(),)
        data += (self.pu_status.currentText().lower(),)
        data += (self.pu_title.text().strip(),)
        data += (self.pu_volume.text(),write_record(self.pu_ed_year),self.pu_sub_title.text())
        a = dbmain.execute_query(sql, data)
        
        ''' campos especiais '''
        self.id = dbmain.query_one('select max(pu_id) from livros', (True,))[0]
        pa.last_id = self.id
        ''' actualiza obs'''
        self.update_tags()
        pa.TYPE = self.pu_type.currentText()
        pa.STATUS = self.pu_status.currentText()
    
    def update_record(self):
        sql = '''UPDATE livros SET 
        pu_author_id=(select au_id from authors where lower(au_name)=%s),
        pu_cota =%s,
        pu_type=(select ty_id from types where lower(ty_name)=%s),
        pu_isbn =%s,
        pu_obs=%s,
        pu_sinopse=%s,
        pu_status=(select st_id from status where lower(st_nome)=%s),
        pu_title=%s,
        pu_volume=%s,
        pu_ed_year=%s,
        pu_sub_title=%s
        WHERE pu_id = %s'''
        
        data = (self.pu_author_id.currentText().lower(),)
        data += (self.pu_cota.text().upper().strip(),)
        data += (self.pu_type.currentText().lower(),)
        data += (self.pu_isbn.text().strip(),)
        data += (self.pu_obs.toPlainText(),)
        data += (self.pu_sinopse.toPlainText(),)
        data += (self.pu_status.currentText().lower(),)
        data += (self.pu_title.text().strip(),)
        data += (self.pu_volume.text().upper(),)
        data += (write_record(self.pu_ed_year), self.pu_sub_title.text())
        
        data += (self.item_data['pu_id'],)
        
        a = dbmain.execute_query(sql, data)
        ''' actualiza obs'''
        if str(self.tags_stack) != str(self.tags.toPlainText()):
            self.update_tags()
        pa.TYPE = self.pu_type.currentText()
        pa.STATUS = self.pu_status.currentText()
    
    def update_tags(self):
        ''' get tags'''
        xl = self.tags.toPlainText()    #.rstrip(',')
        xl = xl.replace(',,',',')
        xl = xl.rstrip(',')
        xl = xl.lstrip(',')
        tags_list = xl.split(',')
        tags_list = stdio.remove_duplicates(tags_list)
        if tags_list[0] == '':
            cleantag_rfs = dbmain.execute_query('delete from tag_ref where tr_book = %s', (self.id,))
        else:
            cleantag_rfs = dbmain.execute_query('delete from tag_ref where tr_book = %s', (self.id,))
            data_access.update_tags(self.id, tags_list)
    
    def cleanTags(self, text):
        # remove the newlines
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = " ".join(text.split())
        text = text.replace('<lm', '')
        text = text.replace('<br', '')
        text = text.replace('<b', '')
        text = text.replace('/', '')
        return text


def write_record(obj, dic={}):
    a = type(obj)
    if a == QLineEdit:
        if obj.text() == '':
            return None
        else:
            return obj.text()
    elif a == QCheckBox:
        return obj.isChecked()
    elif a == QPlainTextEdit:
        return obj.toPlainText()
    elif a == QComboBox:
        if dic == {}:
            return obj.currentText()
        else:
            return dic[obj.currentText().lower()]


def read_record(obj, field, dic):
    try:
        a = type(obj)
        toto = dic[field]
        if toto == None:
            pass
        elif a == QCheckBox:
            obj.setChecked(toto)
        elif a == QLineEdit:
            if type(toto) == int:
                obj.setText(str(toto))
            else:
                obj.setText(toto)
        elif a == QTextEdit:
            obj.setText(toto)
        elif a == QPlainTextEdit:
            obj.appendPlainText(toto)
        elif a == QComboBox:
            obj.setEditText(toto)
        elif a == QDateEdit:
            obj.setDate(toto)
    except Exception as e:
        print('erro em def read_record()')
        print(str(e) + '\n ', obj.objectName(), '\nin field:', field, '\nin dic:', dic)

#
# def text_title(txt):
#     a = txt.title()
#     a = a.split(' ')
#     bc = [a[0]]
#     for n in range(1,len(a)):
#         if a[n].lower() in pa.prep_set:
#             bc.append(a[n].lower())
#         else:
#             bc.append(a[n])
#     return ' '.join(bc)
    

def main():
    pass

if __name__ == '__main__':
    main()
