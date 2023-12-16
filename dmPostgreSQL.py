#!/usr/bin/python
# -*- coding: utf-8 -*-

import parameters as pa
import psycopg2
import psycopg2.extras
import sqlite3
import sys
import datetime
import stdio


def check_alive():
    try:
        conn = psycopg2.connect(pa.conn_string + ' connect_timeout=3')
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
        conn = psycopg2.connect(pa.conn_string)
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
        conn = psycopg2.connect(pa.conn_string)
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
        conn = psycopg2.connect(pa.conn_string)
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
        conn = psycopg2.connect(pa.conn_string)
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
        conn = sqlite3.connect('livros.db')
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

def clone_livros(book_id):
    # clona registo principal
    sql = '''INSERT INTO public.livros (pu_id, pu_title, pu_isbn, pu_cota, pu_obs, pu_tags, pu_volume, pu_type,
            pu_author_id, pu_sub_title, pu_status, pu_sinopse, pu_ed_year, pu_modified) select nextval('livros_livroid_seq'),
            pu_title, pu_isbn, pu_cota, pu_obs, pu_tags, pu_volume, pu_type,
            pu_author_id, pu_sub_title, pu_status, pu_sinopse, pu_ed_year, pu_modified
            FROM livros WHERE pu_id=%s'''
    execute_query(sql,(book_id,))
    new_book_id =  query_one('select max(pu_id) from livros', (True,))[0]
    # clona tags
    sql ='''INSERT INTO public.tags_reference (tags_ref_id, tags_ref_book, tags_ref_tag_id, tags_ref_key, tags_ref_level)
            SELECT nextval('tag_ref_id_seq'), %s, tags_ref_tag_id, tags_ref_key, tags_ref_level
            FROM tags_reference where tags_ref_book=%s'''
    execute_query(sql,(new_book_id, book_id))
    return new_book_id


def find_duplicate(table, field, data):
    data = data.lower()
    try:
        conn = psycopg2.connect(pa.conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        cur.execute('select * from ' + table + ' where ' + field + '=\'' + data + '\'')
        xl = cur.fetchall()
        cur.close()
        conn.close()
        if xl == []:
            return False
        else:
            return True
    
    except Exception as e:
        print('ERRO', str(e))
        return True

if __name__ == '__main__': 
    pass