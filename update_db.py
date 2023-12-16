import datetime
import os
import sys

import psycopg2

import parameters as gl
import stdio

gl.db_params = stdio.read_config_file('gabo.ini')
gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params['db_database'] +\
        ' user=' + gl.db_params['db_user'] + ' password=' +gl.db_params['db_password']
a = ['DIM', 'COVER', 'DATA','COL','LANG', 'PAG', 'ED']

def execute_query(sql, data):
    try:
        conn = psycopg2.connect(gl.conn_string)
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        error_print(e, sql, 'execute_query', data)
        

def error_print(err,sql, caller,data='', to_file=False, d_file=False, show=True):
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


def query_many(sql, data=None):
    try:
        conn = psycopg2.connect(gl.conn_string)
        cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        if data is None:
            cur.execute(sql)
        else:
            cur.execute(sql, data)
        xl = cur.fetchall()
        cur.close()
        conn.close()
        return xl
    
    except Exception as e:
        error_print(e, sql, 'query_main')
        sys.exit(1)






def update_main():
    sql = """select tags_ref_book,tags_ref_key, tags.ta_name
    from tags_reference
             inner join tags on tags.ta_id=tags_ref_tag_id
          where not tags_ref_key is null
          order by tags_ref_book"""
    
    data_set = query_many(sql)
    
    for n in data_set:
        print(n)
        if n[1] == 'DIM':
            execute_query('update livros set pu_dimensions=%s where pu_id=%s' ,(n[2],n[0]))
        elif n[1] == 'COVER':

            execute_query('update livros set pu_cover=%s where pu_id=%s' ,(n[2][0].upper() + n[2][1:], n[0] ))
        elif n[1] == 'DATA':
            execute_query('update livros set pu_edition_date=%s where pu_id=%s' ,(n[2],n[0]))
        # elif n[1] == 'COL':
        #     print('update livros set pu_r=' + n[2] + ' where pu_id=' + str(n[0]))
        elif n[1] == 'LANG':
            execute_query('update livros set pu_language=%s where pu_id=%s' ,(n[2],n[0]))
        elif n[1] == 'PAG':
            execute_query('update livros set pu_pages=%s where pu_id=%s' ,(n[2],n[0]))
        elif n[1] == 'ED':
            execute_query('update livros set pu_publisher=%s where pu_id=%s' ,(n[2].title(),n[0]))

def update_cover():
    execute_query('update livros set pu_cover=%s where pu_cover is null',('Capa mole',))
    
def update_language():
    execute_query('update livros set pu_language=%s where pu_language is null',('Português',))

print(gl.conn_string)

# update_main()
update_cover()
update_language()


"""
alter sequence livros_livroid_seq as integer;

alter sequence tag_ref_id_seq as integer;

alter sequence tags_special_tag_s_id_seq as integer;

create sequence conditions_condition_id_seq;

create sequence classifications_classification_id_seq;

create sequence languages_languages_id_seq as smallint;

create sequence bindings_binding_id_seq as integer;

create sequence status_status_id_seq as integer;

alter table authors drop constraint authors_pk;

alter table last_tags drop constraint last_tags_pk;

alter table livros alter column pu_volume drop not null;

alter table livros alter column pu_volume drop default;

alter table livros drop constraint livros_pk;

alter table locals drop constraint locals_pk;

alter table tags_reference alter column tags_ref_key type varchar(8) using tags_ref_key::varchar(8);

alter table tags_reference drop constraint tag_ref_pkey;

alter table params drop constraint params_pkey;

alter table prep drop constraint prep_pk;

alter table sizes drop constraint sizes_pk;

alter table status drop column st_nome;

alter table status drop column pu_type;

alter table status drop constraint status_pk;

alter table status drop column st_id;

alter table tags alter column tag_key type varchar(8) using tag_key::varchar(8);

alter table tags drop constraint tags_pkey;

alter table tags_special
    alter column tags_special_key type varchar(8) using tags_special_key::varchar(8);

alter table tags_special
    drop constraint tags_special_pk;

alter table types
    alter column ty_order drop not null;

alter table types
    alter column ty_order drop default;

alter table types
    drop constraint genero_pk;

alter table livros
    add pu_volume_collection integer;

alter table livros
    add pu_copy_number integer;

alter table livros
    add pu_edition_date varchar(8);

alter table livros
    add pu_ed_place varchar(20);

alter table livros
    add pu_price varchar(8);

alter table livros
    add pu_source varchar(30);

alter table livros
    add pu_language varchar(30);

alter table livros
    add pu_edition integer;

alter table livros
    add pu_condition varchar(40);

alter table livros
    add pu_volume_series integer;

alter table livros
    add pu_classification varchar(10);

alter table livros
    add pu_publisher varchar(40);

alter table livros
    add pu_pages integer;

alter table livros
    add pu_dimensions varchar(12);

alter table livros
    add pu_cover varchar(16);

alter table status
    add status_id integer default nextval('status_status_id_seq'::regclass) not null;

-- pode haver um erro aqui nos estados
alter table status
    add status_name varchar(80) not null;

alter table status
    add status_order integer default 1 not null;

create unique index status_status_name_uindex
    on status (status_name);

create unique index status_status_id_uindex
    on status (status_id);

alter table status
    add constraint status_pk
        primary key (status_id);

create table conditions
(
    condition_id    smallint default nextval('conditions_condition_id_seq'::regclass) not null,
    condition_name  varchar(60)                                                       not null,
    condition_order integer  default 1                                                not null
);

create table classifications
(
    classification_id    smallint default nextval('classifications_classification_id_seq'::regclass) not null,
    classification_name  varchar(12)                                                                 not null,
    classification_order integer  default 1                                                          not null,
    constraint classifications_pk
        primary key (classification_id)
);

create unique index classifications_classification_id_uindex
    on classifications (classification_id);

create table languages
(
    language_id    smallint default nextval('languages_languages_id_seq'::regclass) not null,
    language_name  varchar(40)                                                      not null,
    language_order integer  default 1                                               not null,
    constraint languages_pk
        primary key (language_id)
);

create unique index languages_languages_id_uindex
    on languages (language_id);

create unique index languages_language_name_uindex
    on languages (language_name);

create table bindings
(
    binding_id    integer default nextval('bindings_binding_id_seq'::regclass) not null,
    binding_name  varchar(40)                                                  not null,
    binding_order integer default 1                                            not null,
    constraint bindings_pk
        primary key (binding_id)
);

create unique index bindings_binding_id_uindex
    on bindings (binding_id);

create unique index bindings_binding_name_uindex
    on bindings (binding_name);

alter table livros add pu_collection varchar(80);
alter table livros add pu_series_name varchar(80);
create unique index tags_ta_id_uindex
    on tags (ta_id);


"""


'''
SQLite

STEP1: make a dump of your database structure and data

pg_dump -h 192.168.5.14 --create --inserts -f myPgDump.sql -d livros -U root
-W masterkey

STEP2: delete everything except CREATE TABLES and INSERT statements out of myPgDump.sql (using text editor)

STEP3: initialize your SQLite database passing structure and data of your Postgres dump

sqlite3 livros.db -init myPgDump.sql

STEP4: use your database ;)


'''





