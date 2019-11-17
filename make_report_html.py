#!/usr/bin/python
# -*- coding: utf-8 -*-

def main_grid_report(hl):
    html = '''<!DOCTYPE html><html lang="pt_pt"><head><meta charset="utf-8">
                <style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 3px;
}

tr:nth-child(even) {
    background-color: #dddddd;
    border: 1px solid #000000;
}
</style>
</head>
<body> </style> '''
    html += '''
        <table width="900" align="center">
        <th width="40">ID</th>
        '''
    
    if len(hl) > 0:
        for n in hl:
            html += '''<tr class="cores">'''
            html += '''<td id="linha_encP" align="right">''' + str(n[0]) + '</td>\n'
            html += '''<td id="linha_encP" align="left">''' + str(n[1]) + '</td>\n'
            html += '''<td id="linha_encP" align="left">''' + str(n[2]) + '</td>\n'
            html += '''<td id="linha_encP" align="left">''' + str(n[3]) + '</td>\n'
            html += '''<td id="linha_encP" align="left">''' + str(n[4]) + '</td>\n'
            html += '''<td id="linha_encP" align="left">''' + str(n[5]) + '</td>\n'
            html += '''<td id="linha_encP" align="right">''' + str(n[6]) + '</td>\n'
            html += '''<td id="linha_encP" align="right">''' + str(n[7]) + '</td>\n'
            html += '</tr>\n'
        html += '</table>'
    # print(html, file=open("output.html", "a"))
    return html

if __name__ == '__main__':
    print('não corre')

