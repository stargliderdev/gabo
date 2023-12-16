#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import parameters as gl
import re
import os
import json
the_page = ''

def parse_wook(page_to_parse):
    global the_page
    gl.record_current_dict = {}
    gl.TAGS_SPECIAL_LEVEL1_DATA = []
    gl.TAGS_NORMAL_DATA = []
    the_page = page_to_parse
    the_page = " ".join(page_to_parse.split())
    try:
        os.remove(".\\tmp\\page.html")
    except FileNotFoundError:
        pass
    print(the_page.encode("utf-8"), file=open(".\\tmp\\page.html", "a"))
    # find SEO
    p0 = the_page.find('Google SEO Optimization -->')
    p1 = the_page.find('<!-- Fim Google SEO')
    google_seo_string = (the_page[p0:p1])
    p0 = google_seo_string.find('{')
    p1 = google_seo_string.rfind('}')
    google_seo_string = (google_seo_string[p0:p1+1])
    seo_dict = json.loads(google_seo_string)
    # for key, value in seo_dict.items():
    #     print(key, ' : ', value)
    
    try:
        gl.record_current_dict['pass'] = True
        # gl.record_current_dict['isbn'] = get_isbn('id="productPageSectionDetails-collapseDetalhes-content-isbn"') # old
        gl.record_current_dict['isbn'] = get_isbn()
        gl.record_current_dict['pu_title'] = get_tag_value('productPageRightSectionTop-title-h1">').strip()
        gl.record_current_dict['pu_sub_title'] = get_tag_value('id="productPageRightSectionTop-author-lnk"')
        gl.record_current_dict['pu_author'] = get_author('productPageRightSectionTop-authors-h3">de ')
        dum = get_tag_value('productPageRightSectionTop-subtitle-h2">')
        if dum.find('>') > -1:
            gl.record_current_dict['pu_sub_title'] = ''
        else:
            gl.record_current_dict['pu_sub_title'] = dum
        gl.record_current_dict['pu_ed_year'] = '0'
        # new version
        gl.record_current_dict['pu_edition_date'] = seo_dict['bookEdition']
        gl.record_current_dict['pu_publisher'] = seo_dict['publisher']['name']
        gl.record_current_dict['pu_dimensions'] = get_size()
        gl.record_current_dict['pu_language'] = get_language('Idioma:').strip()
        gl.record_current_dict['pu_cover'] = get_cover_type()
        try:
            gl.record_current_dict['pu_pages'] = str(seo_dict['numberOfPages'])
        except KeyError:
            gl.record_current_dict['pu_pages'] = '0'
        gl.TAGS_SPECIAL_LEVEL1_DATA.append(('TRAD', get_translator(), gl.tag_special_dict['TRAD']))
        gl.TAGS_NORMAL_DATA = get_arvore_tematica()
        try:
            if gl.year_as_date:
                try:
                    gl.record_current_dict['pu_ed_year'] = seo_dict['bookEdition'].split('-')[1]
                    # get_edition('id="productPageSectionDetails-collapseDetalhes-content-year"').split('-')[1]
                except IndexError:
                    gl.record_current_dict['pu_ed_year'] = '0'
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
            dum = ",".join(gl.TAGS_NORMAL_DATA)
            gl.record_current_dict['pu_tags'] += ',' + dum.lower()
            
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

# # def get_isbn_wook(isbn):
# #     xl = {}
#     xl = parse_wook('https://www.wook.pt/pesquisa/' + isbn)
#     xl = parse_wook('https://www.wook.pt/Afiliados')
#     # return xl

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

def get_isbn():
    import re
    tag = 'ISBN </span> <span class="info">'
    p0 = the_page.find(tag)
    a = the_page[p0 + len(tag):]
    p1 = a.find('</')
    dum = a[:p1]
    isbn = re.sub('\D', '', a[:p1])
    return isbn

def get_size():
    p1 = the_page.find('Dimensões:')
    a = the_page[p1 + len('Dimensões:'):]
    p1 = a.find('mm')
    a = a[:p1]
    a = a.replace(' </span> <span class="info">','')
    a = a.replace(' ','')
    a = a.replace('mm','')
    return a

def dimension_convert(dim_string):
    if dim_string.find('mm')>-1:
        dim_string = dim_string.replace('mm','')
        dim_string = dim_string.replace(' ','')
    elif dim_string.find('cm') >-1 :
        dim_string = dim_string.replace('cm','')
        dim_string = dim_string.replace(' ','')
        dum_list = dim_string.split('x')
        dim_string = str(int(float(dum_list[0]) * 10))
        dim_string = dim_string + 'x' + str(int(float(dum_list[1]) * 10))
        try:
            dim_string = dim_string + 'x' + str(int(float(dum_list[2]) * 10))
        except IndexError:
            dim_string = dim_string + 'x' + '00'
        dum_list = dim_string.split('x')
        if int(dum_list[2]) > int(dum_list[1]):
            dim_string = dum_list[0] + 'x' + dum_list[2] + 'x' + dum_list[1]
    elif dim_string.find('inches') >-1 :
        dim_string = dim_string.replace('inches','')
        dim_string = dim_string.replace(' ','')
        dum_list = dim_string.split('x')
        dim_string = str(int(float(dum_list[0]) * 2.54*10))
        dim_string = dim_string + 'x' + str(int(float(dum_list[1]) * 2.54*10))
        try:
            dim_string = dim_string + 'x' + str(int(float(dum_list[2]) * 2.54*10))
        except IndexError:
            dim_string = dim_string + 'x' + '00'
        dum_list = dim_string.split('x')
        if int(dum_list[2]) > int(dum_list[1]):
            dim_string = dum_list[0] + 'x' + dum_list[2] + 'x' + dum_list[1]
    else:
        dim_string = 'Erro!!!'
    return dim_string

 
def get_language(tag):
    p1 = the_page.find(tag)
    a = the_page[p1 + len(tag):]
    p1 = a.find('>')
    p2 = a.find('<', p1+1)
    return a[p1+1:p2]
    
def get_cover_type():
    p1 = the_page.find('Encadernação: ')
    a = the_page[p1 + len('Encadernação: '):]
    p1 = a.find('</span> </span>')
    a = a[:p1]
    a = a.replace('</span> <span class="info">','')
    return a

def get_translator():
    a = ''
    p1 = the_page.find('Tradução: ')
    if p1 > -1:
        a = the_page[p1 + len('Tradução: '):]
        p1 = a.find('</a>')
        a = a[:p1]
        a = a.replace('<a id="productPageRightSectionTop-entidade-lnk">','')
    return a

def get_collection():
    a = ''
    p1 = the_page.find('Coleção: ')
    if p1 > -1:
        a = the_page[p1 + len('Coleção: '):]
        p1 = a.find('</a>')
        a = a[:p1]
        a = a.replace('<a id="productPageRightSectionTop-entidade-lnk">','')
    return a

def get_arvore_tematica():
    page_org = the_page
    tree_list = []
    while True:
        p1 = page_org.rfind('arvoretematica')
        if p1 ==-1:
            break
        page_stack = page_org[:p1]
        text_to_process = page_org[p1:]
        p1 = text_to_process.find('</span')
        text_to_process = text_to_process[:p1]
        if text_to_process.find('title=') > -1:
            break
        page_org = page_stack
        tree_list.append(text_to_process[text_to_process.rfind('>')+1:])
    return tree_list
    
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


if __name__ == '__main__':
    print(dimension_convert('153 x 231 x 32 mm'))
    print(dimension_convert('18.44 x 0.64 x 25.07  cm'))
    print(dimension_convert('18.44 x 25.07x 0.64  cm'))
    print(dimension_convert('18.44 x 25.07  cm'))
    print(dimension_convert('8.5 x 0.65 x 11 inches'))