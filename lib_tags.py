
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parameters as gl
import sqlite_crud


def update_special_tags(pub_id,level=1):
    sqlite_crud.execute_query('DELETE FROM tags_reference '
            'WHERE tags_ref_book = ? and tags_ref_key in (select tags_special_key FROM tags_special WHERE tags_special_level=?) '
            , (pub_id,level))
    tags_id = []
    tag_max = dbmain.query_one('''SELECT MAX(ta_id)+1 AS t FROM tags''', (True,))[0]
    if tag_max is None:
        tag_max = 1
    for n in gl.TAGS_SPECIAL_LEVEL1_DATA:
        a = dbmain.query_one('SELECT ta_id FROM tags where lower(ta_name) = ? and tag_key = ?', (n[1].lower(),n[0]))
        if a == None: # é nova
            sqlite_crud.execute_query('INSERT INTO tags (ta_name, tag_key) values(?,?)', (n[1],n[0]))
            tags_id.append((pub_id,tag_max, n[0],level))
            tag_max +=1
        else:
            tags_id.append((pub_id,a[0], n[0],level))
    sql = ''' INSERT INTO tags_reference(tags_ref_book, tags_ref_tag_id, tags_ref_key, tags_ref_level) VALUES''' + str(tags_id)[1:-1]
    if not tags_id == []:
        sqlite_crud.execute_query(sql, (True, ))
    