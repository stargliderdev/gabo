#!/usr/bin/python
# -*- coding: utf-8 -*-
import database_init
import parameters as pa
import psycopg2
import psycopg2.extras
import sqlite3
import sys
import datetime

import settings
import sqlite_crud
import stdio
import parameters as gl

conn_string = "host=192.168.5.99 dbname=renato user=root password=masterkey"

def check_alive():
    try:
        conn = psycopg2.connect(conn_string + ' connect_timeout=3')
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        cur.mogrify('Select * from params')
        cur.close()
        conn.close()
        return True,
    except psycopg2.DatabaseError:
        return False

def execute_query(sql, data):
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        error_print(e, sql, 'execute_query', data)
        sys.exit(1)

def query_one(sql, data):
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        cur.execute(sql, data)
        xl = cur.fetchone()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        error_print(e, sql,'query_one',data)
        sys.exit(1)


def query_one_simple(sql):
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute(sql)
        xl = cur.fetchone()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        error_print(e, sql, 'query_one_simple')
        sys.exit(1)

def query_many(sql, data = None):
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        if data is None:
            cur.execute(sql)
        else:
            cur.execute(sql,data)
        xl = cur.fetchall()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        error_print(e,sql,'query_main')
        sys.exit(1)


def query_many_sqlite(sql, data=None):
    # print('-> ' + sql.upper())
    xl = []
    try:
        conn = sqlite3.connect('livros.db', uri=True)
        if data is None:
            cur = conn.execute(sql)
            for n in cur:
                xl.append(n)
        else:
            cur = conn.execute(sql, data)
        conn.close()
    except Exception as e:
        print(e, '\n sql-> ' + sql, '\n IN \n *** query_main ***')
        print('exit')
        exit()
    return xl


def error_print(err,sql, caller,data='', to_file=True, d_file=True, show=True):
    if d_file:
        stdio.file_ok('error.txt')
    sql = sql.lower()
    output_string ='-' * 30 +'\n'
    output_string +='     SQL ERROR IN ' + caller + '()\r\n ' + str(err) + '\r\n'
    output_string += '-' * 30 + '\n'
    sql_dump = []
    b = sql.find('from')
    sql_dump.append(sql[:b])
    c = sql.find('where')
    sql_dump.append(sql[b:c])
    sql_dump.append(sql[c:])
    output_string += 'SQL:\n' + '\r\n '.join(sql_dump) + '\r\n'
    output_string += 'DATA:\n' + str(data) + '\r\n'
    output_string += '-' * 30 + '\n'
    if to_file:
        output_string += '@ ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        # print(output_string, file=open("error.txt", "a"))
    if show:
        print(output_string)
    return output_string

def main_old_table():
    sql = '''SELECT
    pu_id,
            pu_title             ,
            pu_isbn              ,
            pu_cota as pu_local             ,
            pu_obs               ,
            pu_tags              ,
            '1' as pu_volume            ,
            types.ty_name as pu_type        ,
            authors.au_name as pu_author      ,
            pu_sub_title         ,
            status.st_nome as pu_status  ,
            pu_sinopse           ,
            pu_ed_year as pu_year              ,
            pu_modified          ,
            '' as pu_local_new         ,
            '' as pu_volume_collection ,
            '' as pu_copy_number       ,
            '' as pu_edition_date      ,
            '' as pu_edition_place     ,
            '' as pu_price             ,
            '' as pu_source            ,
            'Português' as pu_language          ,
            '' as pu_edition           ,
            'Novo' as pu_condition         ,
            '' as pu_volume_series     ,
            '' as pu_classification    ,
            '' as pu_publisher         ,
            '' as pu_pages             ,
            '' as pu_dimensions        ,
            '' as pu_cover             ,
            '' as pu_collection        ,
            '' as pu_series_name       ,
            '' as pu_translator  ,
            '' as pu_color             ,
            '' as pu_draw              ,
            '' as pu_isbn10            ,
            '' as pu_dep_legal         ,
            '' as pu_design_cover      ,
            '' as pu_title_original    ,
            '' as pu_printer           ,
            '' as pu_weight            ,
            '' as pu_print_number      ,
            '' as pu_preface           ,
            '' as pu_inventory

               from livros
               inner join authors on au_id=pu_author_id
               inner join types on ty_id=livros.pu_type
               inner join status on st_id=pu_status
               order by pu_id'''

    print('Working...')
    # for n in query_many(sql):
    #     print(n)
    # sys.exit(0)
    for n in query_many(sql):
        # print(n[0], n[1])
        sqlite_crud.execute_query('''insert into books (
        pu_id,
        pu_title             ,
        pu_isbn              ,
        pu_local             ,
        pu_obs               ,
        pu_tags              ,
        pu_volume            ,
        pu_type              ,
        pu_author            ,
        pu_sub_title         ,
        pu_status            ,
        pu_sinopse           ,
        pu_year              ,
        pu_modified          ,
        pu_local_new         ,
        pu_volume_collection ,
        pu_copy_number       ,
        pu_edition_date      ,
        pu_edition_place     ,
        pu_price             ,
        pu_source            ,
        pu_language          ,
        pu_edition           ,
        pu_condition         ,
        pu_volume_serie     ,
        pu_classification    ,
        pu_publisher         ,
        pu_pages             ,
        pu_dimensions        ,
        pu_cover             ,
        pu_collection        ,
        pu_serie       ,
        pu_translator        ,
        pu_color             ,
        pu_draw              ,
        pu_isbn10            ,
        pu_dep_legal         ,
        pu_design_cover      ,
        pu_title_original    ,
        pu_printer           ,
        pu_weight            ,
        pu_print_number      ,
        pu_preface           ,
        pu_inventory         
            )
            VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
            )''', n)
        insert_tags_old(n[0])



    print('Done')

def insert_tags_old(pu_id):
    sql = '''select tags_ref_book, ta_name, tag_key 
        from tags 
            inner join tags_reference on ta_id= tags_ref_tag_id
            where tags_ref_book = %s  
            order by tags_ref_book'''
    tags_txt = ''
    for n in query_many(sql, (pu_id,)):
        # tags_txt = tags_txt + '|' + n[1]
        if n[2] is None:
            dot = n[1].find(':')
            # print(n)
            # print('    ', dot)
            if dot == -1:
                # print()
                # print('TAG NORMAL:', n[1])
                # print()
                sqlite_crud.execute_query('insert into tags_reference (tags_ref_book, tags_ref_key) values (?,?)',(pu_id,n[1]))
                tags_txt = tags_txt + '|' + n[1]
            else:
                list_tag=n[1].split(':')
                # print('{:>10}'.format('FIELD:'), n[1])

                if list_tag[0] =='edt':
                    # print('           -»', 'pu_publisher', '=' , list_tag[1])
                    field_name = 'pu_publisher'
                elif list_tag[0] =='ed org':
                    # print('           -»', 'pu_year', '=' , list_tag[1])
                    field_name = 'pu_year'
                elif list_tag[0] =='local':
                    # print('           -»', 'pu_edition_place', '=' , list_tag[1])
                    field_name = 'pu_edition_place'
                sqlite_crud.execute_query('update books set ' + field_name + '=? where pu_id=?', ( list_tag[1].capitalize(), pu_id) )
        else:
            # print('TAG ESPECIAL', n[1], n[2])
            if n[2] =='COVER':
                    field_name = 'pu_cover'
            elif n[2] =='TRAD':
                    tags_txt = tags_txt + '|' + n[1]
                    field_name = 'pu_translator'
            elif n[2] =='DIM':
                    field_name = 'pu_dimensions'
            elif n[2] =='DATA':
                    field_name = 'pu_edition_date'
            elif n[2] =='COL':
                    tags_txt = tags_txt + '|' + n[1]
                    field_name = 'pu_collection'
            elif n[2] =='LANG':
                    field_name = 'pu_languages'
            elif n[2] =='PAG':
                    field_name = 'pu_pages'
            elif n[2] =='ED':
                    field_name = 'pu_publisher'
            elif n[2] =='ISBN13':
                    field_name = 'pu_isbn'
            if n[2] == 'IM':
                pass
            else:
                sqlite_crud.execute_query('update books set ' + field_name + '=? where pu_id=?', (n[1].capitalize(), pu_id) )


    tags_txt = tags_txt.replace('||','|')  #retirado e sublitiuido por |
    tags_txt = tags_txt.rstrip('|')
    tags_txt = tags_txt.lstrip('|')
    sqlite_crud.execute_query('''update books set pu_tags=? where pu_id=?''', (tags_txt, pu_id))
    sqlite_crud.execute_query('''update books set pu_collection =\'Colecção Mil Folhas\' where pu_obs like '%Mil folhas%';''')

def main_table():
    sql = '''SELECT  
    pu_id,
            pu_title             ,
            pu_isbn              ,
            pu_cota as pu_local             ,
            pu_obs               ,
            pu_tags              ,
            pu_volume            ,
            types.ty_name as pu_type        ,
            authors.au_name as pu_author      ,
            pu_sub_title         ,
            status.status_name as pu_status  ,
            pu_sinopse           ,
            pu_ed_year as pu_year              ,
            pu_modified          ,
            '' as pu_local_new         ,
            pu_volume_collection ,
            pu_copy_number       ,
            pu_edition_date      ,
            pu_ed_place as pu_edition_place     ,
            pu_price             ,
            pu_source            ,
            pu_language          ,
            pu_edition           ,
            pu_condition         ,
            pu_volume_series     ,
            pu_classification    ,
            pu_publisher         ,
            pu_pages             ,
            pu_dimensions        ,
            pu_cover             ,
            pu_collection        ,
            pu_series_name       ,
            '' as pu_translator  ,
            '' as pu_color             ,
            '' as pu_draw              ,
            '' as pu_isbn10            ,
            '' as pu_dep_legal         ,
            '' as pu_design_cover      ,
            '' as pu_title_original    ,
            '' as pu_printer           ,
            '' as pu_weight            ,
            '' as pu_print_number      ,
            '' as pu_preface           ,
            '' as pu_inventory    
                                
               from livros
               inner join authors on au_id=pu_author_id
               inner join types on ty_id=livros.pu_type
               inner join status on status_id=pu_status
               order by pu_id'''

    print('Working...')
    for n in query_many(sql):
        print(n)
    sys.exit(0)
    for n in query_many(sql):
        # print(n[0], n[1])
        sqlite_crud.execute_query('''insert into books (
        pu_id,
        pu_title             ,
        pu_isbn              ,
        pu_local             ,
        pu_obs               ,
        pu_tags              ,
        pu_volume            ,
        pu_type              ,
        pu_author            ,
        pu_sub_title         ,
        pu_status            ,
        pu_sinopse           ,
        pu_year              ,
        pu_modified          ,
        pu_local_new         ,
        pu_volume_collection ,
        pu_copy_number       ,
        pu_edition_date      ,
        pu_edition_place     ,
        pu_price             ,
        pu_source            ,
        pu_language          ,
        pu_edition           ,
        pu_condition         ,
        pu_volume_serie     ,
        pu_classification    ,
        pu_publisher         ,
        pu_pages             ,
        pu_dimensions        ,
        pu_cover             ,
        pu_collection        ,
        pu_serie       ,
        pu_translator        ,
        pu_color             ,
        pu_draw              ,
        pu_isbn10            ,
        pu_dep_legal         ,
        pu_design_cover      ,
        pu_title_original    ,
        pu_printer           ,
        pu_weight            ,
        pu_print_number      ,
        pu_preface           ,
        pu_inventory         
            )
            VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
            )''', n)
        insert_tags(n[0])

    print('Done')


def insert_tags(pu_id):
    sql = '''select tags_ref_book, ta_name, tag_key 
        from tags 
            inner join tags_reference on ta_id= tags_ref_tag_id
            where tags_ref_book = %s    and tag_key is null
            order by tags_ref_book'''
    tags_txt = ''
    for n in query_many(sql, (pu_id,)):
        tags_txt = tags_txt + '|' + n[1]
        sqlite_crud.execute_query('insert into tags_reference (tags_ref_book, tags_ref_key) values (?,?)',(pu_id,n[1]))
    tags_txt = tags_txt.replace('||','|') #retirado e sublitiuido por |
    tags_txt = tags_txt.rstrip('|')
    tags_txt = tags_txt.lstrip('|')
    sqlite_crud.execute_query('''update books set pu_tags=? where pu_id=?''', (tags_txt, pu_id))
    # print(tags_txt)


# insert_tags(1835)

database_init.create_database()
settings.load_settings()
gl.DB_VERSION = 0
database_init.updater()
main_old_table()
# insert_tags_old(3)
