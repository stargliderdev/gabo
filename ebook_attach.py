#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import base64
import os

import psycopg2.extras

import parameters as pa
import dmPostgreSQL as dbmain

def attach_file(encoded_file, pub_id, info):
    dbmain.execute_query('delete from edoc_data where edoc_pub_id= %s',(pub_id,))
    conn = psycopg2.connect(pa.conn_string)    
    curs = conn.cursor()
    curs.execute("INSERT into edoc_data (edoc_pub_id, edoc_data, edoc_size, edoc_file_name,edoc_file_format) values (%s,%s,%s,%s,%s)",
     (pub_id, psycopg2.Binary(encoded_file),info['file_size'],info['file_name'],info['ext'].upper()))
    conn.commit()
    curs.close()
    conn.close()


def attachment_info(file_path):
    if os.path.exists(file_path):
        ext = file_path[file_path.rfind('.') +1 :]
        file_name = file_path[file_path.rfind('/') +1 :]
        file_name = file_name[: file_name.rfind('.')]
        return {'ext':ext,'file_name':file_name, 'file_size':0}
    else:
        print('file not found')
        return {'ext':'','file_name':'', 'file_size': -1}


def attachment_add(file_path, pub_id):
    c= {}
    if os.path.exists(file_path):
        f = open(file_path, 'rb')  #.read()
        binary = f.read()
        c = attachment_info(file_path)
        c['file_size'] = len(binary)
        encoded_var = base64.b64encode(binary)
        attach_file(encoded_var, pub_id, c)
        # dbmain.execute_query('update livros set pu_ebook_flag = True where pu_id= %s',(livro_id,))
        c['status'] = 'OK'
        return c
    else:
        c['status'] = 'file not found'
        return c


def attachment_save(pu_id, file_path):
    if file_path is not None:
        sql = '''select edoc_id, edoc_data, edoc_pub_id, edoc_size, edoc_file_name, edoc_file_format from edoc_data where edoc_pub_id = %s'''
        try:
            hl = dbmain.query_one(sql, (pu_id,))
            a = base64.b64decode(hl[1])
            print(hl[3]/1024,hl[4],hl[5])
            print('-----------------------')
            f = open(file_path + hl[4] + '.' + hl[5], 'wb')
            f.write(a)
        except Exception as e:
            print(str(e))
    #     encoded_var = base64.b64encode(data_dic['texto'])
    #     attach_file(encoded_var)
    #     sql = '''INSERT into attachments (at_type,at_tabela,at_table_id, at_description,at_original, at_attach_id)
    #         values (%s,%s,%s,%s,%s,%s)'''
    #     data = (data_dic['type'], data_dic['at_tabela'], data_dic['at_table_id'],data_dic['at_description'],data_dic['at_original'],pa.ebo_data_id)
    #     dbmain.execute_query(sql,data)
    # else:
    #     if os.path.exists(pa.file_to_attach):
    #         f = open(pa.file_to_attach, 'rb')
    #         binary = f.read()
    #         encoded_var = base64.b64encode(binary)
    #         attach_file(encoded_var)
    #         sql = '''INSERT into attachments (at_type,at_tabela,at_table_id, at_description,at_original, at_attach_id)
    #             values (%s,%s,%s,%s,%s,%s)'''
    #         data = (data_dic['type'], data_dic['at_tabela'], data_dic['at_table_id'],data_dic['at_description'],data_dic['at_original'],pa.ebo_data_id)
    #         dbmain.execute_query(sql,data)


if __name__ == "__main__":
    print('corre do SO')
    #pa.conn_string = "host=192.168.0.98 dbname=livros_sandbox  user=sysdba password= masterkey"
    # f = '/home/zorze/Downloads/KAWAI_K5000_SERVICE_MANUAL.pdf'
    # print attachment_add(f, 2159)
    attachment_save(2159, '/home/zorze/Downloads/')