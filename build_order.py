#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
import dmPostgreSQL as dbmain
import stdio
import parameters as gl

def simple_table():
    pdfmetrics.registerFont(TTFont('calibri',"calibri.ttf"))
    pdfmetrics.registerFont(TTFont('calibrib',"calibrib.ttf"))
    # and
    # unaccent(lower(authors.au_name))
    # LIKE
    # unaccent('%varios%')
    data = dbmain.query_many('''SELECT livros.pu_id, left(livros.pu_title, 80), left(authors.au_name, 40),
    left(types.ty_name, 3), left(status.st_nome,5),livros.pu_cota,livros.pu_volume, pu_ed_year
    FROM livros, authors, status, types
     where authors.au_id=livros.pu_author_id and
      types.ty_id= livros.pu_type and
      status.st_id= livros.pu_status
    AND  livros.pu_status = status.st_id AND authors.au_id = livros.pu_author_id
    AND types.ty_id = livros.pu_type
    and  types.ty_id not in(7,8,9,10,11)
           ORDER BY livros.pu_title asc LIMIT 99999 ''')
    # '%charlier,giraud%'
    doc = SimpleDocTemplate("simple_table.pdf", pagesize=A4,rightMargin=72,
                            leftMargin=62,
                            topMargin=30,
                            bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []
    text = "<font face=calibri size=8>cabeçalho</font>"
    para = Paragraph(text, style=styles["Normal"])
    story.append(para)
    cnt = 1
    page_count = 1
    PAGE_BREAK = 75
    back_color = colors.lightgrey
    for n in data:
        
        # a = [n]
        # print(a)
        if cnt & 1:
            back_color = colors.lightgrey
        else:
            back_color = colors.white
        tblstyle = TableStyle([('ROWBACKGROUNDS', (0, 0), (-1, -1), [back_color, colors.green]),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('FONT', (0, 0), (-1, -1), 'calibri', 8),
                               ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                               ('ALIGN', (1, 0), (5, -1), 'LEFT'),
                               ('ALIGN', (6, 0), (6, -1), 'RIGHT'),
                               ('ALIGN', (7, 0), (7, -1), 'RIGHT')])
        
        tbl = Table([n],colWidths=[30,260,150,20,30,50,20,20], rowHeights=[10 for x in range(len([n]))])
        if PAGE_BREAK == cnt:
            story.append(tbl)
            tbl.setStyle(tblstyle)
            para = Paragraph("<font face=calibri size=8>Página " + str(page_count) + "</font>", style=styles["Normal"])
            story.append(para)
            text = "<font face=calibri size=8>Livros"  + "</font>"
            cnt = 1
            para = Paragraph(text, style=styles["Normal"])
            story.append(para)
            page_count +=1
        else:
            story.append(tbl)
            tbl.setStyle(tblstyle)
            cnt += 1
    story.append(para)
    doc.build(story)

if __name__ == '__main__':
    gl.db_params = stdio.read_config_file('livros.ini')
    gl.db_params = gl.db_params[1]
    gl.conn_string = "host=" + gl.db_params['db_host'] + ' port=' + gl.db_params['db_port'] + ' dbname=' + \
                     gl.db_params['db_database'] + ' user=' + gl.db_params['db_user'] + ' password=' + gl.db_params['db_password']
    simple_table()