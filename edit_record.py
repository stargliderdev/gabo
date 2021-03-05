#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QLabel, QCheckBox, QVBoxLayout, QLineEdit, QComboBox, QDateEdit, \
    QWidget, QDialog, QHBoxLayout, QToolButton, QPushButton, QTextEdit, QMessageBox, QPlainTextEdit,QTextBrowser

from PyQt5.Qt import Qt

import browser
import isbn_lib
import lib_tags
import parameters as gl
import dmPostgreSQL as dbmain
import data_access as data_access
import missing_data
import tags_special
from qlib import addHLayout,HLine
import tag_browser
import stdio
import locals


class EditRecord(QDialog):
    def __init__(self, pub_id, draft_data=True, copy=0, parent=None):
        """draft_data: data from wook not saved
           data: a dictionary from wook """
        super(EditRecord, self).__init__(parent)
        self.setWindowTitle('Edita Livros')
        self.resize(1024, 768)
        self.error_list = []
        gl.userError = ''
        self.draft_data = draft_data
        # self.data = data
        self.toto = False
        self.pub_id = pub_id
        self.up_date_special_tags = False
        # self.tags_special_level1_data = (False,[])
        mainLayout = QVBoxLayout(self)
        self.buttonsLayout = QHBoxLayout()
        # tabs
        self.titleLayout = QVBoxLayout()
        self.make_buttons()
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
        
        if self.pub_id == -1:
            # new
            self.item_data = -1
            self.record_add()
            if self.draft_data:
                self.add_from_webbrowser()
            
        else:
            # old
            
            # if copy == 0:
            if data_access.get_book_data(self.pub_id):
                self.refresh_datafields()
            #     # record on database
            #     self.refresh_datafields()
            # elif copy == 1:
            #     self.item_data = data_access.get_book_data(self.pub_id)
            #     self.refresh_datafields()
            #     self.duplicar_registo()
            # elif copy == 2:
            #     self.item_data = data_access.get_book_data(self.pub_id)
            #     toto = self.item_data
            #     self.refresh_datafields()
            #     self.duplicar_registo()
            #     read_record(self.pu_title, 'pu_title', toto)
            #     read_record(self.pu_isbn, 'pu_isbn', toto)
            #     read_record(self.pu_cota, 'pu_cota', toto)
        self.pu_title.setFocus()
        
        self.stored = True
        # if self.pu_cota.text() == '':
        #     self.pu_cota.setText(gl.ON_LOCAL)
    
    def make_title(self):
        self.pu_title = QLineEdit()
        titleCapitalize = QToolButton()
        titleCapitalize.setIcon(QIcon('./img/caps.png'))
        titleCapitalize.setToolTip('Capitaliza Titulo')
        titleCapitalize.clicked.connect(self.title_caps)
        searchTitleBtn = QToolButton()
        searchTitleBtn.setIcon(QIcon('./img/chrome.png'))
        searchTitleBtn.setToolTip('Pesquisa na internet')
        searchTitleBtn.clicked.connect(self.title_internet_search)
        
        
        self.pu_volume = QLineEdit()
        self.pu_volume.setMaximumWidth(40)
        self.pu_volume.setMaxLength(3)
        
        self.pu_ed_year = QLineEdit()
        self.pu_ed_year.setMaximumWidth(60)
        self.pu_ed_year.setMaxLength(4)
        
        self.titleLayout.addLayout(addHLayout(['Titulo:', self.pu_title,titleCapitalize,searchTitleBtn]))
        self.titleLayout.addLayout(addHLayout(['Volume:', self.pu_volume, 'Ano',self.pu_ed_year, True]))
        self.pu_sub_title = QLineEdit()
        self.pu_sub_title.setMaxLength(255)
        subTitleCapitalize = QToolButton()
        # setSize(subTitleCapitalize)
        subTitleCapitalize.setIcon(QIcon('./img/caps.png'))
        subTitleCapitalize.setToolTip('Capitaliza sub-titulo')
        subTitleCapitalize.clicked.connect(self.sub_title_caps)
        self.titleLayout.addLayout(addHLayout(['Sub-titulo:', self.pu_sub_title,subTitleCapitalize]))
        labelpu_author_id = QLabel('Autor:')
        labelpu_author_id.setAlignment(Qt.AlignRight)
        
        self.pu_author_id = QComboBox(self)
        self.pu_author_id.setEditable(True)
        authorToTagBtn = QToolButton()
        authorToTagBtn.setIcon(QIcon('./img/green.png'))
        authorToTagBtn.setToolTip('Adiciona autor ás etiquetas')
        searchAuthorBtn = QToolButton()
        searchAuthorBtn.setIcon(QIcon('./img/chrome.png'))
        searchAuthorBtn.setToolTip('Pesquisa na internet')
        searchAuthorBtn.clicked.connect(self.author_internet_search)
        authorToTagBtn.clicked.connect(self.add_author_to_tags)
        self.titleLayout.addLayout(addHLayout(['Autor:', self.pu_author_id,authorToTagBtn,searchAuthorBtn]))
        
        self.pu_type = QComboBox()
        self.pu_type.setEditable(True)
        typeToTagBtn = QToolButton()
        # setSize(typeToTagBtn)
        typeToTagBtn.setIcon(QIcon('./img/green.png'))
        typeToTagBtn.setToolTip('Adiciona tipo às etiquetas')
        typeToTagBtn.clicked.connect(self.add_type_to_tags)
        self.pu_cota = QLineEdit()
        self.pu_cota.setObjectName('pu_cota')
        self.pu_cota.setMaxLength(10)
        self.pu_status = QComboBox()
        self.pu_status.setEditable(True)
        
        self.titleLayout.addLayout(addHLayout(['Tipo:', self.pu_type,typeToTagBtn, 'Estado:', self.pu_status]))
        
        self.pu_isbn = QLineEdit()
        self.pu_isbn.setMaxLength(20)

        searchIsbnBtn = QToolButton()
        searchIsbnBtn.setIcon(QIcon('./img/chrome.png'))
        searchIsbnBtn.setToolTip('Pesquisa na internet')
        searchIsbnBtn.clicked.connect(self.isbn_internet_search)
        
        # self.pu_isbn10 = QLineEdit()
        # self.pu_isbn10.setMaxLength(10)
        #
        # self.pu_isbn10.setObjectName('pu_isbn10')
        self.pu_depLegal = QLineEdit()
        self.pu_depLegal.setMaxLength(20)
        setLocalBtn = QToolButton()
        setLocalBtn.setIcon(QIcon('./img/blue.png'))
        setLocalBtn.setToolTip('Ver locais')
        setLocalBtn.clicked.connect(self.set_local_click)
        pasteLocalBtn = QToolButton()
        pasteLocalBtn.setIcon(QIcon('./img/paste.png'))
        pasteLocalBtn.setToolTip('Cola o ultimo local')
        pasteLocalBtn.clicked.connect(self.paste_local_click)
        self.titleLayout.addLayout(addHLayout(['ISBN:', self.pu_isbn,searchIsbnBtn, 'Cota:', self.pu_cota,setLocalBtn,pasteLocalBtn]))
    
    
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
        sizesTBtn = QToolButton()
        sizesTBtn.clicked.connect(self.show_sizes_click)
        specialTagsBtn = QToolButton()
        specialTagsBtn.setText('Caracteristicas')
        specialTagsBtn.clicked.connect(self.edit_special_tags_click)
        sizesTBtn = QToolButton()
        sizesTBtn.clicked.connect(self.show_sizes_click)
        self.pu_sinopse = QTextEdit()
        tab4Layout.addLayout(addHLayout([addTags, editTags,specialTagsBtn,True,sizesTBtn]))
        tab4Layout.addWidget(self.tags)
        tab4Layout.addWidget(self.pu_sinopse)
        mainTab4Layout.addLayout(tab4Layout)
    
    def make_buttons(self):
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
        
        self.openWookBtn = QPushButton('Wook')
        self.openWookBtn.clicked.connect(self.open_wook_click)
        self.buttonsLayout.addWidget(self.openWookBtn)
        
        self.btnSai = QPushButton()
        self.btnSai.setText('Sair')
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.btnSai)
        self.btnSai.clicked.connect(self.exit_form)

    
    def add_from_webbrowser(self,):
        self.pu_title.setText(gl.record_current_dict['pu_title'])
        self.pu_isbn.setText(gl.record_current_dict['isbn'])
        self.pu_sub_title.setText(gl.record_current_dict['pu_sub_title'])
        self.pu_author_id.setEditText(gl.record_current_dict['pu_author'])
        self.pu_sinopse.setText(self.cleanTags(gl.record_current_dict['pu_sinopse']))
        if gl.record_current_dict['pu_ed_year'] == '0':
            self.pu_ed_year.setText('0')
        else:
            self.pu_ed_year.setText(gl.record_current_dict['pu_ed_year'])
        self.tags.setHtml('<font color="blue"><strong>' + gl.record_current_dict['pu_tags'])
    
    def open_wook_click(self):
        form = browser.BrowserInLine("https://www.wook.pt/")
        form.exec_()
    
    def exit_form(self):
        self.toto = False
        if not self.stored:
            responde = QMessageBox.warning(None,
                                           "Sair Antes de Gravar",
                                           """Atenção o registo ainda não foi gravado! \nSair sem gravar? """,
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
        gl.ON_LOCAL = self.pu_cota.text().upper().strip()
        gl.TYPE = self.pu_type.currentIndex()
        gl.STATUS = self.pu_status.currentIndex()
        if self.pub_id == -1:
            # if self.draft_data:
            if self.check_new_record():
                self.insert_record()
                self.toto = True
                self.close()
            else:
                form = missing_data.DadosWizard('\n'.join(self.error_list), ['Corrigir'])
                form.exec_()
                # if form.toto == 0:
                #     print('Corrige')
                # elif form.toto == 1:
                #     print('continua')
                #     self.fill_defaults()
                #     self.check_new_record()
                #     self.insert_record()
                #     self.toto = True
                #     self.close()
                
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
                if dum.lower() not in gl.autores_dict:
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
            if dum.lower() not in gl.types_dict:
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
            if dum.lower() not in gl.status_dict:
                recordFlag = False
                if self.askForNew("Foi encontrad um novo Estado.", "Adiciono este Estado/Lista?", dum):
                    self.pu_status.setEditText(dum)
                    dbmain.execute_query('INSERT INTO status (st_nome) VALUES(%s); ', (dum,))
                    data_access.get_status()
                else:
                    self.error_list.append('Não foi definido o Estado.')
    
    def askForNew(self, caption, prefix, text):
        if QMessageBox.information(None,caption , prefix + '\n' + text,
                                   QMessageBox.StandardButtons(QMessageBox.Cancel |QMessageBox.Ok), QMessageBox.Ok) == QMessageBox.Ok:
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
    
    def set_local_click(self):
        form = locals.BrowserLocals()
        form.exec_()
        if not form.toto == '':
            self.pu_cota.setText(form.toto)
            gl.ON_LOCAL = form.toto
    
    def paste_local_click(self):
        if gl.ON_LOCAL != '':
            self.pu_cota.setText(gl.ON_LOCAL)
    
    def add_author_to_tags(self):
        self.tags.setHtml(self.tags.toHtml() + ',<font color="blue"><strong>' +self.pu_author_id.currentText().lower())
    
    def add_type_to_tags(self):
        self.tags.setHtml(self.tags.toHtml() + ',<font color="blue"><strong>' +self.pu_type.currentText().lower())
    
    def title_caps(self):
        a = isbn_lib.text_title(self.pu_title.text())
        self.pu_title.setText(a)

    def title_internet_search(self):
        stdio.search_internet(self.pu_title.text())
    
    def isbn_internet_search(self):
        stdio.search_internet('ISBN ' + self.pu_isbn.text())

    def author_internet_search(self):
        stdio.search_internet(self.pu_author_id.currentText())

   
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

    def edit_special_tags_click(self):
        if self.draft_data:
            form = tags_special.EditSpecialTags(0)
        else:
            form = tags_special.EditSpecialTags(self.pub_id)
        form.exec_()
        # save pub special tags
        if form.flag:
            if self.pub_id > 0:
                lib_tags.update_special_tags(self.pub_id, 1)
                gl.update_special_tags = False
        # else:
        #     self.tags_special_level1_data = (False,[])
        
    def show_sizes_click(self):
        pass
    
    def previous_record_click(self):
        for n in gl.FILTER_DATASET:
            print(n[0])
    
    def procField(self, aString):
        if aString is None:
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
        self.pu_author_id.addItems(gl.dsAutores)
        self.pu_type.clear()
        self.pu_type.addItems(gl.ds_types)
        self.pu_status.clear()
        self.pu_status.addItems(gl.dsStatus)
        self.pu_type.setCurrentText(gl.STATUS)
        self.pu_type.setCurrentText(gl.TYPE)
    
    def refresh_datafields(self):
        """record on database"""
        self.update_combo_boxes()
        self.pu_title.setText(gl.record_current_dict['pu_title'])
        self.pu_sub_title.setText(gl.record_current_dict['pu_sub_title'])
        self.pu_author_id.setCurrentText(gl.record_current_dict['au_name'])
        read_record(self.pu_isbn, 'pu_isbn', gl.record_current_dict)
        read_record(self.pu_cota, 'pu_cota', gl.record_current_dict)
        read_record(self.pu_type, 'ty_name', gl.record_current_dict)
        read_record(self.pu_volume, 'pu_volume', gl.record_current_dict)
        self.pu_status.setCurrentIndex(gl.record_current_dict['st_id'] - 1)
        read_record(self.pu_obs, 'pu_obs', gl.record_current_dict)
        read_record(self.pu_sinopse, 'pu_sinopse', gl.record_current_dict)
        read_record(self.pu_ed_year, 'pu_ed_year', gl.record_current_dict)
        self.tags_stack = self.get_tags_from_record()
        self.tags.setHtml('<font color="blue"><strong>' + self.tags_stack)
    
    def get_tags_from_record(self):
        sql = 'SELECT tags.ta_name FROM tags_reference INNER JOIN public.tags ON (public.tags_reference.tags_ref_tag_id = public.tags.ta_id)\
        where tags_reference.tags_ref_book =%s and tags_ref_level =0' # + str(self.pub_id)
        a = dbmain.query_many(sql, (self.pub_id,))
        tags = ''
        for n in a:
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
        dbmain.execute_query(sql, data)
        
        ''' campos especiais '''
        self.pub_id = dbmain.query_one('select max(pu_id) from livros', (True,))[0]
        gl.last_id = self.pub_id
        ''' actualiza obs'''
        self.update_tags()
        gl.TYPE = self.pu_type.currentText()
        gl.STATUS = self.pu_status.currentText()
    
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
        data += (self.pu_isbn.text().strip().replace('-',''),)
        data += (self.pu_obs.toPlainText(),)
        data += (self.pu_sinopse.toPlainText(),)
        data += (self.pu_status.currentText().lower(),)
        data += (self.pu_title.text().strip(),)
        data += (self.pu_volume.text().upper(),)
        data += (write_record(self.pu_ed_year), self.pu_sub_title.text())
        
        data += (self.pub_id,)
        
        a = dbmain.execute_query(sql, data)
        ''' actualiza obs'''
        # if str(self.tags_stack) != str(self.tags.toPlainText()):
        
        self.update_tags()
        gl.TYPE = self.pu_type.currentText()
        gl.STATUS = self.pu_status.currentText()
    
    def update_tags(self):
        ''' get tags'''
        xl = self.tags.toPlainText()    #.rstrip(',')
        xl = xl.replace(',,',',')
        xl = xl.rstrip(',')
        xl = xl.lstrip(',')
        tags_list = xl.split(',')
        tags_list = stdio.remove_duplicates(tags_list)
        if tags_list[0] == '':
            dbmain.execute_query('delete from tags_reference where tags_ref_book = %s and tags_ref_level=0', (self.pub_id,))
        else:
            dbmain.execute_query('delete from tags_reference where tags_ref_book = %s and tags_ref_level=0', (self.pub_id,))
            data_access.update_tags(self.pub_id, tags_list)
        # if self.tags_special_level1_data[0]:
        if self.up_date_special_tags:
            lib_tags.update_special_tags(self.pub_id, 1)
    
    
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


def main():
    pass

if __name__ == '__main__':
    main()
