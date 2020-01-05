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
    a = dbmain.query_many('select ty_id,ty_name from types  ')
    gl.types_dict ={}
    gl.ds_types = []
    for n in a:
        gl.types_dict[n[1].lower()] = n[0]
        gl.ds_types.append(n[1])


def get_autores():
    a = dbmain.query_many('select au_id, au_name from authors order by au_name asc')
    gl.dsAutores = [] #QStringList()
    gl.autores_dict = {}
    for n  in a:
        gl.autores_dict[n[1].lower()] = n[0]
        gl.dsAutores.append(n[1])
               
def get_status():
    a = dbmain.query_many('select st_id,st_nome from status')
    gl.dsStatus = []   
    gl.status_dict = {}
    for n in a:
        gl.status_dict[n[1].lower()] = n[0]
        gl.dsStatus.append(n[1])


def search_data_in_table(table, field, data_to_search):
    sql = 'SELECT * from ' + table + ' where ' + 'lower(' + field +') = \'' + data_to_search.lower() + '\''
    print(sql)
    if dbmain.query_one(sql, (True,)):
        print('existe')
    else:
        print('nao existe')


def get_livro_data(index):
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''SELECT livros.pu_id, livros.pu_title, pu_sub_title, authors.au_name,
        livros.pu_cota,types.ty_name,
        livros.pu_obs,  
        livros.pu_isbn,status.st_nome, pu_sinopse, pu_volume,pu_ed_year,types.ty_id,status.st_id
        FROM livros, authors,types, status
        WHERE livros.pu_id = %s and  
        types.ty_id = livros.pu_type  and
        livros.pu_author_id=authors.au_id AND 
        livros.pu_status = status.st_id;'''
    dict_cur.execute(sql, (index, ))
    rec = dict_cur.fetchone()
    if rec == []: # houve um erro e o registo está limpo.
        return -1
    return rec

def get_modelo_data(index):
    gl.conn_string = "host=" + gl.db_host + " dbname=" + gl.db_database + " user=" + gl.db_user + " password=" + gl.db_password
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    sql = '''SELECT
            livros.pu_id,
            livros.pu_title,
            livros.pu_ed_date,
            livros.pu_volume,
            livros.pu_pages,
            livros.pu_cota,
            livros.pu_obs,
            collection.col_name,
            livros.pu_tags,
            media.me_name,
            types.ty_name,
            livros.pu_volumes,
            publishers.pb_name,
            media_formats.mf_name,
            livros.pu_ed_year,
            livros.pu_sinopse
            FROM
            public.livros,
            media,
            types,
            collection,
            publishers,
            media_formats
            where livros.pu_id=%s and
            livros.pu_media = media.me_id and
            livros.pu_type = types.ty_id and
            livros.pu_collection = collection.col_id and
            livros.pu_editor_id = publishers.pb_id and
            livros.pu_media_format = media_formats.mf_id'''
    dict_cur.execute(sql, (index, ))
    rec = dict_cur.fetchone()
    if rec == []: # houve um erro e o registo está limpo.
        return -1
    return rec

def get_bd_data(index):
    # gl.conn_string = "host=" + gl.db_host + " dbname=" + gl.db_database + " user=" + gl.db_user + " password=" + gl.db_password
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name,
        livros.pu_cota,assuntos.as_nome,media.me_name,types.ty_name,livros.pu_media_format,livros.pu_translator,
        livros.pu_obs,livros.pu_author_others,livros.pu_volume,livros.pu_pages,livros.pu_sub_title,
        livros.pu_title_original,collection.col_name,livros.pu_type,
        media_formats.mf_name, publishers.pb_name, livros.pu_isbn, livros.pu_isbn10, livros.pu_deplegal,
        livros.pu_ed_date, livros.pu_ed_local,livros.pu_volumes, 
        pu_edition_number, series.se_nome, status.st_nome, livros.pu_estado_fisico, languages.lg_short,pu_sinopse, pu_ed_year, 
        hero.he_nome
        FROM livros, media, media_formats, authors,
        types, assuntos, collection, publishers, status, languages,series, hero
        WHERE livros.pu_id = %s and media.me_id = livros.pu_media AND 
        collection.col_id= livros.pu_collection and 
        types.ty_name = livros.pu_type AND assuntos.as_id = livros.pu_subject AND
        livros.pu_media_format=media_formats.mf_id AND livros.pu_serie = series.se_id AND 
        livros.pu_author_id=authors.au_id AND publishers.pb_id = livros.pu_editor_id AND 
        livros.pu_status = status.st_id AND livros.pu_language=languages.lg_id AND
        livros.pu_bd_hero = hero.he_id;'''
    dict_cur.execute(sql, (index, ))

    rec = dict_cur.fetchone()
    if rec == []: # houve um erro e o registo está limpo.
        return -1
    conn.close()
    return rec

def update_tags_list(tag_list):
    for n in tag_list:
        toto = n.lower().strip()
        if toto != '':
            a = dbmain.OutputQueryOne('select ta_id from tags where ta_name = %s', (toto, ))
            if a.output == None:
                dbmain.execute_query('insert into tags (ta_name) values(%s)', (toto, ))
               
            
def get_tags_index(tag_list):
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
    # print tag_max
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
    # print 'tags.id',tags_id
    sql = ''' INSERT INTO tag_ref (tr_book, tr_tag) VALUES''' + str(tags_id)[1:-1]
    dbmain.execute_query(sql, (True, ))


def get_record(uuid):
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''select * from livros where pu_id = %s'''
    dict_cur.execute(sql, (uuid, ))
    rec = dict_cur.fetchone()
    conn.close()
    return rec

def load_preps():
    a = dbmain.query_many('select prep_word from prep')
    gl.prep_dict = {}
    for n in a:
        gl.prep_dict[n[0].lower()]=n[0]
    
def load_parameters():
    a = dbmain.query_one('select param_json from params where param_key=%s', ('FORM',))[0]
    gl.forms = json.loads(a)

def get_params():
    a = dbmain.query_many('select * from params')
    for n in a:
        if n[0] == 'LAST_TAGS':
            dum = n[1].split(',')
            for f in dum:
                gl.last_tags.append((0, f))
        elif n[0] == 'SHOW_RECORDS':
            gl.SHOW_RECORDS = n[1]
        elif n[0] == 'OWNER':
            gl.OWNER = n[1]
    
def save_param(k_name, k_data):
    dbmain.execute_query('update params set param_data=%s where param_key=%s', (k_data,k_name))
    

def get_areas():
    a = dbmain.query_many('''select distinct pu_cota from livros WHERE pu_cota IS NOT NULL and pu_cota  <>'' order by pu_cota''')
    gl.ds_areas = []
    for n in a:
        gl.ds_areas.append(n[0])
    

    
if __name__ == "__main__":
    pass
    # settings.load_settings()
    # pprint.pprint(get_modelo_data(2144))
