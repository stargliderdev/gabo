#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections
import random
from typing import Collection

from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDateEdit, QDialog,
                             QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                             QPlainTextEdit, QPushButton, QTabWidget,
                             QTextBrowser, QTextEdit, QToolButton, QVBoxLayout,
                             QWidget)

import authors
import bindings
import classifications
import conditions
import colections
import isbn_lib
import languages
import lib_tags
import locals
import parameters as gl
import sqlite_crud
from pu_source import SourceBrowser
import pub_types
from publishers import PublishersBrowser
import series
import status
import stdio
import tag_browser
import tags_manage
import qlib as qc


class EditRecord(QDialog):
    def __init__(self, pub_id, copy=0, navigator=-1, parent=None):
        """navigator >-1 numero da coluna index da lista
                     """
        super(EditRecord, self).__init__(parent)
        self.setWindowTitle('Edita Livros')
        self.setWindowIcon(QIcon('./img/edit_record.png'))
        self.resize(800, 600)
        self.error_list = []
        self.tags_refresh_flag = False
        gl.userError = ''
        self.navigator = navigator
        self.toto = False
        self.pub_id = pub_id
        self.up_date_special_tags = False
        if self.pub_id == -1:
            # new
            self.item_data = -1
        else:
            sqlite_crud.get_book_data(self.pub_id)

        mainLayout = QVBoxLayout(self)
        self.buttonsLayout = QHBoxLayout()
        # tabs
        #
        self.make_buttons()
        self.make_title()
        self.tabuladorTabWidget = QTabWidget()
        self.makeTab2()
        self.makeTab4()
        self.makeTab5()
        self.tabuladorTabWidget.setTabPosition(3)
        self.tabuladorTabWidget.addTab(self.tab1,'Principal')
        self.tabuladorTabWidget.addTab(self.tab5, 'Outros')
        self.tabuladorTabWidget.addTab(self.tab4, 'Etiquetas')
        self.tabuladorTabWidget.addTab(self.tab2, 'Observações')
        mainLayout.addLayout(self.buttonsLayout)
        mainLayout.addWidget(qc.HLine())
        # mainLayout.addLayout(self.titleLayout)
        mainLayout.addWidget(self.tabuladorTabWidget)
        
        if self.pub_id == -1:
            # new
            self.item_data = -1
            self.record_add()
        else:
            self.refresh_datafields()
        self.pu_title.setFocus()
        self.stored = True
    
    def make_title(self):
        self.tab1 = QWidget()
        mainTab1Layout = QVBoxLayout(self.tab1)
        tab1Layout = QHBoxLayout()
        self.titleLayout = QVBoxLayout()
        # self.pu_obs = QTextEdit()
        # tab1Layout.addWidget(self.pu_obs)
        mainTab1Layout.addLayout(tab1Layout)
        self.pu_title = QLineEdit()
        self.pu_title.setObjectName('pu_title')
        # titleCapitalize = QToolButton()
        # titleCapitalize.setIcon(QIcon('./img/caps.png'))
        # titleCapitalize.setToolTip('Capitaliza Titulo')
        # titleCapitalize.clicked.connect(self.title_caps)
        searchTitleBtn = QToolButton()
        searchTitleBtn.setIcon(QIcon('./img/chrome.png'))
        searchTitleBtn.setToolTip('Pesquisa na internet')
        searchTitleBtn.clicked.connect(self.title_internet_search)
        pu_volumeLabel = QLabel('Volume:')
        self.pu_volume = QLineEdit()
        self.fix_size(self.pu_volume,50)
        pu_yearLabel = QLabel('Ano:')
        self.pu_year = QLineEdit()
        self.fix_size(self.pu_year,50)
        self.pu_year.setMaximumWidth(60)
        self.pu_year.setMinimumWidth(60)
        self.pu_year.setMaxLength(12)
        self.pu_sub_title = QLineEdit()
        self.pu_sub_title.setMaxLength(255)
        pu_editionLabel = QLabel('Edição')
        self.pu_edition = QLineEdit()
        self.fix_size(self.pu_edition, 50)
        self.pu_edition.setMaximumWidth(50)
        self.pu_edition.setMinimumWidth(50)
        self.pu_edition_date = QLineEdit()
        self.pu_edition_date.setMaximumWidth(70)
        self.pu_edition_date.setMinimumWidth(70)
        pu_edition_dateLabel = QLabel('Data Ed.:')
        pu_publisherLabel = QLabel('<a href="pu_publisher" >Editora:</a>')
        pu_publisherLabel.linkActivated.connect(self.link_click)
        self.fix_size(pu_publisherLabel)
        self.pu_publisher = QLineEdit()
        self.pu_type = QComboBox()
        self.pu_type.setMinimumWidth(200)
        self.pu_type.setEditable(True)
        pu_typeLabel = QLabel('<a href="pu_type" >Tipo:</a>')
        pu_typeLabel.linkActivated.connect(self.link_click)

        # self.pu_edition_place = QLineEdit()
        pu_authorLabel = QLabel('<a href="pu_author" >Autor:</a>')
        self.fix_size(pu_authorLabel, 80)
        pu_authorLabel.linkActivated.connect(self.link_click)
        self.pu_author_id = QComboBox(self)
        self.pu_author_id.setMinimumWidth(320)
        self.pu_author_id.setEditable(True)
        searchAuthorBtn = QToolButton()
        searchAuthorBtn.setIcon(QIcon('./img/chrome.png'))
        searchAuthorBtn.setToolTip('Pesquisa na internet')
        searchAuthorBtn.clicked.connect(self.author_internet_search)

        self.pu_dimensions = QLineEdit()
        self.pu_dimensions.setMaximumWidth(130)
        self.pu_dimensions.setMinimumWidth(130)
        dimentionsTBnt = QToolButton()
        dimentionsTBnt.setIcon(QIcon('./img/dimentions.png'))
        dimentionsTBnt.setToolTip('Converte dimensões de cm, in para mm')
        dimentionsTBnt.clicked.connect(self.convert_dim_click)
        
        pu_pagesLabel = QLabel('Páginas:')
        self.pu_pages = QLineEdit()
        self.pu_pages.setMaximumWidth(40)
        self.pu_pages.setMinimumWidth(40)
        pu_coverLabel = QLabel('<a href="pu_cover" >Encadernação:</a>')
        # pu_coverLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        pu_coverLabel.linkActivated.connect(self.link_click)
        self.pu_cover = QComboBox()
        self.pu_cover.setEditable(True)
        self.pu_cover.addItems(gl.covers_list)
        self.pu_cover.setMaximumWidth(120)
        self.pu_cover.setMinimumWidth(120)
        self.pu_volume_collection = QLineEdit()
        self.fix_size(self.pu_volume_collection, 50)
        self.pu_volume_serie = QLineEdit()
        self.fix_size(self.pu_volume_serie, 50)
        pu_collectionLabel = QLabel('<a href="pu_collection" >Colecção:</a>')
        self.fix_size(pu_collectionLabel)
        pu_collectionLabel.linkActivated.connect(self.link_click)
        self.pu_collection = QLineEdit()
        self.pu_collection.setObjectName('pu_collection')
        self.fix_size(self.pu_collection, 300)
        pu_languageLabel = QLabel('<a href="pu_language" >Idioma:</a>')
        pu_languageLabel.linkActivated.connect(self.link_click)
        self.pu_language = QComboBox()
        self.pu_language.setEditable(True)
        self.pu_language.addItems(gl.languages_list)
        self.pu_local = QLineEdit()
        self.pu_local.setMaximumWidth(100)
        self.pu_local.setMinimumWidth(100)
        self.pu_local.setMaxLength(10)
        # pu_statusLabel = QLabel('Situação:')
        pu_statusLabel = QLabel('<a href="pu_status" >Situação:</a>')
        # pu_statusLabel.setAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.fix_size(pu_statusLabel,80)
        pu_statusLabel.linkActivated.connect(self.link_click)
        self.pu_status = QComboBox()
        self.pu_status.setEditable(True)
        self.pu_status.setMaximumWidth(160)
        self.pu_status.setMinimumWidth(160)
        pu_priceLabel = QLabel('Preço:')

        # pu_sourceLabel = QLabel('<a href="pu_source" >Origem:</a>')
        # pu_sourceLabel.setAlignment(Qt.AlignVCenter|Qt.AlignRight)
        # pu_sourceLabel.linkActivated.connect(self.link_click)

        self.pu_isbn = QLineEdit()
        self.pu_isbn.setMaxLength(20)
        self.pu_isbn.setMaximumWidth(140)
        self.pu_isbn.setMinimumWidth(140)
        searchIsbnBtn = QToolButton()
        searchIsbnBtn.setToolTip('Pesquisa na internet')
        searchIsbnBtn.setIcon(QIcon('./img/chrome.png'))
        searchIsbnBtn.clicked.connect(self.isbn_internet_search)
        pu_localLabel = QLabel('<a href="pu_local" >Local:</a>')
        pu_localLabel.linkActivated.connect(self.link_click)
        pasteLocalBtn = QToolButton()
        pasteLocalBtn.setIcon(QIcon('./img/paste.png'))
        pasteLocalBtn.setToolTip('Cola o ultimo local')
        pasteLocalBtn.clicked.connect(self.paste_local_click)
        # pu_volume_collectionLabel = QLabel('Volume:')
        pu_conditionLabel = QLabel ('<a href="pu_condition" >Estado Fisico:</a>')
        # pu_conditionLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.fix_size(pu_conditionLabel)
        pu_conditionLabel.linkActivated.connect(self.link_click)
        self.pu_condition = QComboBox()
        self.pu_condition.setMinimumWidth(120)
        self.pu_condition.setEditable(True)
        self.pu_condition.addItems(gl.conditions_list)
        self.pu_condition.setCurrentIndex(-1)

        pu_serieLabel = QLabel('<a href="pu_serie" >Série:</a>')
        # pu_serieLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.fix_size(pu_serieLabel)
        pu_serieLabel.linkActivated.connect(self.link_click)
        self.pu_serie = QLineEdit()
        self.fix_size(self.pu_serie,300)
        self.pu_sinopse = QTextEdit()
        " add objectos to layouts"
        self.titleLayout.addLayout(qc.addHLayout(['Titulo:', self.pu_title,pu_volumeLabel, self.pu_volume,
                                               searchTitleBtn ]))
        self.titleLayout.addLayout(qc.addHLayout(['Sub-titulo:', self.pu_sub_title]))
    
        self.titleLayout.addLayout(qc.addHLayout([pu_authorLabel, self.pu_author_id,searchAuthorBtn,pu_typeLabel, self.pu_type,True
                                               ]))
        self.titleLayout.addLayout(qc.addHLayout([pu_publisherLabel ,self.pu_publisher, pu_editionLabel,self.pu_edition,pu_yearLabel,self.pu_year,
                                               pu_edition_dateLabel,self.pu_edition_date]))
        self.titleLayout.addLayout(qc.addHLayout(['Dimensões:', self.pu_dimensions, dimentionsTBnt, pu_pagesLabel, self.pu_pages,
                                               pu_coverLabel, self.pu_cover, pu_languageLabel, self.pu_language, True]))
        self.titleLayout.addLayout(qc.addHLayout([pu_collectionLabel, self.pu_collection,'Volume:', self.pu_volume_collection, True]))
        self.titleLayout.addLayout(qc.addHLayout([pu_serieLabel, self.pu_serie,'Volume:',self.pu_volume_serie,True]))
        self.titleLayout.addLayout(qc.addHLayout(['ISBN:', self.pu_isbn, searchIsbnBtn, pu_localLabel, self.pu_local, pasteLocalBtn, True]))
        self.titleLayout.addLayout(qc.addHLayout([pu_statusLabel, self.pu_status,pu_conditionLabel, self.pu_condition,True]))
        self.titleLayout.addWidget(self.pu_sinopse)
        mainTab1Layout.addLayout(self.titleLayout)
        
    
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
        # self.pu_sinopse = QTextEdit()
        # tab3Layout.addWidget(self.pu_sinopse)
        mainTab3Layout.addLayout(tab3Layout)
    
    def makeTab4(self):
        if self.tags_refresh_flag == True:
            print('apaga layout')
            # self.tab4Layout.deleteLater()
            # for i in reversed(list(range(self.tab4Layout.count()))):
            #     if self.tab4Layout.itemAt(i).widget() is None:
            #         pass
            #     else:
            #         self.tab4Layout.itemAt(i).widget().deleteLater()
            for i in reversed(range(self.dumLayout.count())):
                print('delete widget in layout')
                widget = self.dumLayout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
        self.tab4 = QWidget()
        mainTab4Layout = QVBoxLayout(self.tab4)
        self.tab4Layout = QVBoxLayout()
        # self.tags = QTextBrowser()
        self.dumLayout = QHBoxLayout()
        try:
            x = gl.record_current_dict['pu_tags']
        except KeyError:
            gl.record_current_dict['pu_tags'] = ''
        try:
            tags_list = gl.record_current_dict['pu_tags'].split('|')
            char_count = 0
            limit = 70
            color_txt = "#0000FF"
            # print(tags_list)
            for n in tags_list:
                # print('add labels')
                tx = n.strip()
                char_count = char_count + len(tx)
                label = QLabel(tx)
                color_background = "#{:02x}{:02x}{:02x}".format(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                # label.setStyleSheet("color:" + color_txt + "; background-color:" + color_background + ";border: 1px solid brown")
                css = '''
            
                color: ''' + color_txt + '''; /* Set text color */
                font-size: 14px; /* Set font size */
                font-weight: bold; /* Set font weight */
                background-color: ''' + color_background + '''; /* Set background color */
                border: 2px solid #336699; /* Add a border */
                padding: 2px; /* Add padding */
                border-radius: 4px; /* Add border radius */
            
                '''
                label.setStyleSheet(css)
                self.dumLayout.addWidget(label)

                # line +=1
                if char_count >= limit:
                    char_count = 0
                    self.tab4Layout.addLayout(self.dumLayout)
                    self.dumLayout=QHBoxLayout()
        except AttributeError:
            gl.record_current_dict['pu_tags'] = ''
        self.tab4Layout.addLayout(self.dumLayout)
        self.tab4Layout.addStretch()
        mainTab4Layout.addLayout(self.tab4Layout)

    def makeTab5(self):
        self.tab5 = QWidget()
        mainTab5Layout = QVBoxLayout(self.tab5)
        tab5Layout = QVBoxLayout()

        self.pu_translator = QLineEdit()
        self.pu_translator.setObjectName('pu_translator')
        self.pu_color = QLineEdit()
        self.pu_draw = QLineEdit()
        self.pu_isbn10 = QLineEdit()
        self.pu_dep_legal = QLineEdit()
        self.pu_design_cover = QLineEdit()
        self.pu_title_original = QLineEdit()
        self.pu_printer = QLineEdit()
        self.pu_weight = QLineEdit()
        self.fix_size(self.pu_weight,80)
        self.pu_print_number = QLineEdit()
        self.fix_size(self.pu_print_number,80)
        self.pu_preface = QLineEdit()
        self.pu_editor = QLineEdit()
        self.pu_copy_number = QLineEdit()
        self.fix_size(self.pu_copy_number,50)
        pu_priceLabel = QLabel('Preço:')
        pu_sourceLabel = QLabel('Origem:')
        self.pu_edition_place = QLineEdit()

        self.pu_source = QLineEdit()
        self.fix_size(self.pu_source,200)
        self.pu_source.setMinimumWidth(200)
        self.pu_price = QLineEdit()
        self.fix_size(self.pu_price,80)
        self.pu_price.setAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.pu_inventory = QLineEdit()
        tab5Layout.addLayout(qc.addHLayout(['Titulo Original:', self.pu_title_original], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Tradução:', self.pu_translator],label_size=120))

        tab5Layout.addLayout(qc.addHLayout(['Prefácio:', self.pu_preface], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Editor(a):', self.pu_editor], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Côr:', self.pu_color], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Desenho:', self.pu_draw], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Desenho da Capa:', self.pu_design_cover], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['ISBN 10:', self.pu_isbn10, 'Dep. Legal',self.pu_dep_legal, True], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Impressor:',self.pu_printer, 'Num. Impressão:',self.pu_print_number], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Peso:', self.pu_weight, True], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Local Edição:',self.pu_edition_place], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Cópia:', self.pu_copy_number, pu_priceLabel, self.pu_price,
                                            pu_sourceLabel, self.pu_source, True], label_size=120))
        tab5Layout.addLayout(qc.addHLayout(['Inventário:', self.pu_inventory], label_size=120))
        pu_classificationLabel = QLabel('<a href="pu_classification" >Classificação:</a>')
        pu_classificationLabel.linkActivated.connect(self.link_click)
        self.pu_classification = QComboBox()
        self.pu_classification.setMaximumWidth(100)
        self.pu_classification.setMinimumWidth(100)
        self.pu_classification.setEditable(True)
        self.pu_classification.setCurrentIndex(-1)
        self.pu_classification.addItems(gl.classifications_list)
        self.pu_classification.setCurrentIndex(-1)

        tab5Layout.addLayout(qc.addHLayout(['Classificação', self.pu_classification, True], label_size=120))

        # self.pu_sinopse = QTextEdit()
        # tab3Layout.addWidget(self.pu_sinopse)
        mainTab5Layout.addLayout(tab5Layout)
        mainTab5Layout.addStretch()

    def make_buttons(self):
        self.btnGrava = QPushButton()
        self.btnGrava.setText('Grava')
        self.btnGrava.clicked.connect(self.record_save)
        self.buttonsLayout.addWidget(self.btnGrava)

        self.btnNovo = QPushButton('Novo')
        self.btnNovo.clicked.connect(self.record_add)
        self.buttonsLayout.addWidget(self.btnNovo)

        self.doubleBtn = QPushButton()
        self.doubleBtn.setText('Duplica')
        self.doubleBtn.clicked.connect(self.double_record_click)
        self.buttonsLayout.addWidget(self.doubleBtn)

        self.editTags = QPushButton()
        self.editTags.setText('Edita Etiquetas')
        self.buttonsLayout.addWidget(self.editTags)
        self.editTags.clicked.connect(self.edit_tags_click)

        # self.specialTagsBtn = QToolButton()
        # self.specialTagsBtn.setText('Caracteristicas')
        # self.buttonsLayout.addWidget(self.specialTagsBtn)
        # self.specialTagsBtn.clicked.connect(self.edit_special_tags_click)
        findFocusAndCapitalize = QToolButton()
        findFocusAndCapitalize.setIcon(QIcon('./img/caps.png'))
        findFocusAndCapitalize.setToolTip('Capitaliza')
        findFocusAndCapitalize.clicked.connect(self.capitalize_focus)
        self.buttonsLayout.addWidget(findFocusAndCapitalize)
        
        addTextToTags = QToolButton()
        addTextToTags.setIcon(QIcon('./img/add_to_tags.png'))
        addTextToTags.setToolTip('Adiciona texto ás etiquetas')
        addTextToTags.clicked.connect(self.add_text_tag_focus)
        self.buttonsLayout.addWidget(addTextToTags)


        if self.navigator > -1 :
            self.forwardBtn = QPushButton()
            self.forwardBtn.setIcon(QIcon('./img/nav_forward.png'))
            self.forwardBtn.clicked.connect(self.forward_click)
            
            self.backwardBtn = QPushButton()
            self.backwardBtn.setIcon(QIcon('./img/nav_backward.png'))
            self.backwardBtn.clicked.connect(self.backward_click)
            
            self.buttonsLayout.addWidget(self.backwardBtn)
            self.buttonsLayout.addWidget(self.forwardBtn)
            self.autoSaveCheck = QCheckBox('Grava Automáticamente')
            self.autoSaveCheck.setCheckState(2)
            self.buttonsLayout.addWidget(self.autoSaveCheck)

        self.btnSai = QPushButton()
        self.btnSai.setText('Sair')
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.btnSai)
        self.btnSai.clicked.connect(self.exit_form)

    def forward_click(self):
        try:
            if self.autoSaveCheck.checkState() == 2:
                self.record_save()
            self.pub_id = gl.NAVIGATOR_INDEX[self.navigator + 1][1]
            self.navigator +=1
            if sqlite_crud.get_book_data(self.pub_id):
                self.refresh_datafields()
        except IndexError:
            pass
    
    def backward_click(self):
        if self.navigator > 0:
            if self.autoSaveCheck.checkState() == 2:
                self.record_save()
            self.pub_id = gl.NAVIGATOR_INDEX[self.navigator - 1][1]
            self.navigator -= 1
            if sqlite_crud.get_book_data(self.pub_id):
                self.refresh_datafields()

    def authors_click(self):
        form = authors.BrowserAuthors()
        form.exec_()
        if form.toto != '':
            self.pu_author_id.setCurrentText(form.toto)

    def languages_click(self):
        form = languages.LanguagesBrowser()
        form.exec_()
        self.pu_language.clear()
        self.pu_language.addItems(gl.languages_list)

    def binding_click(self):
        form = bindings.BindingsBrowser()
        form.exec_()
        self.pu_cover.clear()
        self.pu_cover.addItems(gl.covers_list)

    def status_click(self):
        form = status.StatusBrowser()
        form.exec_()
        self.pu_status.clear()
        self.pu_status.addItems(gl.status_list)

    def conditions_click(self):
        form = conditions.ConditionsBrowser()
        form.exec_()
        self.pu_condition.clear()
        self.pu_condition.addItems(gl.conditions_list)

    def classification_click(self):
        form = classifications.ClassificationsBrowser()
        form.exec_()
        self.pu_classification.clear()
        self.pu_classification.addItems(gl.classifications_list)

    def pub_types_click(self):
        form = pub_types.TypesBrowser()
        form.exec_()
        self.pu_type.clear()
        self.pu_type.addItems(gl.types_list)
    
    def collection_click(self):
        form = colections.CollectionBrowser()
        form.exec_()
        if form.toto != '':
            self.pu_collection.setText(form.toto)
            # self.tags.setHtml('<font color="blue"><strong>' + self.tags.toPlainText() + ',' + form.toto)
    
    def series_click(self):
        form = series.SeriesBrowser()
        form.exec_()
        if form.toto != '':
            self.pu_serie.setText(form.toto)
            # self.tags.setHtml('<font color="blue"><strong>' + self.tags.toPlainText() + ',' + form.toto)
            
    def sources_click(self):
        form = SourceBrowser()
        form.exec_()
        if form.toto != '':
            self.pu_source.setText(form.toto)
            # self.tags.setHtml('<font color="blue"><strong>' + self.tags.toPlainText() + ',' + form.toto)
            
    def publisher_click(self):
        form = PublishersBrowser()
        form.exec_()
        if form.toto != '':
            self.pu_publisher.setText(form.toto)
            # self.tags.setHtml('<font color="blue"><strong>' + self.tags.toPlainText() + ',' + form.toto)
    
    def link_click(self, link ):
        if link == 'pu_local':
            self.set_local_click()
        elif link == 'pu_type':
            self.pub_types_click()
        elif link == 'pu_classification':
            self.classification_click()
        elif link == 'pu_status':
            self.status_click()
        elif link == 'pu_condition':
            self.conditions_click()
        elif link == 'pu_binding':
            self.binding_click()
        elif link == 'pu_language':
            self.languages_click()
        elif link == 'pu_cover':
            self.binding_click()
        elif link == 'pu_author':
            self.authors_click()
        elif link == 'pu_collection':
            self.collection_click()
        elif link == 'pu_serie':
            self.series_click()
        elif link == 'pu_source':
            self.sources_click()
        elif link == 'pu_publisher':
            self.publisher_click()

    
    # def add_from_webbrowser(self,):
    #     self.pu_title.setText(gl.record_current_dict['pu_title'])
    #     self.pu_isbn.setText(gl.record_current_dict['isbn'])
    #     self.pu_sub_title.setText(gl.record_current_dict['pu_sub_title'])
    #     self.pu_author_id.setEditText(gl.record_current_dict['pu_author'])
    #     self.pu_sinopse.setText(self.cleanTags(gl.record_current_dict['pu_sinopse']))
    #     self.pu_edition_date.setText(gl.record_current_dict['pu_edition_date'])
    #     self.pu_publisher.setText(gl.record_current_dict['pu_publisher'] )
    #     self.pu_dimensions.setText(gl.record_current_dict['pu_dimensions'])
    #     self.pu_language.setCurrentText(gl.record_current_dict['pu_language'])
    #     self.pu_cover.setCurrentText(gl.record_current_dict['pu_cover'])
    #     self.pu_type.setCurrentText(gl.LAST_PUB_TYPE)
    #     self.pu_status.setCurrentText(gl.LAST_STATUS)
    #     self.pu_language.setCurrentText(gl.LAST_LANGUAGE)
    #
    #     self.pu_pages.setText(gl.record_current_dict['pu_pages'])
    #     if gl.record_current_dict['pu_year'] == '0':
    #         self.pu_year.setText('0')
            # pass
        # else:
        #     self.pu_year.setText(gl.record_current_dict['pu_year'])
        # self.tags.setHtml('<font color="blue"><strong>' + gl.record_current_dict['pu_tags'])
    
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
        gl.ON_LOCAL = self.pu_local.text().upper().strip()
        gl.LAST_PUB_TYPE = self.pu_type.currentText()
        gl.LAST_STATUS = self.pu_status.currentText()
        # sqlite_crud.save_parameters('LAST_STATUS', gl.LAST_STATUS)
        # sqlite_crud.save_parameters('LAST_PUB_TYPE', gl.LAST_PUB_TYPE)
        # sqlite_crud.save_parameters('LAST_BINDING', gl.LAST_BINDING)
        if self.pub_id == -1:
            # if self.check_required_fields():
            self.insert_record()
            self.toto = True
            self.close()
            # else:
            #     form = missing_data.DadosWizard('\n'.join(self.error_list), ['Corrigir'])
            #     form.exec_()
        else:
            # if self.check_required_fields():
            self.update_record()
            self.toto = True  # refresh
            if self.navigator == -1:
                self.close()
            # else:
            #     result = QMessageBox.information(None,
            #                                      "Faltam os seguintes dados.", '\n'.join(self.error_list),
            #                                      QMessageBox.StandardButtons(QMessageBox.Close), QMessageBox.Close)
    
    def check_required_fields(self):
        self.error_list = []
        if str(self.pu_title.text()) == '':
            self.error_list.append('Falta o titulo.')
        if self.pub_id == -1:
            self.check_ISBN()
        self.check_autor()
        self.check_genere()
        self.check_status()
        self.check_cover()
        self.check_language()
        if not self.error_list:
            return True
        else:
            return False


    def check_update_record(self):
        " APAGA"
        self.error_list = []
        if str(self.pu_title.text()) == '':
            self.error_list.append('Falta o titulo.')
        
        if not self.error_list:
            return True
        else:
            return False
    
    def check_new_record(self):
        " APAGA"
        self.error_list = []
        if self.pu_title.text() == '':
            self.error_list.append('Falta o titulo.')
        self.pu_title.setText(self.pu_title.text().title())
        self.check_autor()
        self.check_genere()
        self.check_ISBN()
        self.check_status()
        self.check_cover()
        if not self.error_list:
            return True
        else:
            return False
    
    def check_ISBN(self):
        """ impede/informa quando há um ISBN duplicado """
        isbn = str(self.pu_isbn.text())
        if isbn != '':
            a = dbmain.query_one('select pu_isbn from books where pu_isbn =?', (isbn,))
            if a is not None:
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
                        sqlite_crud.execute_query('INSERT INTO authors (au_name) VALUES(?); ', (dum,))
                        self.pu_author_id.setEditText(dum)
                        sqlite_crud.get_autores()
                    else:
                        self.error_list.append('Não foi definido o Autor.')
    
    def check_genere(self):
        # types
        dum = self.pu_type.currentText().strip()
        if dum == '':
            self.error_list.append('Não foi definido o Tipo.')
        else:
            if dum.lower() not in gl.types_dict:
                self.error_list.append('Tipo de Publicação errado!')
    
    def check_status(self):
        # editora
        dum = self.pu_status.currentText().strip()
        if dum == '':
            self.error_list.append('Não foi definido o Estado.')
        else:
            if dum not in gl.status_list:
                self.error_list.append('Não foi definido o Estado.')
    
    def check_cover(self):      
        dum = self.pu_cover.currentText().strip()
        if dum == '':
            self.error_list.append('Não foi definida a Encadernação.')
        else:
            if dum in gl.bindings_list:
                pass
            else:
                self.error_list.append('Encadernação enisistente.')
    
    def check_language(self):
        dum = self.pu_language.currentText().strip()
        if dum == '':
            self.error_list.append('Não foi definida o Idioma.')
        else:
            if dum in gl.languages_list:
                pass
            else:
                self.error_list.append('Idioma não definido.')
    
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
        self.doubleBtn.setDisabled(True)
    
    def set_local_click(self):
        form = locals.BrowserLocals()
        form.exec_()
        if not form.toto == '':
            self.pu_local.setText(form.toto)
            gl.ON_LOCAL = form.toto
    
    def paste_local_click(self):
        if gl.ON_LOCAL != '':
            self.pu_local.setText(gl.ON_LOCAL)
    
    def convert_dim_click(self):
        self.pu_dimensions.setText(isbn_lib.dimension_convert(self.pu_dimensions.text()))
    
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

    def capitalize_focus(self):
        bog = self.focusWidget()
        try:
            a = isbn_lib.text_title(bog.text())
            bog.setText(a)
        except AttributeError:
            pass

    def add_text_tag_focus(self):
        bog = self.focusWidget()
        try:
            print('ADD to tags:', bog.text())
            new_tag = bog.text().lower()
            print(gl.record_current_dict['pu_tags'])
            gl.record_current_dict['pu_tags'] += '|' + new_tag
            print(gl.record_current_dict['pu_tags'])
        except AttributeError:
            try:
                print('ADD to tags:', bog.currentText())
                new_tag = bog.currentText().lower()
                print(gl.record_current_dict['pu_tags'])
                gl.record_current_dict['pu_tags'] += '|' + new_tag
                print(gl.record_current_dict['pu_tags'])
            except AttributeError:
                pass

    def publisher_caps(self):
        a = isbn_lib.text_title(self.pu_publisher.text())


    def add_tags_click(self):
        form = tags_manage.BrowserTags()
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
        # dum = self.tags.toPlainText().rstrip(',')
        tags_txt = []
        try:
            tags_txt = gl.record_current_dict['pu_tags'].split('|')
        except AttributeError:
            tags_txt = []
            pass
        form = tag_browser.EditRecordTags(tags_txt)
        form.exec_()
        # print('MAKE tab 4')
        # self.tab4.deleteLater()
        # self.makeTab4()
        # if form.flag:
        #     print('GRAVOU')
        #     print('REFRESH LABELS')


    # def edit_special_tags_click(self):
    #     if self.draft_data:
    #         form = tags_special.EditSpecialTags(0)
    #     else:
    #         form = tags_special.EditSpecialTags(self.pub_id)
    #     form.exec_()
    #     save pub special tags
        # if form.flag:
        #     if self.pub_id > 0:
        #         lib_tags.update_special_tags(self.pub_id, 1)
        #         gl.update_special_tags = False
        # else:
        #     self.tags_special_level1_data = (False,[])

    def previous_record_click(self):
        for n in gl.MAIN_DATASET:
            print(n[0])
    
    def procField(self, aString):
        if aString is None:
            return ''
        else:
            return aString
    
    def init_record(self):
        self.item_data = -1
        self.pu_title.setText('')
        self.pu_sub_title.setText('')
        self.pu_isbn.setText('')
        self.pu_local.setText('')
        self.pu_author_id.setEditText('')
        self.pu_year.clear()
        # self.tags.setText('')
        # self.tags_stack = ''
        self.pu_sinopse.clear()
        self.pu_obs.clear()
        self.pu_language.setCurrentText(gl.LAST_LANGUAGE)
        self.pu_condition.setCurrentIndex(-1)
        self.pu_cover.setCurrentText(gl.LAST_BINDING)
        self.pu_type.setCurrentText(gl.LAST_PUB_TYPE)
        self.pu_status.setCurrentText(gl.LAST_STATUS)

    
    def double_record_click(self):
        self.pub_id = -1
        self.item_data = -1
        self.pu_title.setText('')
        self.pu_sub_title.setText('')
        self.pu_isbn.setText('')
        self.pu_sinopse.clear()
        self.pu_obs.clear()
        # if int(self.pu_volume.text()) > 1:
        #     self.pu_volume.setText(str(int(self.pu_volume.text()) + 1))
        # else:
        #     self.pu_volume.setText('1')
    
    def update_combo_boxes(self):
        sqlite_crud.update_datasets()
        # limpa os campos
        self.pu_author_id.clear()
        self.pu_author_id.addItems(gl.dsAutores)
        self.pu_type.clear()
        self.pu_type.addItems(gl.types_list)
        self.pu_status.clear()
        self.pu_status.addItems(gl.status_list)
        self.pu_type.setCurrentText(gl.STATUS)
        self.pu_type.setCurrentText(gl.TYPE)
    
    def refresh_datafields(self):
        """record on database"""
        self.update_combo_boxes()
        self.pu_title.setText(gl.record_current_dict['pu_title'])
        self.pu_sub_title.setText(gl.record_current_dict['pu_sub_title'])
        self.pu_author_id.setCurrentText(gl.record_current_dict['pu_author'])
        read_record(self.pu_isbn, 'pu_isbn', gl.record_current_dict)
        read_record(self.pu_local, 'pu_local', gl.record_current_dict)
        read_record(self.pu_type, 'pu_type', gl.record_current_dict)
        read_record(self.pu_volume, 'pu_volume', gl.record_current_dict)
        # self.pu_status.setCurrentIndex(gl.record_current_dict['status_id'] - 1)
        read_record(self.pu_obs, 'pu_obs', gl.record_current_dict)
        read_record(self.pu_sinopse, 'pu_sinopse', gl.record_current_dict)
        read_record(self.pu_year, 'pu_year', gl.record_current_dict)
        read_record(self.pu_edition,'pu_edition',gl.record_current_dict)
        read_record(self.pu_volume_collection,'pu_volume_collection',gl.record_current_dict)
        self.pu_publisher.setText(gl.record_current_dict['pu_publisher'])
        read_record(self.pu_pages,'pu_pages',gl.record_current_dict)
        self.pu_dimensions.setText(gl.record_current_dict['pu_dimensions'])
        self.pu_cover.setCurrentText(gl.record_current_dict['pu_cover'])
        self.pu_language.setCurrentText(gl.record_current_dict['pu_language'])
        read_record(self.pu_copy_number,'pu_copy_number',gl.record_current_dict)
        self.pu_edition_date.setText(gl.record_current_dict['pu_edition_date'])
        self.pu_edition_place.setText(gl.record_current_dict['pu_edition_place'])
        self.pu_price.setText(gl.record_current_dict['pu_price'])
        self.pu_source.setText(gl.record_current_dict['pu_source'])
        read_record(self.pu_volume_serie,'pu_volume_serie',gl.record_current_dict)
        self.pu_classification.setCurrentText(gl.record_current_dict['pu_classification'])
        self.pu_condition.setCurrentText(gl.record_current_dict['pu_condition'])
        self.pu_collection.setText(gl.record_current_dict['pu_collection'])
        self.pu_serie.setText(gl.record_current_dict['pu_serie'])
        self.pu_color.setText(gl.record_current_dict['pu_color'])
        self.pu_draw .setText(gl.record_current_dict['pu_draw'])
        self.pu_isbn10.setText(gl.record_current_dict['pu_isbn10'])
        self.pu_dep_legal.setText(gl.record_current_dict['pu_dep_legal'])
        self.pu_design_cover.setText(gl.record_current_dict['pu_design_cover'])
        self.pu_title_original.setText(gl.record_current_dict['pu_title_original'])
        self.pu_printer.setText(gl.record_current_dict['pu_printer'])
        self.pu_weight.setText(gl.record_current_dict['pu_weight'])
        self.pu_print_number.setText(str(gl.record_current_dict['pu_print_number']))
        self.pu_preface.setText(gl.record_current_dict['pu_preface'])
        self.pu_translator.setText(gl.record_current_dict['pu_translator'])
        self.pu_inventory.setText(gl.record_current_dict['pu_inventory'])
        self.pu_editor.setText(gl.record_current_dict['pu_editor'])

        


    def get_tags_from_record(self):
        sql = 'SELECT tags.ta_name FROM tags_reference INNER JOIN public.tags ON (public.tags_reference.tags_ref_tag_id = public.tags.ta_id)\
        where tags_reference.tags_ref_book =? and tags_ref_level =0' # + str(self.pub_id)
        a = dbmain.query_many(sql, (self.pub_id,))
        tags = ''
        for n in a:
            tags += n[0].lower() + ','
        return tags.rstrip(',')
    
    def insert_record(self):
        sql = '''insert into books (
        pu_author, pu_local , pu_type, pu_isbn , pu_obs,
        pu_sinopse, pu_status, pu_title, pu_volume,pu_year, pu_sub_title,
        pu_volume_collection,
        pu_edition,
        pu_publisher,
        pu_pages,
        pu_dimensions,
        pu_cover,
        pu_copy_number,
        pu_edition_date,
        pu_edition_place,
        pu_price,
        pu_source,
        pu_language,
        pu_volume_serie,
        pu_condition,
        pu_classification,
        pu_collection,
        pu_serie,
        pu_color,
        pu_draw ,
        pu_isbn10,
        pu_dep_legal,
        pu_design_cover,
        pu_title_original,
        pu_printer,
        pu_weight,
        pu_print_number,
        pu_preface,pu_translator,
        pu_inventory,
        pu_editor
        )
        VALUES (?,?,?,?
        ,?,?,?,?,?,?,?,?,?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )'''
        data = (stdio.authors_process(self.pu_author_id.currentText()),self.pu_local.text().upper(),)
        data += (self.pu_type.currentText(),self.pu_isbn.text().strip(),)
        data += (self.pu_obs.toPlainText(),)
        data += (self.pu_sinopse.toPlainText(),)
        data += (self.pu_status.currentText(),)
        data += (self.pu_title.text().strip(),)
        data += (self.pu_volume.text(), )
        data += (self.pu_year.text(),)
        data += (self.pu_sub_title.text(),)
        data += (self.pu_volume_collection.text(),)
        data += (self.pu_edition.text(),)
        data += (self.pu_publisher.text(),)
        data += (self.pu_pages.text(),)
        data += (self.pu_dimensions.text(),)
        data += (self.pu_cover.currentText(),)
        data += (self.pu_copy_number.text(),)
        data += (self.pu_edition_date.text(),)
        data += (self.pu_edition_place.text().strip(),)
        data += (self.pu_price.text(),)
        data += (self.pu_source.text(),)
        data += (self.pu_language.currentText(),)
        data += qstring_to_int(self.pu_volume_serie)
        data += (self.pu_condition.currentText(),)
        data += (self.pu_classification.currentText(),)
        data += (self.pu_collection.text(),)
        data += (self.pu_serie.text(),)
        data += (self.pu_color.text(),)
        data += (self.pu_draw.text(),)
        data += (self.pu_isbn10.text(),)
        data += (self.pu_dep_legal.text(),)
        data += (self.pu_design_cover.text(),)
        data += (self.pu_title_original.text(),)
        data += (self.pu_printer.text(),)
        data += (self.pu_weight.text(),)
        data += (self.pu_print_number.text(),)
        data += (self.pu_preface.text(),)
        data += (self.pu_translator.text(),)
        data += (self.pu_inventory.text(),)
        data += (self.pu_editor.text(),)

        sqlite_crud.execute_query(sql, data)
        
        ''' campos especiais '''
        # self.pub_id = dbmain.query_one('select max(pu_id) from books', (True,))[0]
        # gl.last_id = self.pub_id
        ''' actualiza obs'''
        # self.update_tags()
        # gl.TYPE = self.pu_type.currentText()
        # gl.STATUS = self.pu_status.currentText()
        # if self.pub_id > 0:
        #     lib_tags.update_special_tags(self.pub_id, 1)
        #     gl.update_special_tags = False
        # else:
    
    def update_record(self):
        sql = '''UPDATE books SET 
        pu_author=?,
        pu_local =?,
        pu_type=?,
        pu_isbn =?,
        pu_obs=?,
        pu_sinopse=?,
        pu_status==?,
        pu_title=?,
        pu_volume=?,
        pu_year=?,
        pu_sub_title=?,
        pu_edition=?,
        pu_volume_collection=?,
        pu_publisher=?,
        pu_pages=?,
        pu_dimensions=?,
        pu_cover=?,
        pu_copy_number=?,
        pu_edition_date=?,
        pu_edition_place=?,
        pu_price=?,
        pu_source=?,
        pu_language=?,
        pu_volume_serie=?,
        pu_condition=?,
        pu_classification=?,
        pu_collection = ?,
        pu_serie = ?,
        pu_color = ?,
        pu_draw = ?,
        pu_isbn10 = ?,
        pu_dep_legal = ?,
        pu_design_cover = ?,
        pu_title_original = ?,
        pu_printer = ?,
        pu_weight = ?,
        pu_print_number = ?,
        pu_preface = ?,
        pu_translator = ?,
        pu_inventory = ?,
        pu_editor = ?
        WHERE pu_id = ?'''
        data = (self.pu_author_id.currentText(),)
        data += (self.pu_local.text().upper().strip(),)
        data += (self.pu_type.currentText(),)
        data += (self.pu_isbn.text().strip().replace('-', ''),)
        data += (self.pu_obs.toPlainText(),)
        data += (self.pu_sinopse.toPlainText(),)
        data += (self.pu_status.currentText(),)
        data += (self.pu_title.text().strip(),)
        data += qstring_to_int(self.pu_volume)
        data += (write_record(self.pu_year), self.pu_sub_title.text())
        data += (self.pu_edition.text(),)
        data += qstring_to_int(self.pu_volume_collection)
        data += (self.pu_publisher.text(),)
        data += (self.pu_pages.text(),)
        data += (self.pu_dimensions.text(),)
        data += (self.pu_cover.currentText(),)
        data += qstring_to_int(self.pu_copy_number)
        data += (self.pu_edition_date.text(),)
        data += (self.pu_edition_place.text().strip(),)
        data += (self.pu_price.text(),)
        data += (self.pu_source.text(),)
        data += (self.pu_language.currentText(),)
        data += qstring_to_int(self.pu_volume_serie)
        data += (self.pu_condition.currentText(),)
        data += (self.pu_classification.currentText(),)
        data += (self.pu_collection.text(),)
        data += (self.pu_serie.text(),)
        data += (self.pu_color.text(),)
        data += (self.pu_draw.text(),)
        data += (self.pu_isbn10.text(),)
        data += (self.pu_dep_legal.text(),)
        data += (self.pu_design_cover.text(),)
        data += (self.pu_title_original.text(),)
        data += (self.pu_printer.text(),)
        data += (self.pu_weight.text(),)
        data += (self.pu_print_number.text(),)
        data += (self.pu_preface.text(),)
        data += (self.pu_translator.text(),)
        data += (self.pu_inventory.text(),)
        data += (self.pu_editor.text(),)

        data += (self.pub_id,)
        void = sqlite_crud.execute_query(sql, data)
        # self.update_tags()
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
            sqlite_crud.execute_query('delete from tags_reference where tags_ref_book = ? and tags_ref_level=0', (self.pub_id,))
        else:
            sqlite_crud.execute_query('delete from tags_reference where tags_ref_book = ? and tags_ref_level=0', (self.pub_id,))
            sqlite_crud.update_tags(self.pub_id, tags_list)
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

    def fix_size(self, widget_control, size=80, right=True):
        widget_control.setMaximumWidth(size)
        widget_control.setMinimumWidth(size)
        if type(widget_control) == QLineEdit:
            pass
        elif type(widget_control) == QComboBox:
            pass
        else:
            if right:
                widget_control.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

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

def qstring_to_int(qt_object):
    a = type(qt_object)
    if a == QLineEdit:
        try:
            return int(qt_object.text().strip()),
        except ValueError:
            return None,
    elif a == QComboBox:
        try:
            return int(qt_object.currentText().strip()),
        except ValueError:
            return None,

def read_record(obj, field, dic):
    try:
        a = type(obj)
        toto = dic[field]
        if toto is None:
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
            obj.setEditText(str(toto))
        elif a == QDateEdit:
            obj.setDate(toto)
    except Exception as e:
        print('ERRO EM def read_record()')
        print(str(e) + '\n ', obj.objectName(), '\nin field:', field, '\nin dic:', dic)


    
def main():
    pass

if __name__ == '__main__':
    main()
