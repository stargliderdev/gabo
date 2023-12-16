#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
try:
    from PyQt4.QtCore import QT_VERSION_STR
    from PyQt4.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR
except ImportError:
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR

import parameters as gl
import psycopg2
import psycopg2.extras


def addRecord2Table(table, field, value, type_field):
    value = str(value)
    execute_query('insert into ' + table + ' ( ' + field + ',' + type_field + ') values(%s); ', (value,))


def get_types():
    a = query_many('select ty_id,ty_name from types  ')
    gl.types_dict = {}  # {u'Ficção':1, 'Romance':2, 'Ensaio':3, 'Técnico':4}
    gl.types_list = []  # [u'Ficção', u'Romance', u'Ensaio', u'Técnico'])
    for n in a:
        gl.types_dict[n[1]] = n[0]
        gl.types_list.append(n[1])


def get_autores():
    a = query_many('select au_id, au_name from authors order by au_name asc')
    gl.dsAutores = []  # QStringList()
    gl.autores_dict = {}
    for n in a:
        gl.autores_dict[n[1]] = n[0]
        gl.dsAutores.append(n[1])


def get_status():
    a = query_many('select status_id,status_nome from status')
    gl.dsStatus = []
    gl.status_dict = {}
    for n in a:
        gl.status_dict[n[1]] = n[0]
        gl.dsStatus.append(n[1])
    # estados fisicos
    gl.dsEstadoFisico = ['Novo', 'Usado']
    gl.estado_fisico_dict = {'Novo': 'Novo', 'Usado': 'Usado'}


def search_data_in_table(table, field, data_to_search):
    sql = 'SELECT * from ' + table + ' where ' + 'lower(' + field + ') = \'' + data_to_search.lower() + '\''
    print(sql)
    if query_one(sql, (True,)):
        print('esisote')
    else:
        print('nao existe')


def get_livro_data(index):
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''SELECT livros.pu_id, livros.pu_title, authors.au_name,
        livros.pu_cota,types.ty_name,
        livros.pu_obs,  
        livros.pu_isbn,status.st_nome, pu_sinopse, pu_volume,pu_ed_year,types.ty_id,status.status_id
        FROM livros, authors,types, status
        WHERE livros.pu_id = %s and  
        types.ty_id = livros.pu_type  and
        livros.pu_author_id=authors.au_id AND 
        livros.pu_status = status.status_id;'''
    dict_cur.execute(sql, (index,))
    rec = dict_cur.fetchone()
    if rec == []:  # houve um erro e o registo está limpo.
        return -1
    return rec


def get_modelo_data(index):
    gl.conn_string = "host=" + gl.db_host + " dbname=" + gl.db_database + " user=" + gl.db_user + " password=" + gl.db_password
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
            types.ty_nema,
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
    dict_cur.execute(sql, (index,))
    rec = dict_cur.fetchone()
    if rec == []:  # houve um erro e o registo está limpo.
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
        types.ty_id = livros.pu_type AND assuntos.as_id = livros.pu_subject AND
        livros.pu_media_format=media_formats.mf_id AND livros.pu_serie = series.se_id AND 
        livros.pu_author_id=authors.au_id AND publishers.pb_id = livros.pu_editor_id AND 
        livros.pu_status = status.status_id AND livros.pu_language=languages.lg_id AND
        livros.pu_bd_hero = hero.he_id;'''
    dict_cur.execute(sql, (index,))
    
    rec = dict_cur.fetchone()
    if rec == []:  # houve um erro e o registo está limpo.
        return -1
    conn.close()
    return rec

def update_tags_1(id, tag_list):
    for n in tag_list:
        a = execute_query('insert into tags_reference(tr_book, tr_tag) values(%s,%s) ', (id, n))


def update_tags(id, tag_list):
    # id = livro
    tags_id = []
    tag_max = query_one('''Select max(ta_id)+1 as t from tags''', (True,))[0]
    # print tag_max
    for n in tag_list:
        toto = n.lower().strip()
        if toto != '':
            a = query_one('select ta_id from tags where ta_name = %s', (toto,))
            if a == None:  # é nova
                execute_query('insert into tags (ta_name) values(%s)', (toto,))
                tags_id.append((id, tag_max))
                tag_max += 1
            else:
                tags_id.append((id, a[0]))
    # print 'tags.id',tags_id
    sql = ''' INSERT INTO tags_reference(tr_book, tr_tag) VALUES''' + str(tags_id)[1:-1]
    execute_query(sql, (True,))


def get_record(uuid):
    conn = psycopg2.connect(gl.conn_string)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''select * from livros
           where pu_id = %s'''
    dict_cur.execute(sql, (uuid,))
    rec = dict_cur.fetchone()
    conn.close()
    return rec

def execute_query(sql, data):
    try:
        conn = psycopg2.connect(gl.conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')

        # print 'mogrify:', cur.mogrify(sql, data)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        print('-------------------------------------------------------')
        print((str(e) + '\n -- SQL Error --\n in :' + '\n' + sql + '\n', data))
        exit(1)


def query_many(sql):
    try:
        conn = psycopg2.connect(gl.conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        # print 'mogrify:', cur.mogrify(sql, data)
        cur.execute(sql)
        xl = cur.fetchall()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        print('Erro de SQL output_query_many' + str(e) + '\n -- SQL Error --\n in :' + '\n' + sql)
        exit(1)


def query_one(sql, data):
    try:
        conn = psycopg2.connect(gl.conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        cur.execute(sql, data)
        xl = cur.fetchone()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        print('-------------------------------------------------------')
        print((str(e) + '\n -- SQL Error --\n in :' + '\n' + sql + '\n', data))
        exit(1)

def insert_tags(tags, pu_id):
    tags_list = tags.split(',')
    if tags_list[0] == '':
        cleantag_rfs = execute_query('delete from tags_reference where tr_book = %s', (pu_id, ))
    else:
        cleantag_rfs = execute_query('delete from tags_reference where tr_book = %s', (pu_id, ))
        update_tags(tags_list)
        tagID = get_tags_index(tags_list)
        update_tags(self.pub_id, tagID)


def db_converter():
    gl.conn_string = "host=localhost dbname=livros user=root password=masterkey"
    
    bc = query_many('''Select pu_id
                    from livros
                    --where pu_id in (110,111,112,113,114,115,116,117,118,119,120)
                    order by pu_id ''')
    for xl in bc:
        tags = ''
        ed_org = 0
        book_data = get_record(xl)
        print('#',book_data['pu_id'])
        # print('{:40}'.format(book_data['pu_title']), '#',book_data['pu_id'])
        
        # if book_data['pu_author_others'] is not None:
        #     print('encontrou outros')
        #     y =book_data['pu_author_others'].split(' e ')
        #     b = query_one('select au_name from authors where au_id=%s', (book_data['pu_author_id'],))
        #     c = b[0] + ',' + ','.join(y)
        #     t = query_one('select au_id from authors where lower(au_name) =%s ', (c.lower(),) )
        #     if not t == '':
        #         print('cria autores')
        #         execute_query('insert into authors (au_name) values (%s)', (c,))
        #         execute_query('update livros set pu_author_id = (select au_id from authors where au_name=%s) '
        #                       'where pu_id =%s', (c, xl ))
        #
        #     else:
        #         print('já existem')
        #         execute_query('update livros set pu_author_id = (select au_id from authors where au_name=%s) '
        #                       'where pu_id =%s', (c, xl ))
        # if book_data['pu_subject'] > 1:
        #     b = query_one('select as_nome  from assuntos where as_id=%s', (book_data['pu_subject'],))
        #     tags += b[0].lower() + ','
      
        
        if book_data['pu_translator'] is not None:
            z = book_data['pu_translator'].replace(' e ',',')
            z = z.replace('/ ',',')
            for c in z.split(','):
                 tags += 'trad:' + c.strip() + ','
        # if book_data['pu_ed_local'] is not None:
        #     tags += 'local:' + book_data['pu_ed_local'].lower() + ','
        z = book_data['pu_ed_date']
        ed = 0
        try:
            if z is not None:
                z = z.strip()
                x = z.find('/')
                if x > 0:
                    z = z[:x]
                z = z.replace('(','')
                z = z.replace(')','')
                z = z.split(' ')
    
                if len(z) > 1:
                    tags += 'ed org:' + z[0].strip() + ','
                    ed = int(z[1])
                elif len(z) == 1:
                    # tags += 'ed org:' + z[0].strip() + ','
                    ed = int(z[0])
        except ValueError:
            ed= 0
        execute_query('update livros set pu_ed_year=%s where pu_id=%s', (ed, book_data['pu_id']))
    
    
        z = book_data['pu_pages']
        if z > 0:
            tags += 'pag:' + str(z) + ','
        z = book_data['pu_media']
        if z in (2,5,6):
            tags += 'capa dura,'
        else:
            tags += 'capa mole,'
            
        # tags += book_data['as_nome'].lower() + ','
        z = book_data['pu_type']
        if z == 1:
            tags += 'ficção,'
        elif z == 2:
            tags += 'romance,'
        elif z == 3:
            tags += 'ensaio,'
        elif z == 4:
            tags += 'técnico,'
        elif z == 5:
            tags += 'ficção,'
        # z = book_data['pu_media_format']
        # if z > 1: # aguarda opinião
            # b = output_query_one('select mf_name from media_formats where mf_id=%s', (z,))
            # tags += b[0].replace(' mm','') + ','
        if book_data['pu_editor_id'] > 1:
            b = query_one('select pb_name from publishers where pb_id=%s', (book_data['pu_editor_id'],))
            b = b[0].replace(',','')
            tags += 'edt:' + b.lower() + ','

        if book_data['pu_media_format'] > 1:
            b = query_one('select mf_name from media_formats where mf_id=%s', (book_data['pu_media_format'] ,))
            a = b[0].replace(' ', '')
            a = a.replace('mm', '')
            tags += a.lower() + ','
        
        he = tags[:-1].split(',')

        # print('       tags',he)

        for n in he:
            n = n[:45]
            try:
                a = query_one('select ta_id from tags where lower(ta_name) = %s', (n.lower(),))
                execute_query('insert into tags_reference(tr_book, tr_tag) VALUES (%s,%s)', (book_data['pu_id'], a[0]))
            except TypeError:
                execute_query('insert into tags (ta_name) VALUES (%s)', (n.lower(),))
                a = (query_one('select ta_id from tags where lower(ta_name) = %s', (n.lower(),)))
                execute_query('insert into tags_reference(tr_book, tr_tag) VALUES (%s,%s)', (book_data['pu_id'], a[0]))
    
    
def get_system_info():
    print(sys.version)
    print("Qt version:", QT_VERSION_STR)
    print("SIP version:", SIP_VERSION_STR)
    print("PyQt version:", PYQT_VERSION_STR)
    
def main():
    gl.conn_string = "host=localhost dbname=livros user=root password=masterkey"
    
    bc = query_many('''Select * from tags''')
    for n in bc:
        # print (n[1])
        a = n[1].split(':')
        if len(a)>1:
            # print(a[0].upper(),a[1])
            if a[0].upper() in ['DATA','ED','DIM','COL','PAG', 'TRAD']:
                # print(n,'=>',a[1], a[0])
                # print('update tags set ta_name=%s, tags_key=%s, tag_level=1 where ta_id=%s', (a[1],a[0].upper(),n[0]))
                h = execute_query('update tags set ta_name=%s, tag_key=%s where ta_id=%s',(a[1],a[0].upper(),n[0]))
                h = execute_query('update tags_reference set tags_ref_key=%s, tags_ref_level=1 where tags_ref_tag_id=%s',(a[0].upper(),n[0]))
                

main()
