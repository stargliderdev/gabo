#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import re
import parse_html

def clean_title(text_to_clean):
    toto = re.sub('[^0-9]', '', text_to_clean)
    return toto
    
def search_by_isbn(isbn_t):
    isbn_t = str(isbn_t)
    isbn_t = re.sub('[^0-9]', '', isbn_t)
    url = 'https://www.wook.pt/pesquisa/' + isbn_t
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
    except Exception as detail:
        print("Error in getBookDataISBN", detail)
        return False, 'Exception '
    return parse_html.parse_wook(url) # faz o parse da pagina em HTML

if __name__ == '__main__':
    pass
