#!/usr/bin/python
# -*- coding: utf-8 -*-
ISBN = ''
book_data_dict = {}
autores_dict = {}
editoras_dict = {}
media_formats_dict = {}
media_dict = {}
last_id = 0
db_params = {}
RECORDS_IN_DATASET = 0
last_tags = []
SHOW_RECORDS = '80'
ON_LOCAL = ''
ISBN_SEARCH_SITE = 0
TYPE = 'Romance'
STATUS = 'Na colecção'
AUTHOR_SEARCH_MASK = ''
VERSION = '20231130'
OWNER = ''
prep_set = set()
WORDS_DICT = {}
tag_special_list = []
tag_special_dict = {}
locals_list = []
CURRENT_SQL = ''
FIELDS_ORDER_DIC = {'todos': 'pu_id', 'autor': 'pu_author', 'titulo': 'pu_title',
                    'isbn': 'pu_isbn', 'local': 'pu_local',
                    'tipo': ' pu_type ',
                    'volume': 'pu_volume', 'ano': 'pu_year, pu_volume ', 'estado': 'pu_status',
                    'num': 'pu_id', 'tomo': 'pu_volume',
                    'vol. série': 'pu_volume_serie', 'vol. colec.': 'pu_volume_collection'}
types_dic = {'todos': ''}
"""where was last search 1:author, 2:local"""
LAST_SEARCH_WHERE: int = 1
MAIN_DATASET = []
SEARCH_DICT = {'WHERE': '', 'ORDER': '', 'ORDER_BY': '', 'LAST': 0, 'STATUS': '', 'TYPE': ''}
# main vars
record_current_dict = {}
TAGS_SPECIAL_LEVEL1_DATA = []  # KEY, value, description
TAGS_NORMAL_DATA = []

year_as_date = True
add_author_as_label = True
check_in_database = True
capitalize_title = True
title_in_upper = False
author_surname = False
author_surname_title = False
smart_title = False
add_isbn = True
update_special_tags = False
LAST_TAG = ''
NAVIGATOR_INDEX = []
CURRENT_LOCAL = None
TYPES_FILTER_LIST = []
languages_list = []
languages_dict = {}
languages_tuple = []
classifications_list = []
classifications_dict = {}
classifications_tuple = []
conditions_list = []
types_dict = {}
types_list = []
types_tuple = []
TYPES_FILTER = []
status_list = []
STATUS_FILTER_LIST = []
status_tuples = []
combox_list = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
LAST_STATUS = ''
LAST_BINDING = ''
LAST_LANGUAGE = ''
LAST_PUB_TYPE = ''
GRID_COLUMN_SIZES = ''
GRID_COL_NAMES = ['Num', 'Titulo', 'Autor', 'Tipo', 'Estado', 'Local', 'Tomo', 'Ano', 'Edição', 'Vol. Série',
                  'Vol. Colec.', 'Preço', 'Cópia']
GRID_COL_NAMES_ORG = GRID_COL_NAMES[:]
COLUMN_SORT = (0, 0)
conn_string = ''
sources_tuple = []
collections_tuple = []
DB_PATH = ''
DB_FILE = ''
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
RUN_FROM = ''
DOCUMENTS_DIR = ''
DB_VERSION = -1
BIN_VERSION = -1
STACK_DB_PATH = ''
STACK_DB_NAME = ''
