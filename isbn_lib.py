#!/usr/bin/python
# -*- coding: utf-8 -*-
import parameters as gl
import settings
import sqlite_crud


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
    # else:
    #     dim_string = 'Erro!!!'
    return dim_string


def text_title(txt):
    a = txt.title()
    a = a.split(' ')
    bc = [a[0]]
    for n in range(1,len(a)):
        if a[n].lower() in gl.WORDS_DICT:
            bc.append(gl.WORDS_DICT[a[n].lower()])
        else:
            bc.append(a[n])
    return ' '.join(bc)


if __name__ == '__main__':
    # settings.load_settings()
    # sqlite_crud.load_words()
    # print(gl.WORDS_DICT)
    # print(text_title('luisa de gusmão'))
    pass