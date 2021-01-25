#!/usr/bin/python
# -*- coding: utf-8 -*-
ISBN = ''
book_data_dict = {}
autores_dict = {}
editoras_dict = {}
media_formats_dict = {}
media_dict = {}
last_id=0
db_params = (False,[])
records_in_ds = 0
last_tags = []
SHOW_RECORDS = '80'
ON_LOCAL = ''
ISBN_SEARCH_SITE = 0
TYPE = 'Romance'
STATUS = 'Na colecção'
AUTHOR_SEARCH_MASK = ''
VERSION = '28-11-2020'
OWNER = ''
prep_set = set()
prep_dict = {}
tag_special_list = []
tag_special_dict = {}
locals_list = []
CURRENT_SQL = ''
sort_dic = {'nada': 'livros.pu_id', 'autor': 'authors.au_name', 'titulo': 'livros.pu_title',
               'isbn': 'livros.pu_isbn', 'local': 'livros.pu_cota',
               'tipos': ' livros.pu_type ',
               'volume': 'livros.pu_volume', 'ano': 'livros.pu_ed_year, livros.pu_volume '}
types_dic = {'todos': ''}
"""where was last search 1:author, 2:local"""
LAST_SEARCH_WHERE:int = 1
FILTER_DATASET = []
SEARCH_DICT = {}

