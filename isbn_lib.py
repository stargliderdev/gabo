#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import parameters as gl

def get_isbn_wook(isbn):
    xl = {}
    # xl = parse_wook('https://www.wook.pt/pesquisa/' + isbn)
    xl = parse_wook('https://www.wook.pt/Afiliados')
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

def get_isbn(tag):
    p0 = the_page.find(tag)
    a = the_page[p0 + len(tag):]
    p1 = a.find('>')
    p1 = a.find('>', p1+1)
    p2 = a.find('<', p1+1)
    isbn = a[p1 + 1:p2].replace('-','')
    return isbn.replace(' ','')
    
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


def parse_wook(pag):
    global the_page
    the_page = pag
    gl.record_current_dict = {}
    gl.tags_special_level1_data = []
    try:
        gl.record_current_dict['pass'] = True
        gl.record_current_dict['isbn'] = get_isbn('id="productPageSectionDetails-collapseDetalhes-content-isbn"')
        gl.record_current_dict['pu_title'] = get_tag_value('productPageRightSectionTop-title-h1">')
        gl.record_current_dict['pu_sub_title'] = get_tag_value('id="productPageRightSectionTop-author-lnk"')
        gl.record_current_dict['pu_author'] = get_author('productPageRightSectionTop-authors-h3">de ')
        dum = get_tag_value('productPageRightSectionTop-subtitle-h2">')
        if dum.find('>') > -1:
            gl.record_current_dict['pu_sub_title'] = ''
        else:
            gl.record_current_dict['pu_sub_title'] = dum
        gl.record_current_dict['pu_ed_year'] = '0'
        gl.tags_special_level1_data.append(('DATA', get_edition('id="productPageSectionDetails-collapseDetalhes-content-year"'),gl.tag_special_dict['DATA']))
        gl.tags_special_level1_data.append(('ED', get_editor('Editor:'),gl.tag_special_dict['ED']))
        gl.tags_special_level1_data.append(('DIM',get_size('Dimensões:'),gl.tag_special_dict['DIM']))
        gl.tags_special_level1_data.append(('LANG', get_language('Idioma:').strip(),gl.tag_special_dict['LANG']))
        gl.tags_special_level1_data.append(('COVER',get_value('Encadernação'),gl.tag_special_dict['COVER']))
        gl.tags_special_level1_data.append(('PAG', get_value('Páginas'),gl.tag_special_dict['PAG']))
        if gl.add_isbn:
            gl.tags_special_level1_data.append(('ISBN13', gl.record_current_dict['isbn'],gl.tag_special_dict['ISBN13']))
        # special_tags.append(('GEN',get_value('Temática').strip()))
        try:
            if gl.year_as_date:
                gl.record_current_dict['pu_ed_year'] = get_edition('id="productPageSectionDetails-collapseDetalhes-content-year"').split('-')[1]
            else:
                gl.record_current_dict['pu_ed_year'] = '0'
            gl.record_current_dict['pu_sinopse'] = get_sinopse('productPageSectionAboutBook-sinopse')
            if gl.add_author_as_label:
                gl.record_current_dict['pu_tags'] = gl.record_current_dict['pu_author']
            else:
                gl.record_current_dict['pu_tags'] = ''
            
            if gl.smart_title:
                gl.record_current_dict['pu_title'] = text_title(gl.record_current_dict['pu_title'])
                gl.record_current_dict['pu_sub_title'] = text_title(gl.record_current_dict['pu_sub_title'])
            elif gl.capitalize_title:
                gl.record_current_dict['pu_title'] = gl.record_current_dict['pu_title'].title()
            if gl.title_in_upper:
                gl.record_current_dict['pu_title'] = gl.record_current_dict['pu_title'].upper()
            if gl.author_surname_title:
                gl.record_current_dict['pu_author'] = autor_forename(gl.record_current_dict['pu_author'], False)
            elif gl.author_surname:
                gl.record_current_dict['pu_author'] = autor_forename(gl.record_current_dict['pu_author'])
            # book_data['special_tags'] = special_tags
        except IndexError:
            gl.record_current_dict['pass'] = False

    except urllib.error.HTTPError as e:
        gl.record_current_dict['pass'] = False
        gl.record_current_dict['error'] = sys.exc_info()[0]
        print(sys.exc_info()[0])
        print('--------Debug---------')
        print('parse_wook')
        print('URL')
        print(e)
        print('------end debug-------')
        
        sys.exit(99)
        
    if not gl.record_current_dict['pu_author']:
        return False
    return True

def autor_forename(a, caps=True):
    bc = a.split(',')
    xl = ''
    for f in bc:
        b = f.split()
        e = b[-1] + ', '
        if caps:
            e = e.upper()
        for n in range(len(b)-1):
            e = e + b[n] + ' '
        xl = xl + e + ';'
    xl = xl.replace(' ;', ';')
    return xl[:-1]


# def get_isbn_search(pag):
#     global the_page
#
#     the_page = pag
#     book_data = {}
#     # url ='https://isbnsearch.org/isbn/' + isbn
#     try:
#         req = urllib.request.Request(url)
#         response = urllib.request.urlopen(req)
#         the_page = response.read().decode('utf-8')
#         book_data['pass'] = True
#         print(get_tag_value('''<div class="bookinfo">'''))
#
#     except:
#         book_data['pass'] = False
#         book_data['error'] = sys.exc_info()[0]
#         print(sys.exc_info()[0])
#         sys.exit(99)
#
#     if not book_data['pu_author']:
#         book_data['pass'] = False
#     return book_data



if __name__ == '__main__':
    print(get_isbn_search('0078812321'))