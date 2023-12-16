import os
import sqlite3

import parameters as gl
import settings


def execute_query(sql, data=None):
    try:
        conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
        cursor = conn.cursor()
        if data is None:
            cursor.execute(sql)
        elif type(data) is str:
            cursor.execute(sql, (data,))
        else:
            cursor.execute(sql, data)
        conn.commit()
    except Exception as e:
        print("An exception occurred:", e)
        print('EXECUTE QUERY ', sql)
        print('DATA', data)
        print('\nEND DUMP')
        exit(2)


def record_to_dict(sql):
    conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
    cursor = conn.cursor()
    query = sql
    cursor.execute(query)

    # Fetch all the records
    records = cursor.fetchall()

    # Convert records to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    record_dicts = [dict(zip(columns, record)) for record in records]

    # Close the connection
    conn.close()


def query_many(sql, data=None):
    xl = []
    try:
        conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
        if data is None:
            cur = conn.execute(sql)
        elif type(data) is str:
            cur = conn.execute(sql, (data,))
        else:
            cur = conn.execute(sql, data)
        for n in cur:
            xl.append(n)
        conn.close()
    except Exception as e:
        print(e, '\n SQL-> ' + sql, '\n DATA '
                                    '\n *** query_main ***')
        print('exit')
        exit()
    return xl

def query_one(sql, data=None):
    xl = []
    try:
        conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
        if data is None:
            cur = conn.execute(sql)
            xl = cur.fetchone()
        else:
            cur = conn.execute(sql, data)
            xl = cur.fetchone()
        conn.close()
    except Exception as e:
        print(e, '\n SQL-> ' + sql, '\n DATA '
                                    '\n *** query_main ***')
        print('exit')
        exit()
    return xl

def get_book_data(index):
    conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE, uri=True)
    cursor = conn.cursor()
    sql = '''SELECT *
        FROM books
        WHERE pu_id = ?
        order by pu_id;'''
    cursor.execute(sql, (index,))
    records = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    record_dicts = [dict(zip(columns, record)) for record in records]
    conn.close()

    # for key, value in record_dicts[0].items():
    #     print(f"  {key}: {value}")
    gl.record_current_dict = record_dicts[0]
    return True


def get_authors():
    a = query_many('select au_name from authors order by au_name asc')
    gl.dsAutores = ['Varios']
    gl.autores_dict = {}
    for n in a:
        gl.autores_dict[n[0].lower()] = n[0]
        gl.dsAutores.append(n[0])


def get_types():
    a = query_many('select ty_name, ty_order from types order by ty_order  ')
    gl.types_dict = {}
    gl.types_list = []
    gl.types_tuple = []
    gl.TYPES_FILTER_LIST = ['Todos']
    for n in a:
        gl.types_dict[n[0].lower()] = n[0]
        gl.types_list.append(n[0])
        gl.TYPES_FILTER_LIST.append(n[0])
        gl.types_tuple.append(n)


def get_status():
    a = query_many('select status_name,status_order from status order by status_order')
    gl.status_list = []
    gl.STATUS_FILTER_LIST = ['Todos']
    gl.status_tuple = []
    for n in a:
        gl.status_list.append(n[0])
        gl.status_tuple.append(n)
        gl.STATUS_FILTER_LIST.append(n[0])


def get_locals():
    a = query_many('select local_id,local_name from locals')
    gl.locals_list = []
    gl.locals_dict = {}
    for n in a:
        gl.locals_list.append(n[1])


def get_conditions():
    a = query_many('select condition_name, condition_order from conditions order by condition_order')
    gl.conditions_list = []
    gl.conditions_dict = {}
    gl.conditions_tuple = []
    for n in a:
        gl.conditions_list.append(n[0])
        gl.conditions_tuple.append(n)


def get_sources():
    a = query_many('select  pu_source from books where pu_source is not null  group by pu_source order by pu_source')
    gl.sources_tuple = []
    for n in a:
        gl.sources_tuple.append(n)


def get_publishers():
    a = query_many(
        'select  pu_publisher from books where pu_publisher is not null  group by pu_publisher order by pu_publisher')
    gl.publishers_tuple = []
    for n in a:
        gl.publishers_tuple.append(n)


def get_collections():
    a = query_many(
        '''select  pu_collection from books where pu_collection is not null  group by pu_collection order by pu_collection''')
    gl.collections_tuple = []
    for n in a:
        gl.collections_tuple.append(n)


def get_series():
    a = query_many(
        'select  pu_serie from books where pu_serie is not null  group by pu_serie order by pu_serie')
    gl.series_tuple = []
    for n in a:
        gl.series_tuple.append(n)


def get_classifications():
    a = query_many(
        'select classification_name, classification_order from classifications order by classification_order')
    gl.classifications_list = []
    gl.classifications_dict = {}
    gl.classifications_tuple = []
    for n in a:
        gl.classifications_list.append(n[0])
        gl.classifications_tuple.append(n)


def get_languages():
    a = query_many('select language_name, language_order from languages order by language_order')
    gl.languages_list = []
    gl.languages_dict = {}
    gl.languages_tuple = []
    for n in a:
        gl.languages_list.append(n[0])
        gl.languages_tuple.append(n)


def get_covers():
    a = query_many('select cover_name,cover_order from covers order by cover_order')
    gl.covers_list = []
    gl.covers_tuple = []
    for n in a:
        gl.covers_list.append(n[0])
        gl.covers_tuple.append(n)


def load_words():
    a = query_many('select word_value from words')
    gl.WORDS_DICT = {}
    for n in a:
        gl.WORDS_DICT[n[0].lower()] = n[0]


def update_datasets():
    get_authors()
    get_status()
    get_types()
    load_words()
    get_locals()
    get_conditions()
    get_classifications()
    get_languages()
    get_covers()
    # get_areas()
    # get_special_tags()
    # load_parameters()
    # print('ending loading datasets!')


def load_parameters():

    sql = 'select * from params'
    a = []
    try:
        conn = sqlite3.connect(gl.DB_PATH + gl.DB_FILE)
        cur = conn.execute(sql)
        for n in cur:
            a.append(n)
        conn.close()
        NO_TABLES = False

    except Exception as e:
        NO_TABLES = True

    if NO_TABLES == True:
        print('Create DATABASE')
        gl.DB_VERSION = 0
        # database_init.create_database()
    else:
        for n in a:
            if n[0] == 'LAST_TAGS':
                toto = n[1].rstrip('|')
                dum = toto.split('|')
                for f in dum:
                    gl.last_tags.append(f)
                gl.last_tags = gl.last_tags[: len(gl.last_tags) - (len(gl.last_tags) - 10)]
            elif n[0] == 'SHOW_RECORDS':
                gl.SHOW_RECORDS = n[1]
            elif n[0] == 'OWNER':
                gl.OWNER = n[1]
            elif n[0] == 'LAST_STATUS':
                gl.LAST_STATUS = n[1]
            elif n[0] == 'LAST_BINDING':
                gl.LAST_BINDING = n[1]
            elif n[0] == 'LAST_LANGUAGE':
                gl.LAST_LANGUAGE = n[1]
            elif n[0] == 'LAST_PUB_TYPE':
                gl.LAST_PUB_TYPE = n[1]
            elif n[0] == 'GRID_COLUMN_SIZES':
                gl.GRID_COLUMN_SIZES = eval(n[1])
            elif n[0] == 'DB_VERSION':
                gl.DB_VERSION = int(n[1])
            elif n[0] == 'BIN_VERSION':
                gl.BIN_VERSION = int(n[1])



def save_parameters(k_name, k_data):
    execute_query('update params set param_data=? where param_key=?', (k_data, k_name))


def check_alive():
    if os.path.exists(gl.DB_PATH + gl.DB_FILE):
        # print(f"The file '{gl.DB_PATH + gl.DB_FILE}' exists.")
        load_parameters()
        return True
    else:
        # print(f"The file '{gl.DB_PATH + gl.DB_FILE}' does not exist.")
        # database_init.create_database()
        return False


def find_duplicate(table, field, data):
    data = data.lower()
    try:
        # conn = psycopg2.connect(pa.conn_string)
        # cur = conn.cursor()
        # conn.set_client_encoding('UTF8')
        # cur.execute('select * from ' + table + ' where ' + field + '=\'' + data + '\'')
        # xl = cur.fetchall()
        # cur.close()
        # conn.close()
        xl = query_many('''select * from ''' + table + ''' where lower(''' + field + ''')=\'''' + data + '''\'''')
        if xl == []:
            return False
        else:
            return True

    except Exception as e:
        print('ERRO', str(e))
        return True


if __name__ == '__main__':
    settings.load_settings()
    # check_alive()
    # get_authors()
    print(find_duplicate('types', 'ty_name', 'Poesia'))
