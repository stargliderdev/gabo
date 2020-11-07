#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import parameters as gl

def get_isbn_wook(isbn):
    xl = {}
    xl = parse_wook('https://www.wook.pt/pesquisa/' + isbn)
    return xl

def get_tag_value(tag):
    p0 = the_page.find(tag)
    p1 = p0 + len(tag)
    p2 = the_page.find('<', p1)
    return the_page[p1:p2]
    
def get_author(tag):
    p0 = the_page.find(tag) + len(tag)
    p1 = the_page.find('</h3>')
    if p1 == -1:
        return '\n'
    else:
        a = autor_more_one(the_page[p0:p1+1])
        return a[:a.find(';')] # tira se houver o tradutor

def autor_more_one(a):
    p0 = a.find('</a> e ')
    if p0> 0: # tem varios autores
        a = a.replace('</a> e ',',')
        a = a.replace('&nbsp;','')
        a = a.replace('</div>','')
        xl = a.split(',')
        bc = []
        for n in xl:
            p1 = n.find('<')
            p2 = n.find('>') + 1
            x = (n[p2:]).replace('</a>','')
            bc.append(x)
        return ','.join(bc).strip()
    else:
        p0 = a.find('>') + 1
        a = a[p0:]
        a = a.replace('&nbsp;', '')
        a = a.replace('</a>', '')
        return a
        
def get_edition(tag):
    p0 = the_page.find(tag)
    a = the_page[p0 + len(tag):]
    p1 = a.find('>')
    p1 = a.find('>', p1+1)
    p2 = a.find('<', p1+1)
    return a[p1+1:p2]

def get_editor(tag):
    p1 = the_page.find(tag)
    a = the_page[p1 + len(tag):]
    p1 = a.find('>')
    p2 = a.find('<', p1+1)
    return a[p1+1:p2]
    
def get_size(tag):
    p1 = the_page.find(tag)
    a = the_page[p1 + len(tag):]
    p1 = a.find('>')
    p2 = a.find('<', p1+1)
    a = a[p1+1:p2]
    a = a.replace(' ','')
    a = a.replace('mm','')
    return a
    
def get_language(tag):
    p1 = the_page.find(tag)
    a = the_page[p1 + len(tag):]
    p1 = a.find('>')
    p2 = a.find('<', p1+1)
    return a[p1+1:p2]
    
def get_value(tag):
    p1 = the_page.find(tag)
    a = the_page[p1 + len(tag):]
    p1 = a.find('>')
    p2 = a.find('<', p1+1)
    return a[p1+1:p2]
    
def get_sinopse(tag):
    p1 = the_page.find(tag)
    if p1 > 0:
        a = the_page[p1 + len(tag):]
        p1 = a.find('<p>')
        p2 = a.find('</p></div>', p1 +3)
        a = a[p1 + 3 :p2]
        a = a.replace('<br/><br/>','')
        a = a.replace('</i>','')
        a = a.replace('<i>','')
        a = a.replace('</b>','')
        a = a.replace('<br>','')
        a = a.replace('<b>','')
        return a
    else:
        return 'sem sinopse'

def text_title(txt):
    a = txt.title()
    a = a.split(' ')
    bc = [a[0]]
    for n in range(1,len(a)):
        if a[n].lower() in gl.prep_dict:
            bc.append(gl.prep_dict[a[n].lower()])
        else:
            bc.append(a[n])
    return ' '.join(bc)


def parse_wook(url):
    global the_page
    book_data = {}
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        the_page = response.read().decode('utf-8')
        book_data['pass'] = True
        book_data['pu_title'] = get_tag_value('productPageRightSectionTop-title-h1">')
        book_data['pu_author'] = get_author('productPageRightSectionTop-authors-h3">de ')
        book_data['pu_sub_title'] = get_tag_value('productPageRightSectionTop-subtitle-h2">')
        book_data['pu_ed_date'] = get_edition('id="productPageSectionDetails-collapseDetalhes-content-year"')
        book_data['pu_editor'] = get_editor('Editor:')
        book_data['pu_size']  = get_size('Dimensões:')
        book_data['pu_lang'] = get_language('Idioma:').strip()
        book_data['pu_media']  = get_value('Encadernação')
        book_data['pu_pages']  = get_value('Páginas')
        book_data['pu_theme'] = get_value('Temática')
        book_data['pu_sinopse'] = get_sinopse('productPageSectionAboutBook-sinopse')
        if book_data['pu_author'] == '\n':
            book_data['pass'] = False
    except:
        book_data['pass'] = False
        book_data['error'] = sys.exc_info()[0]
        print(sys.exc_info()[0])
        sys.exit(99)
        
    if not book_data['pu_author']:
        book_data['pass'] = False
    return book_data

def get_isbn_search(isbn):
    global the_page
    book_data = {}
    url ='https://isbnsearch.org/isbn/' + isbn
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        the_page = response.read().decode('utf-8')
        book_data['pass'] = True
        print(get_tag_value('''<div class="bookinfo">'''))

    except:
        book_data['pass'] = False
        book_data['error'] = sys.exc_info()[0]
        print(sys.exc_info()[0])
        sys.exit(99)
    
    if not book_data['pu_author']:
        book_data['pass'] = False
    return book_data

if __name__ == '__main__':
    
    print(get_isbn_search('0078812321'))