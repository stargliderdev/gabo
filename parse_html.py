# -*- coding: utf-8 -*-
import sys
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, time
from bs4 import BeautifulSoup
import string
import parameters as param


def parse_wook(url):
    book_data = {}
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        the_page = response.read() 
        #print the_page 
        
    except Exception as detail:
        print("Error in parseWook ", detail)
        book_data['pu_title']='Error in parseWok'
        book_data['pu_sinopse']=str(detail)

        return True, book_data

    
    soup = BeautifulSoup(the_page, "lxml")
    
    toto = soup.find('div', {'id': 'productPageSectionDetails-collapseDetalhes-content-title'})
    # bookData['pu_title']= get_data_wook(toto)
    book_data['pu_title'] = get_data_wook(toto)
    # print 'titulo:',titulo
    # bookData['pu_title'] = titulo[titulo.find('">')+2:titulo.rfind('</h1')]
    # print '------------------'
    toto = soup.find('div', {'id': 'productPageSectionDetails-collapseDetalhes-content-author'})
    # print 'Autor  ',get_autor(toto)
    book_data['pu_author'] = get_autor(toto)
    # print '------------------'
    # bookData['pu_title']
    # bookData['pu_author_id'] = get_data_wook(toto,';"', '</a').replace('>', '').strip()
    
    
    # toto = soup.find('div', {'class': 'tabbertab'}) #sinopse
    toto = soup.find('div', {'id': 'productPageSectionAboutBook-sinopse'})
    # print 'descricao', get_desc(toto)
    a = str(get_data_wook(toto,'cr"', '</di'))
    
    tag = 'itemprop="description"'
    p1 = a.find(tag) + len(tag)
    a = a.replace('<p>','')
    a = a.replace('</p>','')
    a = a.replace('<i>','')
    a = a.replace('</i>','')
    a = a.replace('<br>','')
    a = a.replace('\n','')
    a = a.replace('br/','')
    a = a.replace('<>','')
    a = a.replace('>','')
    book_data['pu_sinopse'] = a[p1:]
    
    cdata = soup.find('div', {'class': 'data'})
    book_data.update(get_data(cdata))

    return True, book_data

def get_data_wook(elemento,rightD = '">',  leftD = '</d'):
    elemento = str(elemento) 
    foo = elemento.find(rightD)
    foo1 = elemento.find(leftD)
    return elemento[foo+len(rightD):foo1]

def get_autor(a):
    a = str(a)
    b = a.rfind('">')+2
    c = a.rfind('</a>')
    return a[b:c]

def get_desc(a):
   
    a = str(a).encode('utf-8')
    b = a.rfind('">')
    c = a.rfind('</p')  
    a = a[b:c]
    hl = a.replace('<br />','')
    hl = hl.replace('</b>','')
    hl = hl.replace('<b>','')
    hl = hl.replace('<p>','')
    hl = hl.replace('>','')
    return hl


def get_img(a):
    a = str(a)
    b = a.find(' src="') + 6
    c = a.rfind('&amp')
    return a[b:c]


def get_data(a):
    hl = {}
    a = str(a)
    p1 = 0
    p2 = 0
    tag = 'itemprop="isbn">'
    p1 = a.find(tag)
    p2 = a.find('<',p1) #a[p1: len(tag)]
    # print(p1, p2, len(tag))
    # print(a[p1+len(tag): p2])
    hl['isbn'] = a[p1+len(tag): p2]
    p1 = p2
    tag = 'itemprop="datePublished">'
    p1= a.find(tag,p1)
    p2 = a.find('<', p1)
    hl['pu_ed_date'] = a[p1 + len(tag): p2]
    #
    p1 = p2
    tag = 'Editor: <span class="info" itemprop="name">'
    p1 = a.find(tag, p1) + len(tag)
    p2 = a.find('<', p1)
    hl['pu_editor'] = a[p1 : p2]
    #
    p1 = p2
    tag = 'Dimensões: <span class="info">'
    p1 = a.find(tag, p1) + len(tag)
    p2 = a.find('<', p1)
    hl['size'] =  a[p1: p2].strip().replace('mm','').replace(' ','')
    # 

    p1 = p2
    tag = 'Encadernação: <span class="info">'
    p1 = a.find(tag, p1) + len(tag)
    p2 = a.find('<', p1)
    hl['pu_pages'] = a[p1: p2]
    #
    p1 = p2
    tag = 'itemprop="numberOfPages">'
    p1 = a.find(tag, p1) + len(tag)
    p2 = a.find('<', p1)
    hl['pu_pages'] = a[p1: p2]
   
    return hl

def get_ano(a):
    return str(a)

def main():
    #'http://www.bertrand.pt/ficha/terra-abencoada?id=11462775'
    #'http://www.wook.pt/ficha/terra-abencoada/a/id/11462775'

    # parse_wook('https://www.wook.pt/pesquisa/9789723801965')
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(parse_wook('https://www.wook.pt/pesquisa/9789897225130'))

    
if __name__ == '__main__':
    main()
