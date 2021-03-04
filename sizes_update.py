#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import parameters as gl
import dmPostgreSQL as dbmain

import data_access as data_access
import info as info
import qlib
import tag_browser
import edit_record
import stdio
import options_new
import authors
import make_report_html
import report_display




def set_sizes():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.db_params = gl.db_params[1]
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    dbmain.execute_query('delete from sizes', (True,))
    t = dbmain.query_many('select ta_name from tags order by ta_name')
    for n in t:
        a = n[0].split('x')
        if len(a) == 3:
            try:
                dum = int(a[0]) + int(a[1]) + int(a[2])
                print(n[0])
                dbmain.execute_query('insert into sizes (size_name) VALUES (%s)', (n[0],))
            except ValueError:
                pass

def get_areas():
    gl.db_params = stdio.read_config_file('gabo.ini')
    gl.db_params = gl.db_params[1]
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + gl.db_params[
        'db_database'] + \
                     ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    areas = dbmain.query_many('select distinct pu_cota from livros order by pu_cota')
    
main()