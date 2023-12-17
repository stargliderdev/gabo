#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import time
import sqlite3

import parameters as gl
import settings
import sqlite_crud


def create_database():
    print('Create Database', gl.DB_PATH+gl.DB_FILE)
    try:
        os.remove(gl.DB_PATH + gl.DB_FILE)
    except OSError as e:
        # print(f"Error deleting {gl.DB_PATH + gl.DB_FILE}: {e}")
        conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
        conn.commit()
        conn.close()


def update_1():
    create_database()
    write_script('''DROP TABLE IF EXISTS books''')
    write_script(''' create table books
        (
            pu_id                INTEGER PRIMARY KEY AUTOINCREMENT,
            pu_title             varchar(100),
            pu_isbn              varchar(25),
            pu_local              varchar(10),
            pu_obs               text,
            pu_tags              varchar(1024),
            pu_volume            integer,
            pu_type              varchar(100) default 'Romance',
            pu_author            varchar(150) default 'Varios',
            pu_sub_title         varchar(255),
            pu_status            varchar(80) default 'Na Colecção',
            pu_sinopse           text,
            pu_year              varchar,
            pu_modified          timestamp,
            pu_local_new         varchar,
            pu_volume_collection integer,
            pu_copy_number       integer,
            pu_edition_date      varchar(8),
            pu_edition_place     varchar(30),
            pu_price             varchar(8),
            pu_source            varchar(40),
            pu_language          varchar(30),
            pu_edition           integer,
            pu_condition         varchar(40),
            pu_volume_serie      integer,
            pu_classification    varchar(10),
            pu_publisher         varchar(40),
            pu_pages             varchar(10),
            pu_dimensions        varchar(12),
            pu_cover             varchar(16),
            pu_collection        varchar(80),
            pu_serie             varchar(100),
            pu_translator        varchar(255),
            pu_color varchar(150),
            pu_draw      varchar(150),
            pu_isbn10    char(10),
            pu_dep_legal varchar(20),
            pu_design_cover varchar(150),
            pu_title_original varchar(100),
            pu_printer varchar(80),
            pu_weight char(6),
            pu_print_number integer,
            pu_preface varchar(150),
            pu_inventory varchar(20),
            pu_editor varchar(80)
            
        );''')

    write_script('''CREATE INDEX books_title_idx on books(pu_title);''')
    write_script('''CREATE INDEX books_author_idx on books(pu_author);''')
    write_script('''CREATE INDEX books_status_idx on books(pu_status);''')

    write_script('''create table if not exists params (param_key varchar(20) not null,
        param_data text, 
        param_name varchar(50) default nd not null,
        param_level int default 0 not null);''')

    write_script('''create table authors
    (au_id integer  PRIMARY KEY AUTOINCREMENT,
        au_name varchar(150) not null,
        UNIQUE (au_name));''')

    write_script('''create table if not exists classifications
    (
        classification_id integer PRIMARY KEY AUTOINCREMENT not null,
        classification_name varchar(12) not null,
        classification_order integer default 1 not null,
        unique (classification_name)
    );''')

    write_script('''create table if not exists conditions
    (
        condition_id integer PRIMARY KEY AUTOINCREMENT not null,
        condition_name varchar(60) not null,
        condition_order integer default 1 not null,
        unique (condition_name)
    );''')

    write_script('''create table if not exists languages
    (
        language_id integer PRIMARY KEY AUTOINCREMENT not null,
        language_name varchar(40) not null,
        language_order integer default 1 not null,
        unique (language_name)
    );''')

    write_script('''create table if not exists locals
    (
        local_id integer PRIMARY KEY AUTOINCREMENT not null,
        local_name varchar(30) not null,
        local_size_w integer default 200,
        local_size_h integer default 210 not null,
        local_size_c integer default 10 not null,
        local_free_width integer default 0 not null,
        local_use_of varchar(100),
        unique (local_name)
    );''')

    write_script('''create table if not exists words
    (
        word_id integer PRIMARY KEY AUTOINCREMENT not null,
        word_value varchar(10) not null
    );''')

    write_script('''create table if not exists sizes
    (
        size_id integer PRIMARY KEY AUTOINCREMENT not null,
        size_name varchar(15) not null,
        unique (size_name)
    );''')

    write_script('''create table if not exists status
        (
        status_id integer PRIMARY KEY AUTOINCREMENT not null,
        status_name varchar(80) not null,
        status_order integer default 1 not null,
        unique (status_name)
        );''')

    write_script('''create table if not exists types
    (  	ty_id integer PRIMARY KEY AUTOINCREMENT not null,
        ty_name varchar(100) not null,
        ty_order smallint default 1,
        unique (ty_name)    );''')

    write_script('''create table if not exists covers
    (
        cover_id integer PRIMARY KEY AUTOINCREMENT not null,
        cover_name varchar(30) not null,
        cover_order integer default 1,
        unique (cover_name)

    );''')

    write_script('''create table if not exists tags
        (
        ta_id   INTEGER     not null  constraint tags_pk primary key autoincrement,
        ta_name varchar(45) not null    unique
        );''')

    write_script('''create table tags_reference
        (
	        tags_ref_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	        tags_ref_book integer not null,
	        tags_ref_key varchar
	    );''')

    write_script('''create table publishers
        (publisher_id   INTEGER      not null
            primary key autoincrement,
            publisher_name varchar(100) not null
        unique);''')

    write_script('''INSERT INTO params (param_key, param_data) VALUES ('OWNER', 'Euzinho');''')
    write_script('''INSERT INTO params (param_key, param_data) VALUES ('LAST_LANGUAGE', 'Português');''')
    write_script(
        '''INSERT INTO params (param_key, param_data) VALUES ('GRID_COLUMN_SIZES', '[(0, 54), (1, 345), (2, 260), (3, 73), (4, 90), (5, 40), (6, 40), (7, 63), (8, 56), (9, 69), (10, 74), (11, 0), (12, 0)]');''')
    write_script(
        '''INSERT INTO params (param_key, param_data) VALUES ('LAST_TAGS', '');''')
    write_script('''INSERT INTO params (param_key, param_data) VALUES ('LAST_STATUS', 'Na Colecção');''')
    write_script('''INSERT INTO params (param_key, param_data) VALUES ('LAST_PUB_TYPE', 'Romance');''')
    write_script('''INSERT INTO params (param_key, param_data) VALUES ('LAST_BINDING', 'Capa mole');''')
    write_script('''INSERT INTO params (param_key, param_data) VALUES ('SHOW_RECORDS', '80');''')
    write_script('''INSERT INTO params (param_key, param_data, param_name,param_level) VALUES ('DB_VERSION', '1','Versão da Base de Dados',1);''')
    write_script('''INSERT INTO params (param_key, param_data, param_name,param_level) VALUES ('BIN_VERSION','20231125', 'Versão do Programa',1);''')

    write_script('''CREATE TRIGGER insert_into_authors
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO authors (au_name) VALUES (NEW.pu_author);
        END;''')

    write_script('''
        CREATE TRIGGER update_authors_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO authors (au_name) VALUES (NEW.pu_author);
        END;''')
    write_script('''CREATE TRIGGER insert_into_types
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO types (ty_name) VALUES (NEW.pu_type);
        END;''')

    write_script('''CREATE TRIGGER update_types_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO types (ty_name) VALUES (NEW.pu_type);
        END;''')

    write_script('''CREATE TRIGGER insert_into_status
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO status (status_name) VALUES (NEW.pu_status);
        END;''')

    write_script('''CREATE TRIGGER update_status_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO status (status_name) VALUES (NEW.pu_status);
        END;''')

    write_script('''CREATE TRIGGER insert_into_languages
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO languages (language_name) VALUES (NEW.pu_language);
        END;''')

    write_script('''CREATE TRIGGER update_languages_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO languages (language_name) VALUES (NEW.pu_language);
        END;''')



    write_script('''CREATE TRIGGER insert_into_covers
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO covers (cover_name) VALUES (NEW.pu_cover);
        END;''')

    write_script('''CREATE TRIGGER update_covers_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO covers (cover_name) VALUES (NEW.pu_cover);
        END;''')

    write_script('''CREATE TRIGGER insert_into_conditions
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO conditions (condition_name) VALUES (NEW.pu_condition);
        END;''')

    write_script('''CREATE TRIGGER update_conditions_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO conditions(condition_name) VALUES (NEW.pu_condition);
        END;''')

    write_script('''CREATE TRIGGER insert_into_classifications
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO classifications (classification_name) VALUES (NEW.pu_classification);
        END;''')

    write_script('''CREATE TRIGGER update_classifications_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO classifications (classification_name) VALUES (NEW.pu_classification);
        END;''')
    write_script('''CREATE TRIGGER insert_into_locals
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO locals(local_name) VALUES (NEW.pu_local);
        END;''')

    write_script('''CREATE TRIGGER update_locals_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO locals (local_name) VALUES (NEW.pu_local);
        END;''')

    write_script('''CREATE TRIGGER insert_into_tags
        AFTER INSERT ON tags_reference
        BEGIN
            INSERT OR IGNORE INTO tags (ta_name) VALUES (NEW.tags_ref_key);
        END;''')

    write_script('''CREATE TRIGGER update_tags_on_update
        AFTER UPDATE ON tags_reference
        BEGIN
            INSERT OR IGNORE INTO tags (ta_name) VALUES (NEW.tags_ref_key);
        END;''')

    write_script('''create table if not exists collections
    (  	collection_id integer PRIMARY KEY AUTOINCREMENT not null,
        collection_name varchar(100) not null,
        unique (collection_name));''')

    write_script('''CREATE TRIGGER collections_on_insert
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO collections (collection_name) VALUES (NEW.pu_collection);
        END;''')

    write_script('''CREATE TRIGGER collections_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO collections (collection_name) VALUES (NEW.pu_collection);
        END;''')

    write_script('''create table if not exists series
    (  	serie_id integer PRIMARY KEY AUTOINCREMENT not null,
        serie_name varchar(100) not null,
        unique (serie_name)    );''')

    write_script('''CREATE TRIGGER series_on_insert
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO series (serie_name) VALUES (NEW.pu_serie);
        END;''')

    write_script('''CREATE TRIGGER series_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO series (serie_name) VALUES (NEW.pu_serie);
        END;''')

    write_script('''CREATE TRIGGER publishers_on_insert
        AFTER INSERT ON books
        BEGIN
            INSERT OR IGNORE INTO publishers (publisher_name) VALUES (NEW.pu_publisher);
        END;''')

    write_script('''CREATE TRIGGER publishers_on_update
        AFTER UPDATE ON books
        BEGIN
            INSERT OR IGNORE INTO publishers (publisher_name) VALUES (NEW.pu_publisher);
        END;''')

def update_2():
    print('update 2')
    write_script('ALTER TABLE books ADD pu_price1 varchar(8);')
    write_script('ALTER TABLE books	ADD pu_price2 varchar(8);')
    write_script('''UPDATE params SET param_data=\'2\' where param_key=\'DB_VERSION\'''')
    write_script('''INSERT INTO params (param_key, param_data, param_name, param_level) VALUES (\'DB_COMMENTS\', null, \'Comentários\', 1);''')
    write_script('''INSERT INTO params (param_key, param_data, param_name, param_level) VALUES (\'DB_SUBJECT\', null, \'Assunto\', 1);''')

def update_3():
    print('update 3')
    write_script('''INSERT INTO words ( word_value) VALUES ('de');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('a');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('em');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('para');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('com');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('por');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('um');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('uma');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('o');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('no');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('os');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('as');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('e');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('do');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('da');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('dos');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('das');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('in');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('and');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('of');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('the');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('by');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('que');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('to');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('at');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('UFO');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('ST');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('V');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('BD');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('IX');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('III');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('IV');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('I');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('II');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('OVNI');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XV');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XI');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('VIII');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XII');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XXI');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XVII');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('VII');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('VI');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XIX');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('X');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XVI');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XVIII');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XIV');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XIII');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('XX');''')
    write_script('''INSERT INTO words ( word_value) VALUES ('ZX');''')
    write_script('''update params set param_data='3' where param_key='DB_VERSION';''')
    write_script('''INSERT INTO params (param_key, param_data, param_name, param_level) VALUES ('DIR_BACK', null, 'Local para guardar o backup', 2);''')
    write_script('''INSERT INTO params (param_key, param_data, param_name, param_level) VALUES ('BACKUP_FLAG', 'False', 'Flag da base de dados alterada', 0);''')

def write_script(sql, silent=True):
    conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
    cursor = conn.cursor()
    sql = sql.replace("\n", " ")
    if silent:
        pass
    else:
        print('WRITE:', sql[:40])
    try:
        cursor.execute(sql)
    except Exception as e:
        print('ERROR ', str(e))
        exit(2)
    conn.commit()
    conn.close()

def get_db_version():
    a = sqlite_crud.query_one('select param_data from params where param_key=\'DB_VERSION\'')
    return int(a[0])

def updater():
    # print(sqlite_crud.check_alive())
    print('update da ', gl.DB_VERSION, ' para ', '3' )
    if gl.DB_VERSION == 0: update_1()
    if gl.DB_VERSION == 1: update_2()
    if gl.DB_VERSION == 2: update_3()

if __name__ == '__main__':
    # file_path='/home/zorze/python/books/databases/'
    # file_name='test.db'
    settings.load_settings()
    print(gl.DB_PATH)
    print(gl.DB_FILE)
    updater()