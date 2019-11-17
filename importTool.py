#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
import traceback
import sys
import string
import psycopg2


# modulos externos
import lib.dmPostgreSQL as dbmain
import lib.dataAcess as dataAcess
SEP = ','
COMMA = '"'
_mod = 'importTool.py'
VERSION = '1.3'
IP = '192.168.0.102'

def execute_query(sql, data):
    try:
        conn = psycopg2.connect("host=" + IP + " dbname=livros user=sysdba password=masterkey")
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        #print 'mogrify:', cur.mogrify(sql, data)
        cur.execute(sql, data)      
        conn.commit()
        cur.close()
        conn.close()
#        
    except Exception as e:
        print('-'*40)         
        print(str(e) +  '\n -- SQL Error --\n:' + sql + '\n SQL data :\n') 
        print(data)
        print('-'*40)
        sys.exit(1)
        


class OutputQueryOne:
    def __init__(self,  sql):
        
        try:
            conn = psycopg2.connect("host=" + IP +" dbname=livros user=sysdba password=masterkey")
            cur = conn.cursor()
            conn.set_client_encoding('UTF8')
            cur.execute(sql)      
            self.output =  cur.fetchall()
            if len(self.output) >0:
                self.output = self.output[0]
            else:
                self.output = -1
        except Exception as e:
            print((str(e) +  '\n -- SQL Error --\n in :' + _mod + '\n' + sql))
            exit(1) 


class OutputQueryAll:
    def __init__(self,  sql):
        
        try:
            conn = psycopg2.connect("host=" + IP +" dbname=livros user=sysdba password=masterkey")
            cur = conn.cursor()
            conn.set_client_encoding('UTF8')
            cur.execute(sql)      
            self.output =  cur.fetchall()
            if len(self.output) >0:
                pass #self.output = self.output[0]
            else:
                self.output = -1
        except Exception as e:
            print((str(e) +  '\n -- SQL Error --\n in :' + _mod + '\n' + sql))
            exit(1) 


def usage():
    print("Importa para o RestWare um ficheiro com artigos separado por pipes (|)")
    print('Versão:',  VERSION)
    print("  Utilização: "+sys.argv[0]+ " <nome do ficheiro> + [IP]") 


if __name__ == "__main__":
    
#    file_csv = open('db/livros.csv') 
#    try:
#        livros_csv = file_csv.read().splitlines()
#    finally:
#        file_csv.close()
#    
#    
#    for n in livros_csv:
#        foo = n.split('|')
#        print foo[0],  foo[9]
#        g = execute_query('update livros set pu_editor = %s where livros.pu_id=%s;',(foo[9],foo[0]) )

    b = OutputQueryAll('select pb_id, pb_name from publishers')
    dum = b.output
    #a = OutputQueryOne('select  * from livros ')
#    
    for n in dum:
        print(n)
        g = execute_query('update livros set pu_editor_id = %s where pu_editor=%s',n )
#
            
            
