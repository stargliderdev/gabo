#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import json

import parameters as gl
import dmPostgreSQL as dbmain

def addRecord2Table(table, field, value, type_field):
    value = str(value)
    dbmain.execute_query('insert into ' + table + ' ( ' + field + ',' + type_field +') values(%s); ', (value,))


def get_types():
    a = dbmain.query_many('select ty_name, ty_order from types order by ty_order  ')
    gl.types_dict ={}
    gl.types_list = []
    gl.types_tuple = []
    gl.TYPES_FILTER_LIST = ['Todos']
    for n in a:
        gl.types_dict[n[0].lower()] = n[0]
        gl.types_list.append(n[0])
        gl.TYPES_FILTER_LIST.append(n[0])
        gl.types_tuple.append(n)


def get_autores():
    a = dbmain.query_many('select au_id, au_name from authors order by au_name asc')
    gl.dsAutores = []
    gl.autores_dict = {}
    for n in a:
        gl.autores_dict[n[1].lower()] = n[0]
        gl.dsAutores.append(n[1])
               
def get_status():
    a = dbmain.query_many('select status_name,status_order from status')
    gl.status_list = []
    gl.STATUS_FILTER_LIST = ['Todos']
    gl.status_tuple = []
    for n in a:
        gl.status_list.append(n[0])
        gl.status_tuple.append(n)
        gl.STATUS_FILTER_LIST.append(n[0])
        
def get_locals():
    a = dbmain.query_many('select lc_id,lc_name from locals')
    gl.locals_list = []
    gl.locals_dict = {}
    for n in a:
        gl.locals_list.append(n[1])

def get_conditions():
    a = dbmain.query_many('select condition_name, condition_order from conditions order by condition_order')
    gl.conditions_list = []
    gl.conditions_dict = {}
    gl.conditions_tuple = []
    for n in a:
        gl.conditions_list.append(n[0])
        gl.conditions_tuple.append(n)
 
def get_sources():
    a = dbmain.query_many('select  pu_source from livros where pu_source is not null  group by pu_source order by pu_source')
    gl.sources_tuple = []
    for n in a:
        gl.sources_tuple.append(n)
 
def get_publishers():
    a = dbmain.query_many('select  pu_publisher from livros where pu_publisher is not null  group by pu_publisher order by pu_publisher')
    gl.publishers_tuple = []
    for n in a:
        gl.publishers_tuple.append(n)

def get_collections():
    a = dbmain.query_many('select  pu_collection from livros where pu_collection is not null  group by pu_collection order by pu_collection')
    gl.collections_tuple = []
    for n in a:
        gl.collections_tuple.append(n)
    
def get_series():
    a = dbmain.query_many('select  pu_series_name from livros where pu_series_name is not null  group by pu_series_name order by pu_series_name')
    gl.series_tuple = []
    for n in a:
        gl.series_tuple.append(n)
        
def get_classifications():
    a = dbmain.query_many('select classification_name, classification_order from classifications order by classification_order')
    gl.classifications_list = []
    gl.classifications_dict = {}
    gl.classifications_tuple = []
    for n in a:
        gl.classifications_list.append(n[0])
        gl.classifications_tuple.append(n)

def get_languages():
    a = dbmain.query_many('select language_name, language_order from languages order by language_order')
    gl.languages_list = []
    gl.languages_dict = {}
    gl.languages_tuple = []
    for n in a:
        gl.languages_list.append(n[0])
        gl.languages_tuple.append(n)

def get_bindings():
    a = dbmain.query_many('select binding_name,binding_order from bindings order by binding_order')
    gl.bindings_list = []
    gl.bindings_dict = {}
    gl.bindings_tuple = []
    for n in a:
        gl.bindings_list.append(n[0])
        gl.bindings_tuple.append(n)

def search_data_in_table(table, field, data_to_search):
    # abondonado
    sql = 'SELECT * from ' + table + ' where ' + 'lower(' + field +') = \'' + data_to_search.lower() + '\''
    if dbmain.query_one(sql, (True,)):
        print('existe')
    else:
        print('nao existe')


def get_book_data(index):
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''SELECT *
        FROM livros, authors,types, status
        WHERE livros.pu_id = %s and  
        types.ty_id = livros.pu_type  and
        livros.pu_author_id=authors.au_id AND 
        livros.pu_status = status.status_id;'''
    dict_cur.execute(sql, (index, ))
    gl.record_current_dict = dict_cur.fetchone()
    dict_cur.close()
    conn.close()
    if not gl.record_current_dict: # houve um erro e o registo está limpo.
        return False
    else:
        # load level 1
        gl.TAGS_SPECIAL_LEVEL1_DATA = dbmain.query_many('''select tag_key,ta_name,tags_special_name
                                            from tags_reference
                                            inner join tags on tags_reference.tags_ref_tag_id=tags.ta_id
                                            inner join tags_special on tags.tag_key=tags_special.tags_special_key
                                            where tags_ref_book=%s and  tag_key is not null and tags_special.tags_special_level=1
                                            order by tags_special.tags_special_order''', (index,))
        return True



# def OLD_get_bd_data(index):
#     abondonado
#     gl.conn_string = "host=" + gl.db_host + " dbname=" + gl.db_database + " user=" + gl.db_user + " password=" + gl.db_password
#     get a connection, if a connect cannot be made an exception will be raised here
    # conn = psycopg2.connect(gl.conn_string)
    # dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name,
    #     livros.pu_cota,assuntos.as_nome,media.me_name,types.ty_name,livros.pu_media_format,livros.pu_translator,
    #     livros.pu_obs,livros.pu_author_others,livros.pu_volume,livros.pu_pages,livros.pu_sub_title,
    #     livros.pu_title_original,collection.col_name,livros.pu_type,
    #     media_formats.mf_name, publishers.pb_name, livros.pu_isbn, livros.pu_isbn10, livros.pu_deplegal,
    #     livros.pu_ed_date, livros.pu_ed_local,livros.pu_volumes,
    #     pu_edition_number, series.se_nome, status.st_nome, livros.pu_estado_fisico, languages.lg_short,pu_sinopse, pu_ed_year,
    #     hero.he_nome
    #     FROM livros, media, media_formats, authors,
    #     types, assuntos, collection, publishers, status, languages,series, hero
    #     WHERE livros.pu_id = %s and media.me_id = livros.pu_media AND
    #     collection.col_id= livros.pu_collection and
    #     types.ty_name = livros.pu_type AND assuntos.as_id = livros.pu_subject AND
    #     livros.pu_media_format=media_formats.mf_id AND livros.pu_serie = series.se_id AND
    #     livros.pu_author_id=authors.au_id AND publishers.pb_id = livros.pu_editor_id AND
    #     livros.pu_status = status.status_id AND livros.pu_language=languages.lg_id AND
    #     livros.pu_bd_hero = hero.he_id;'''
    # dict_cur.execute(sql, (index, ))
    #
    # rec = dict_cur.fetchone()
    # if rec == []: # houve um erro e o registo está limpo.
    #     return -1
    # conn.close()
    # return rec
    #
def update_tags_list(tag_list):
    for n in tag_list:
        toto = n.lower().strip()
        if toto != '':
            a = dbmain.OutputQueryOne('select ta_id from tags where ta_name = %s', (toto, ))
            if a.output == None:
                dbmain.execute_query('insert into tags (ta_name) values(%s)', (toto, ))
               
            
def get_tags_index(tag_list):
    # abondonado
    xe = []
    for n in tag_list:
        a = dbmain.OutputQueryOne('select ta_id from tags where ta_name = %s', (n.lower().strip(), ))
        xe.append(a.output[0])
    return xe

def update_tags(pub_id,tag_list):
    # id = livro
    tags_id = []
    tag_max = dbmain.query_one('''Select max(ta_id)+1 as t from tags''', (True,))[0]
    if tag_max == None:
        tag_max = 1
    for n in tag_list:
        toto = n.lower().strip()
        if toto != '':
            a = dbmain.query_one('select ta_id from tags where ta_name = %s', (toto,))
            if a == None: # é nova
                dbmain.execute_query('insert into tags (ta_name) values(%s)', (toto, ))
                tags_id.append((pub_id,tag_max))
                tag_max +=1
            else:
                tags_id.append((pub_id,a[0]))
    sql = ''' INSERT INTO tags_reference(tags_ref_book, tags_ref_tag_id) VALUES''' + str(tags_id)[1:-1]
    dbmain.execute_query(sql, (True, ))


def get_record(uuid):
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''select * from livros where pu_id = %s'''
    dict_cur.execute(sql, (uuid, ))
    rec = dict_cur.fetchone()
    conn.close()
    return rec

def load_prepositions():
    a = dbmain.query_many('select prep_word from prep')
    gl.prep_dict = {}
    for n in a:
        gl.prep_dict[n[0].lower()]=n[0]
    
def old_load_parameters():
    """ abandonado"""
    a = dbmain.query_one('select param_json from params where param_key=%s', ('FORM',))[0]
    gl.forms = json.loads(a)

def load_parameters():
    a = dbmain.query_many('select * from params')
    for n in a:
        if n[0] == 'LAST_TAGS':
            toto = n[1].rstrip(',')
            dum = toto.split(',')
            for f in dum:
                gl.last_tags.append(f)
            gl.last_tags = gl.last_tags[: len(gl.last_tags) - (len(gl.last_tags) - 10)]
        elif n[0] == 'SHOW_RECORDS':
            gl.SHOW_RECORDS = n[1]
        elif n[0] == 'OWNER':
            gl.OWNER = n[1]
        elif n[0] == 'LAST_STATUS':
            gl.LAST_STATUS = n[1]
        elif n[0] == 'LAST_BINDING':
            gl.LAST_BINDING = n[1]
        elif n[0] == 'LAST_LANGUAGE':
            gl.LAST_LANGUAGE = n[1]
        elif n[0] == 'LAST_PUB_TYPE':
            gl.LAST_PUB_TYPE = n[1]
        elif n[0] == 'GRID_COLUMN_SIZES':
            gl.GRID_COLUMN_SIZES = eval(n[1])

def save_parameters(k_name, k_data):
    dbmain.execute_query('update params set param_data=%s where param_key=%s', (k_data,k_name))
    
def save_last_tags_params():
    """input gl.LAST_TAGS"""
    last_tags_string = ','.join(gl.last_tags)
    dbmain.execute_query('update params set param_data=%s where param_key=%s', (last_tags_string,'LAST_TAGS'))

def get_areas():
    a = dbmain.query_many('''select distinct pu_cota from livros WHERE pu_cota IS NOT NULL and pu_cota  <>'' order by pu_cota''')
    gl.ds_areas = []
    for n in a:
        gl.ds_areas.append(n[0])
    
def get_special_tags(level=1):
    a = dbmain.query_many('''SELECT tags_special_name, tags_special_key, tags_special_order
    FROM tags_special
    WHERE tags_special_level=%s
    ORDER BY tags_special_order''', (level,))
    gl.tag_special_list = []
    for n in a:
        gl.tag_special_list.append((n[0], n[1], n[2]))
        gl.tag_special_dict[n[1].upper()] = n[0]
   
    
if __name__ == "__main__":
    pass
