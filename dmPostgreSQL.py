#!/usr/bin/python
# -*- coding: utf-8 -*-

import parameters as pa
import psycopg2
import psycopg2.extras
import sys
import datetime
import stdio


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

def query_many(sql):
    try:
        conn = psycopg2.connect(pa.conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        #print 'mogrify:', cur.mogrify(sql, data)
        cur.execute(sql)
        xl = cur.fetchall()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        error_print(e,sql,'query_main')
        sys.exit(1)

def error_print(err,sql, caller,data='', to_file=True, d_file=True, show=True):
    if d_file:
        stdio.file_ok('error.txt')
    sql = sql.lower()
    output_string ='-'* 30 +'\n'
    output_string +='     SQL ERROR IN ' + caller + '()\r\n ' + str(err) + '\r\n'
    output_string += '-' * 30 + '\n'
    sql_dump = []
    b = sql.find('from')
    sql_dump.append(sql[:b])
    c = sql.find('where')
    sql_dump.append(sql[b:c])
    sql_dump.append(sql[c:])
    output_string += 'SQL:\n' + '\r\n* '.join(sql_dump) + '\r\n'
    output_string += 'DATA:\n' + str(data) + '\r\n'
    output_string += '-' * 30 + '\n'
    if to_file:
        output_string += '@ ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(output_string, file=open("error.txt", "a"))
    if show:
        print(output_string)
    return output_string
        
if __name__ == '__main__': 
    pass