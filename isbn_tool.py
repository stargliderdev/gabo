#!/usr/bin/python
# -*- coding: utf-8 -*-
import pprint

import stdio
import search_isbn
import parameters as pa
import dmPostgreSQL as dbmain
import settings
import data_access


def insert_record(record_set):
    sql = '''insert into livros (
    pu_author_id,
    pu_ed_date ,
    pu_media_format,
    pu_media ,
    pu_isbn ,
    pu_obs,
    pu_pages,
    pu_editor_id,
    pu_title )
    VALUES ,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''


    data =  (pa.autores_dict[record_set['pu_author_id']], record_set['pu_ed_date'],
             pa.media_formats_dict[record_set['media_format']], pa.media_dict[record_set['media']],record_set['pu_isbn'],
             record_set['pu_sinopse'], record_set['pu_pages'], pa.editoras_dict[record_set['pu_editor']],
             record_set['pu_title'])

    a = dbmain.execute_query(sql,data)

    # campos especiais
    #pa.currentRecord = dbmain.output_query_one('select max(pu_id) from livros', (True, )).output[0]
    # actualiza obs
    #a = dbmain.execute_query('update livros set pu_obs = %s where pu_id=%s', (unicode(self.pu_obs.toPlainText()).encode('utf-8'), pa.currentRecord))
    #b = dbmain.execute_query('update livros set pu_sinopse = %s where pu_id=%s', (unicode(self.pu_sinopse.toPlainText()).encode('utf-8'), pa.currentRecord))

settings.load_settings()
data_access.refresh_datasets(101)

def insert_data():
    print('le ficheiro com isbn')
    f = stdio.read_file('isbn.txt')
    print('apaga ficheiro com output isbn')
    stdio.delete_file('isbn.log')
    print('loop principal')
    for n in f:
        is_in_isbn =  search_isbn.search_by_isbn(n)
        if is_in_isbn[0]:
            toto = is_in_isbn[1]

            if dbmain.query_one('select pu_isbn from livros where pu_isbn =%s', (n,)) == None:
                print(' não existe')
                if toto['pu_author_id'] not in pa.autores_dict:
                    data_access.addRecord2Table('authors', 'au_name',dum, 'pu_type')
                    #refresca
                    data_access.get_autores(101)

                if toto['pu_editor'] not in pa.editoras_dict:
                    data_access.addRecord2Table('publishers', 'pb_name',dum, 'pu_type')
                    #refresca
                    data_access.get_editoras(101)
                if toto['media_format'] not in pa.media_formats_dict:
                    data_access.addRecord2Table('media_formats', 'mf_name',dum, 'pu_type')
                    #refresca
                    data_access.get_media_formats(101)
                if toto['media'] not in pa.media_dict:
                    data_access.addRecord2Table('media', 'me_name',dum, 'pu_type')
                    #refresca
                    data_access.get_media(101)

            else:
                print('existe')

        else:
            print('não existe ficha', n)
            print('    adiciona ao ficheiro o isbn com erro')
        print('proximo')

settings.load_settings()
data_access.refresh_datasets(101)
data_access.search_data_in_table('authors','au_name','Gabriel García Márquez')

print('fim')