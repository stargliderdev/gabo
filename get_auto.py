#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_autor_1(a):
    a = str(a)
    b = a.rfind('">') + 2
    c = a.rfind('</a>')
    return a[b:c]

def get_autor(a):
    a = a.replace('</a> e ',',')
    a = a.replace('&nbsp;</div>','')
    xl = a.split(',')
    bc = []
    for n in xl:
        p1 = n.find('<')
        p2 = n.find('>') + 1
        # print(n,p1, p2)
        x = (n[p2:]).replace('</a>','')
        bc.append(x)
    return ','.join(bc)
    

print(get_autor('de <a href="/autor/paulinho-assuncao/21889">Paulinho Assunção</a>, <a href="/autor/manuel-jorge-marmelo/2155451">Manuel Jorge Marmelo</a>, <a href="/autor/ondjaki/27161">Ondjaki</a> e <a href="/autor/ana-paula-tavares/21993">Ana Paula Tavares</a>&nbsp;</div>'))
print(get_autor('de <a href="/autor/paulinho-assuncao/21889">Paulinho Assunção</a>&nbsp;</div>'))

