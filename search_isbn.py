#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import re
import parse_html

def clean_title(text_to_clean):
    #toto = re.sub('[._\s]', '', text_to_clean)
    toto = re.sub('[^0-9]', '', text_to_clean)
    #toto = re.sub('\s{2,99}', '', toto)
    
    return toto
    
def search_by_isbn(isbn_t):
    isbn_t = str(isbn_t)
    isbn_t = re.sub('[^0-9]', '', isbn_t)
    url = 'https://www.wook.pt/pesquisa/' + isbn_t
    # print 'url',url

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
    except Exception as detail:
        print("Error in getBookDataISBN", detail)
        return (False, 'Exception ')
    

    return parse_html.parse_wook(url) # faz o parse da pagina em HTML

def main():
    print(search_by_isbn('9789720044334'))
    # pprint.pprint(params.book_data_dict)


if __name__ == '__main__':
    main()
