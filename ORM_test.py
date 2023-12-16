#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select


def slq_alchemy():
    # eng = create_engine('postgresql+psycopg2://root:masterkey@localhost/livros')
    # eng = create_engine('postgresql+psycopg2://root:masterkey@192.168.5.14/livros_develop')
    eng = create_engine('sqlite:///c:/python/gabo/livros.db')
    
    with eng.connect() as con:
        meta = MetaData(eng)
        livros = Table('livros', meta, autoload=True)
        
        # stm = select([livros])
        rs = con.execute('select     pu_id, pu_title     , pu_isbn, pu_cota, pu_obs,pu_tags , pu_volume , pu_type,pu_author_id ,'
                         ' pu_sub_title ,pu_status ,pu_sinopse, pu_ed_year ,pu_modified,pu_cota_new  from livros')
        
        print(rs)
        # for n in rs:
        #     print (n)
        
        
        
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

# print (query_many_sqlite('select * from livros'))

import time
start_time = time.time()
# slq_alchemy()
query_many_sqlite('select     pu_id, pu_title     , pu_isbn, pu_cota, pu_obs,pu_tags , pu_volume , pu_type,pu_author_id, pu_sub_title ,pu_status ,pu_sinopse, pu_ed_year ,pu_modified,pu_cota_new  from livros')
print("--- %s seconds ---" % (time.time() - start_time))
