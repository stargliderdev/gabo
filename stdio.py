#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime
import webbrowser
from random import randrange
from operator import itemgetter

def read_config_file(file_name):
    lines = []
    try:
        f = open(file_name, "r")
        try:
            lines = f.readlines()
        finally:
            f.close()
        conf_ini = ini_file_to_dic(lines)
        return conf_ini
    except IOError:
        print ('erro ao ler ini')
        return {}

def ini_file_to_dic(lines):
    dic = {}
    if not lines == []:
        for n in lines:
            dum = n.split('=')
            if len(dum) > 1:
                dic[dum[0]] = dum[1].strip('\n')
            else:
                dic[dum[0].strip('\n')] = None
        dic['error'] = False
    else:
        dic['error'] = True
    return dic

def read_file(file_name, mode=1):
    try:
        f = open(file_name, "r")
        try:
            if mode == 1:
                # lines into a list.
                toto = f.readlines()
            elif mode == 2:
                # Read the entire contents of a file at once.
                toto = f.read()
            elif mode == 3:
                # OR read one line at a time.
                toto = f.readline()
        finally:
            f.close()
    except IOError:
        toto = 'error ao carregar ficheiro:' + file_name
    return toto

def log_write(file_name, content):
    d = datetime.datetime.now().strftime("%Y.%b.%d %H:%M:%S")
    with open(file_name, "a") as myfile:
        myfile.write(d + ': ' + content + '\n')

def wipe(path):
    with open(path, 'wb') as fout:
        fout.write(os.urandom(randrange(1309, 7483)))

def int_format(number, sep=' '):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + sep.join(reversed(groups))

def float_format(number, sepi=' ', sepf=','):
    """ o dois é a precisão do numero flutuante """
    try:
        dum = str(number).split('.')
        # print dum
        toto = int_format(int(dum[0]), sepi) + sepf + dum[1][:2]
    except:
        return '0' + sepf + '00'
    return toto

def sort_files_by_last_modified(files):
    """ Given a list of files, return them sorted by the last
         modified times. """
    fileData = {}
    for fname in files:
        fileData[fname] = os.stat(fname).st_mtime
    
    fileData = sorted(list(fileData.items()), key=itemgetter(1))
    return fileData

def internet_on():
    try:
        response = urllib.request.urlopen('http://google.com', timeout=1)
        return True
    except urllib.error.URLError as err: pass
    return False

def delete_file(path, echo=False):
    if os.path.isfile(path):
        if echo:
            os.remove(path)

def file_ok(file):
    if os.path.exists(file):
        return True
    else:
        return False

def dir_ok(path, create=True):
    if os.path.isdir(path):
        pass
    else:
        if create:
            os.makedirs(path)

def last_file(path):
    files_by_date = sort_files_by_last_modified(path)
    if not files_by_date:
        toto = -1
    else:
        toto = files_by_date[0][0]
    return toto

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()

def zip_file(filename):
    import gzip
    dum = filename + '.gz'
    dum = dum[:dum.rfind('.xml')]
    f_in = open(filename, 'rb')
    f_out = gzip.open(filename + '.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    if not file_ok(dum + '.gz'):
        os.rename(filename + '.gz', dum + '.gz', )
    return dum + '.gz'

def make_file_name(db_name, drive):
    tdate = datetime.datetime.now().strftime("%Y-%m-%d-%Hh-%Mm")
    return drive + db_name + '_' + tdate + '.backup'

def clean_isbn(a):
    a = a.strip()
    a = a.strip(',')
    a = a.strip('-')
    try:
        a = int(a)
    except ValueError:
        a = -1
    
    return a

def authors_process(hl):
    hl = hl.replace('&', ',')
    hl = hl.replace(';', ',')
    hl = hl.replace(', ', ',')
    hl = hl.split(',')
    xl = ''
    for n in hl:
        a = n.title()
        a = a.strip()
        xl +=a +','
    xl = xl.rstrip(',')
    return xl

def postgresql(data_params):
    print ('--------Debug---------')
    print ('postgresql')
    print (data_params)
    print ('------end debug-------')
    backup_file = make_file_name(data_params['db_database'], data_params['backup_dir'] )
    print('Fazendo backup do Postgresql')
    print('Dest:',)
    exec_string = 'PGPASSWORD=\"' + data_params['db_password'] + '\"  pg_dump -h ' + data_params['db_host'] + ' -p 5432 -U root -Fc  -f ' \
                  + backup_file + ' ' + data_params['db_database']
    os.system(exec_string)

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def search_internet(txt):
    url = "https://www.google.com.tr/search?q={}".format(txt)
    # b = webbrowser.get('google-chrome')
    # b.open(url)
    webbrowser.open(url)
if __name__ == '__main__':
    pass