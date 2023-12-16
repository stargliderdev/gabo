import sys

import parameters as gl
import dmPostgreSQL as dbmain


def calc_width_in_filter():
    publication_ids = []
    xl = dbmain.query_many(gl.CURRENT_SQL)
    height = 0
    width = 0
    depth = 0
    no_dimensions = 0
    com_dim = 0
    de = []
    for n in xl:
        de_dum = (n[0], n[1], n[2], n[7], n[6], n[5], n[8])
        sql = '''select ta_name
            from tags_reference
            inner join tags on ta_id = tags_ref_tag_id
            where tags_ref_key ='DIM' and tags_ref_book =%s'''
        bc = dbmain.query_one(sql, (n[0],))
        if bc is None:
            no_dimensions += 1
            de_dum += '-', 'sem dim'
        else:
            dim = bc[0].split('x')
            if len(dim) == 3:
                if width < int(dim[0]):
                    width = int(dim[0])
                if height < int(dim[1]):
                    height = int(dim[1])
                depth += int(dim[2])
                com_dim += 1
                if int(dim[0]) > int(dim[1]):
                    # print('Duvidoso', n[1],bc[0] )
                    de_dum += bc[0], 'Trocados',
                else:
                    de_dum += bc[0], 'OK'
            else:
                no_dimensions += 1
                de_dum += bc[0], 'falta',
        de.append(de_dum)
    # print('----------------------------')
    # print('Mais fundo', width)
    # print('Mais Alto', height)
    # print('Comprimento', depth)
    # print('sem dim'), no_dimensions
    # print('calc_width_in_filter')
    # print('------end debug-------')
    
    return de, {'width': width, 'height': height, 'depth': depth, 'no_dim': no_dimensions,
                'with_dim': len(de) - no_dimensions}

#
# def calc_width_in_filter_v1():
#     publication_ids = []
#     xl = dbmain.query_many(gl.CURRENT_SQL)
#     for n in xl:
#         publication_ids.append(str(n[0]))
#     in_list = ','.join(publication_ids)
#     sql = '''select pu_id,livros.pu_title,'-',ta_name, '1',livros.pu_ed_year, livros.pu_cota,
#        SPLIT_PART(ta_name, 'x', 1) as l,
#        SPLIT_PART(ta_name, 'x', 2) as h,
#        SPLIT_PART(ta_name, 'x', 3)as d,
#        tags_ref_key
#          from tags_reference
#          left join livros on tags_reference.tags_ref_book = livros.pu_id
#          left join tags on ta_id=tags_reference.tags_ref_tag_id
#         where livros.pu_id in (''' + in_list + ''') and tags_reference.tags_ref_key =\'DIM\''''
#     hl = dbmain.query_many(sql)
#     print('--------Debug---------')
#     print('calc_width_in_filter')
#     pages = 0
#     w = 0
#     d = 0
#     h = 0
#     for n in hl:
#         print(n)
#         w += int(n[7])
#         d += int(n[8])
#         h += int(n[9])
#
#     print('------end debug-------')
#
#     print('ALTURA', w / 10)
#     print('width', d / 10)
#     print('PROFUN', h / 10)
#
#     # print('     width:', leng/10.0)
#     # print('profundidade:', max_width/10.0)
#     # print('      altura:', max_height/10.0)
#     # print('      livros:', len(dimentions))
#     # print('  livros SEM:', missing)
#     print('-' * 40)
#     return hl


# def make_sql(what='', where_index='nada', sort_by=''):
#     gl.CURRENT_SQL = ''
#     select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year,pu_cota_new FROM livros, authors, types, status"
#     join_ = " livros.pu_status = status.st_id AND authors.au_id = livros.pu_author_id AND types.ty_id = livros.pu_type "
#     where_ = ' WHERE '
#     order_ = ''
#     search_ = ''
#     limit_ = ''
#     where_index = where_index.lower()
#     # self.key_sort = self.sort_dic[self.sortByCbox.currentText().lower()]
#     if not what == '':
#         self.recordLimitEdt.setText('0')
#         # self.key_search = self.sort_dic[where_index]
#         if where_index == 'local':  # na cota tem de ser exactamente igual
#             self.key_search = self.sort_dic['local']
#             text_to_search = "\'" + what.lower().strip() + "\'"
#         else:
#             text_to_search = "\'%" + what.lower().strip() + "%\'"
#
#         if len(text_to_search) > 1:
#             where_ += '''unaccent(lower(''' + self.key_search + ''')) LIKE  unaccent(''' + text_to_search + ''') AND '''
#         else:
#             where_ += ''' unaccent(upper(''' + self.key_search + ''')) SIMILAR TO ''' + '''unaccent(''' + text_to_search.upper() + ')' + ''' AND '''
#     elif not self.tags_to_searchEdit.text() == '':  # modo para tags
#         self.recordLimitEdt.setText('0')
#         tags = self.tags_to_searchEdit.text().replace("\'", "\\\'")
#         tags = tags.split(',')
#         in_data = ''
#         if self.logicTags.currentIndex() == 0:  # ou
#             for n in tags:
#                 toto = n.lower().strip()
#                 in_data += "unaccent(\'" + toto + "\'),"
#             a = dbmain.query_many(
#                 '''select ta_id from tags where unaccent(ta_name) in (''' + in_data[:-1] + ''')''')
#             i = []
#             for t in a:
#                 i.append(t[0])
#             if i:
#                 i = str(i)
#                 where_ += '''
#                      pu_id in(select * from (select tags_ref_book from tags_reference where tags_ref_tag_id in(''' + i[
#                                                                                                                      1:-1] + ''')) as foo) AND '''
#             else:
#                 where_ += '''pu_id in(select * from (select tags_ref_book from tags_reference where tags_ref_tag_id in(-1)) as foo) AND '''
#         else:
#             t = ''
#             for n in tags:
#                 t = t + "\'" + n.strip() + "\',"
#             t = t[:-1]
#             c = str(len(tags))
#             where_ = ''' where EXISTS (SELECT NULL
#              FROM tags_reference tg
#              JOIN TAGS t ON t.ta_id = tg.tags_ref_tag_id
#             WHERE unaccent(t.ta_name) IN (unaccent(''' + t + '''))
#               AND tg.tags_ref_book = livros.pu_id
#          GROUP BY tg.tags_ref_book
#            HAVING COUNT(t.ta_name) =''' + c + ''') and '''
#     else:  # não procura em nada
#         where_ += ''' livros.pu_status = status.st_id AND
#       authors.au_id = livros.pu_author_id AND
#       types.ty_id = livros.pu_type and '''
#         self.key_sort = self.sort_dic[self.sortByCbox.currentText().lower()]
#
#     if self.typesCbox.currentIndex() != 0:
#         where_ += " livros.pu_type = (select ty_id from types where ty_name like \'" + str(
#             self.typesCbox.currentText()) + '\') and '
#
#     if self.statusCbox.currentIndex() != 0:
#         where_ += " livros.pu_status = (select st_id from status where st_nome like \'" + str(
#             self.statusCbox.currentText()) + "\') and "
#
#     order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
#
#     if int(gl.SHOW_RECORDS) > 0:  # int(self.recordLimitEdt.text()) > 0:
#         limit_ = 'LIMIT ' + gl.SHOW_RECORDS
#         order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
#     else:
#         self.recordLimitEdt.setText(gl.SHOW_RECORDS)
#         limit_ = 'LIMIT 99999'
#     sql = select_ + where_ + join_ + order_ + limit_
#     gl.CURRENT_SQL = sql


def make_sql(command_dict):
    gl.CURRENT_SQL = ''
    select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.status_name,livros.pu_cota,livros.pu_volume," \
              " pu_ed_year, pu_edition, pu_volume_series,pu_volume_collection, pu_price,pu_copy_number FROM livros "
    join_ = ''' inner join authors on au_id=pu_author_id
                   inner join types on ty_id=livros.pu_type
                   inner join status on status_id=pu_status'''
    where_ = []
    order_by = ''
    limit = ''
    # try:
    if gl.SEARCH_DICT['LAST'] > 0:
        limit = ' limit ' + str(gl.SHOW_RECORDS)
        gl.SEARCH_DICT['ORDER'] = ''
        
    else:
        if gl.SEARCH_DICT['WHERE'] == 'author':
            if not command_dict['WHAT'] == '':
                text_to_search = "\'%" + command_dict['WHAT'].lower().strip() + "%\'"
                where_.append('''unaccent(lower(authors.au_name)) LIKE  unaccent(''' + text_to_search + ''')''')
        elif gl.SEARCH_DICT['WHERE'] == 'local':
            text_to_search = "\'" + command_dict['WHAT'].lower().strip() + "\'"
            where_.append('''(lower(pu_cota)) LIKE  ''' + text_to_search)
        
        elif gl.SEARCH_DICT['WHERE'] == 'title':
            text_to_search = "\'%" + command_dict['WHAT'].lower().strip() + "%\'"
            where_.append('''unaccent(lower(pu_title)) LIKE  unaccent(''' + text_to_search + ''') ''')
        elif gl.SEARCH_DICT['WHERE'] == 'isbn':
            text_to_search = "\'%" + command_dict['WHAT'].lower().strip() + "%\'"
            where_.append('''pu_isbn LIKE  ''' + text_to_search)
        elif gl.SEARCH_DICT['WHERE'] == 'tags_or':
            text_to_search = ''
            for n in gl.SEARCH_DICT['WHAT'].lower().split(','):
                text_to_search += '\'' + n + '\'' + ','
            text_to_search = text_to_search[:-1]
            where_.append("pu_id in (select tags_ref_book from tags_reference "
                          "where tags_ref_tag_id in (select ta_id from tags where ta_name in (" + text_to_search + ")))")
        """ generic filter  v1 """
        if gl.SEARCH_DICT['TYPE'] == '':
            pass
        else:
            where_.append(" livros.pu_type = (select ty_id from types where lower(ty_name) like \'" + gl.SEARCH_DICT['TYPE'].lower() + '\')')
        if gl.SEARCH_DICT['STATUS'] == '':
            pass
        else:
            where_.append(" livros.pu_status = (select status_id from status where lower(status_name) like \'" + gl.SEARCH_DICT['STATUS'].lower() + '\')')
    if gl.SEARCH_DICT['ORDER'] == '':
        order_by = ' order by pu_id DESC '
    else:
        order_by = ' order by ' + gl.SEARCH_DICT['ORDER'] + ' ' + gl.SEARCH_DICT['ORDER_BY']
    sql = select_ + join_ + create_sql_where(where_) + order_by + limit
    gl.CURRENT_SQL = sql
    print('DEBUG')
    print(sql)
    print('END DEBUG')

    return sql


# def make_sql_raw(records=50, update=False):
#     print('--------Debug---------')
#     print('make_sql_raw')
#     print('ABANDONAR')
#     print('------end debug-------')
#
#     gl.CURRENT_SQL = ''
#     select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.status_name,livros.pu_cota,livros.pu_volume, pu_ed_year, pu_cota_new FROM livros "
#     join_ = ''' inner join authors on au_id=pu_author_id
#                    inner join types on ty_id=livros.pu_type
#                    inner join status on status_id=pu_status'''
#     where_ = ''
#     if update:
#         order_ = ' order by pu_modified DESC limit ' + str(records)
#     else:
#         order_ = ' order by pu_id DESC limit ' + str(records)
#     sql = select_ + join_ + where_ + order_
#     gl.CURRENT_SQL = sql
#
#     return sql


def create_sql_where(input_list):
    output_sql = ''
    if len(input_list) > 0:
        output_sql = ' WHERE '
        output_sql += ' AND '.join(input_list)
    return output_sql


if __name__ == '__main__':
    pass
