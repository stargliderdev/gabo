import sys

import parameters as gl
import dmPostgreSQL as dbmain


def calc_width_in_filter():
    publication_ids = []
    xl = dbmain.query_many(gl.CURRENT_SQL)
    for n in xl:
        publication_ids.append(str(n[0]))
    dimentions = []
    for n in xl:
        sql = '''select ta_name, livros.pu_title
         from tag_ref
         left join livros on tag_ref.tr_book = livros.pu_id
         left  join tags on ta_id=tag_ref.tr_tag
        where livros.pu_id =''' + str(n[0]) + ''' and ta_name like \'dim:%\''''
        as_dim = dbmain.query_one_simple(sql)
        if as_dim is None:
            dimentions.append((n[0], n[1], n[2], n[5], n[6], n[7], ''))
        else:
            dimentions.append((n[0], n[1], n[2], n[5], n[6], n[7], as_dim[0].replace('dim:', '')))
    leng = 0
    max_width = 0
    max_height = 0
    missing = 0
    for n in dimentions:
        # print(n)
        if n[6] == '':
            missing += 1
        else:
            dum = n[6].replace('dim:', '')
            dum_list = dum.split('x')
            leng += int(dum_list[2])
            if int(dum_list[0]) > max_width:
                max_width = int(dum_list[0])
            if int(dum_list[1]) > max_height:
                max_height = int(dum_list[1])
    print('     largura:', leng/10.0)
    print('profundidade:', max_width/10.0)
    print('      altura:', max_height/10.0)
    print('      livros:', len(dimentions))
    print('  livros SEM:', missing)
    print('-' * 40)
    return dimentions


def make_sql(what='', where_index='nada', sort_by=''):
    gl.CURRENT_SQL = ''
    select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year FROM livros, authors, types, status"
    join_ = " livros.pu_status = status.st_id AND authors.au_id = livros.pu_author_id AND types.ty_id = livros.pu_type "
    where_ = ' WHERE '
    order_ = ''
    search_ = ''
    limit_ = ''
    where_index = where_index.lower()
    # self.key_sort = self.sort_dic[self.sortByCbox.currentText().lower()]
    if not what == '':
        self.recordLimitEdt.setText('0')
        # self.key_search = self.sort_dic[where_index]
        if where_index == 'local':  # na cota tem de ser exactamente igual
            self.key_search = self.sort_dic['local']
            text_to_search = "\'" + what.lower().strip() + "\'"
        else:
            text_to_search = "\'%" + what.lower().strip() + "%\'"
        
        if len(text_to_search) > 1:
            where_ += '''unaccent(lower(''' + self.key_search + ''')) LIKE  unaccent(''' + text_to_search + ''') AND '''
        else:
            where_ += ''' unaccent(upper(''' + self.key_search + ''')) SIMILAR TO ''' + '''unaccent(''' + text_to_search.upper() + ')' + ''' AND '''
    elif not self.tags_to_searchEdit.text() == '':  # modo para tags
        self.recordLimitEdt.setText('0')
        tags = self.tags_to_searchEdit.text().replace("\'", "\\\'")
        tags = tags.split(',')
        in_data = ''
        if self.logicTags.currentIndex() == 0:  # ou
            for n in tags:
                toto = n.lower().strip()
                in_data += "unaccent(\'" + toto + "\'),"
            a = dbmain.query_many(
                '''select ta_id from tags where unaccent(ta_name) in (''' + in_data[:-1] + ''')''')
            i = []
            for t in a:
                i.append(t[0])
            if i:
                i = str(i)
                where_ += '''
                     pu_id in(select * from (select tr_book from tag_ref where tr_tag in(''' + i[
                                                                                               1:-1] + ''')) as foo) AND '''
            else:
                where_ += '''pu_id in(select * from (select tr_book from tag_ref where tr_tag in(-1)) as foo) AND '''
        else:
            t = ''
            for n in tags:
                t = t + "\'" + n.strip() + "\',"
            t = t[:-1]
            c = str(len(tags))
            where_ = ''' where EXISTS (SELECT NULL
             FROM tag_ref tg
             JOIN TAGS t ON t.ta_id = tg.tr_tag
            WHERE unaccent(t.ta_name) IN (unaccent(''' + t + '''))
              AND tg.tr_book = livros.pu_id
         GROUP BY tg.tr_book
           HAVING COUNT(t.ta_name) =''' + c + ''') and '''
    else:  # não procura em nada
        where_ += ''' livros.pu_status = status.st_id AND
      authors.au_id = livros.pu_author_id AND
      types.ty_id = livros.pu_type and '''
        self.key_sort = self.sort_dic[self.sortByCbox.currentText().lower()]
    
    if self.typesCbox.currentIndex() != 0:
        where_ += " livros.pu_type = (select ty_id from types where ty_name like \'" + str(
            self.typesCbox.currentText()) + '\') and '
    
    if self.statusCbox.currentIndex() != 0:
        where_ += " livros.pu_status = (select st_id from status where st_nome like \'" + str(
            self.statusCbox.currentText()) + "\') and "
    
    order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
    
    if int(gl.SHOW_RECORDS) > 0:  # int(self.recordLimitEdt.text()) > 0:
        limit_ = 'LIMIT ' + gl.SHOW_RECORDS
        order_ = ''' ORDER BY ''' + self.key_sort + ' asc '
    else:
        self.recordLimitEdt.setText(gl.SHOW_RECORDS)
        limit_ = 'LIMIT 99999'
    sql = select_ + where_ + join_ + order_ + limit_
    gl.CURRENT_SQL = sql


def make_sql_author(what='', order_by='nada', pub_type='todos', pub_status='todos'):
    gl.CURRENT_SQL = ''
    # select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year FROM livros "
    # join_ = '''inner join authors on au_id=pu_author_id
    #            inner join types on ty_id=pu_type
    #            inner join status on st_id=pu_status'''
    # where_ = []
    # order_ = ''
    # if not what == '':
    #     text_to_search = "\'%" + what.lower().strip() + "%\'"
    #     if len(text_to_search) > 1:
    #         where_.append('''unaccent(lower(authors.au_name)) LIKE  unaccent(''' + text_to_search + ''')''')
    # if pub_type == 'todos':
    #     pass
    # else:
    #     where_.append(
    #         ''' livros.pu_type = (select ty_id from types where lower(ty_name) like \'''' + pub_type.lower() + '''\')''')
    # if pub_status == 'todos':
    #     pass
    # else:
    #     where_.append(" livros.pu_status = (select st_id from status where lower(st_nome) like \'" + pub_status + '\')')
    # where_ = create_sql_where(where_)
    #
    # order_ = '' #''' ORDER BY ''' + gl.sort_dic[order_by.lower()] + ' asc '
    # sql = select_ + join_ +  + order_
    # gl.CURRENT_SQL = sql
    sql = ''
    return sql


def make_sql_local(what='', order_by='nada', pub_type='todos', pub_status='todos'):
    gl.CURRENT_SQL = ''
    select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year FROM livros "
    join_ = '''inner join authors on au_id=pu_author_id
               inner join types on ty_id=pu_type
               inner join status on st_id=pu_status'''
    where_ = []
    order_ = ''
    if not what == '':
        # self.key_search = self.sort_dic['local']
        # text_to_search = "\'" + what.lower().strip() + "\'"
        
        
        text_to_search = "\'" + what.lower().strip() + "\'"
        if len(text_to_search) > 1:
            where_.append('''(lower(pu_cota)) LIKE  ''' + text_to_search )
    if pub_type == 'todos':
        pass
    else:
        where_.append(
            ''' livros.pu_type = (select ty_id from types where lower(ty_name) like \'''' + pub_type.lower() + '''\')''')
    if pub_status == 'todos':
        pass
    else:
        where_.append(" livros.pu_status = (select st_id from status where lower(st_nome) like \'" + pub_status + '\')')
    where_ = create_sql_where(where_)
    
    order_ = ''' ORDER BY ''' + gl.sort_dic[order_by.lower()] + ' asc '
    sql = select_ + join_ + where_ + order_
    gl.CURRENT_SQL = sql
    return sql

def make_sql(command_dict):
    print(command_dict)
    gl.CURRENT_SQL = ''
    select_ = "SELECT livros.pu_id, livros.pu_title, authors.au_name, types.ty_name, status.st_nome,livros.pu_cota,livros.pu_volume, pu_ed_year FROM livros "
    join_ = ''' inner join authors on au_id=pu_author_id
                   inner join types on ty_id=pu_type
                   inner join status on st_id=pu_status'''
    where_ = []
    order_ = ''
    if command_dict['WHERE'] == 'author':
        if not command_dict['WHAT'] == '':
            text_to_search = "\'%" + command_dict['WHAT'].lower().strip() + "%\'"
            where_.append('''unaccent(lower(authors.au_name)) LIKE  unaccent(''' + text_to_search + ''')''')
    elif command_dict['WHERE'] == 'local':
        text_to_search = "\'" + command_dict['WHAT'].lower().strip() + "\'"
        where_.append('''(lower(pu_cota)) LIKE  ''' + text_to_search )
    """ generic filter """
    try:
        where_.append(" livros.pu_type = (select ty_id from types where lower(ty_name) like \'" + command_dict['TYPE'].lower() + '\')')
    except KeyError:
        pass
    try:
        order_ = ''' ORDER BY ''' + gl.sort_dic[command_dict['ORDER'].lower()] + ' asc '
    except KeyError:
        pass
    try:
        where_.append(" livros.pu_status = (select st_id from status where lower(st_nome) like \'" + command_dict['STATUS'] + '\')')
    except KeyError:
        pass
    sql = select_ + join_ + create_sql_where(where_) + order_
    gl.CURRENT_SQL = sql
    return sql
    
def create_sql_where(input_list):
    output_sql = ' WHERE '
    output_sql += ' AND '.join(input_list)
    return output_sql


if __name__ == '__main__':
   pass