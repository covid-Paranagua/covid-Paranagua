#!/usr/bin/python3

import pandas
from pathlib import Path
import re

def parse_Date(name : str):
    trim = ''.join(name.split(' '))
    date = re.search(r'(\d+-\d+-\d+)', trim)
    try:
        return date[0]
    except:
        # CORONAVIRUS.pdf is one exception
        if name == 'CORONAVÍRUS.pdf\n':
            return '14-07-2020'
        else:
            # jpg files
            return ''

if not Path('../public/order.txt').is_file():
    print('Error: check_csv_healthy: downloaded file list "order.txt" not exist. Did you run parse_paranagua_pdf.py?') # insert boletim_Paranaguá/ before script name, cite the checkout of files from data branch
    exit()

report = []
with open('../public/order.txt') as pdfs:
    for pdf_file_name in pdfs:
        length = len(pdf_file_name)
        base_name = pdf_file_name[:length-5]
        csv_names = ['../public/' + base_name + 't{}.csv'.format(index) for index in range(1,5)]
        dtypes= [{'Bairro': 'string', 'Feminino': 'Int64', 'Masculino': 'Int64', 'Total': 'Int64'},
                 {'Aguardando Resultados': 'string', 'Descartados': 'string', 'Recuperados': 'string'},
                 {'Bairro': 'string', 'Idade': 'Int64', 'Sexo': 'string'},
                 {'Confirmados': 'Int64', 'Bairro': 'string', 'Idade': 'Int64', 'Sexo': 'string'}]
        day = [False]*4
        for i in range(4):
            csv = csv_names[i]
            if Path(csv).is_file():
                try:
                    data = pandas.read_csv(csv, dtype=dtypes[i])
                    day[i] = True
                except:
                    pass
        if day == [True]*4:
            print(pdf_file_name[0:-1] + ': correctly parsed')
        else:
            print('{}: [{}, {}, {}, {}]'.format(pdf_file_name[0:-1], day[0], day[1], day[2], day[3]))
        date = parse_Date(pdf_file_name)
        line = [date, pdf_file_name, day[0], day[1], day[2], day[3]]
        report.append(line)

df = pandas.DataFrame(report, columns=['date', 'file_name', 't1', 't2', 't3', 't4'])
df.to_json('../public/report.json', orient='index')

from zipfile import ZipFile

with ZipFile('../public/CSVs.zip', 'w') as zip_file:
    for i in range(df.shape[0]):
        line = df.iloc[i]
        csv_file = '../public/' + line[1][:-5] + 't{}.csv'
        for j in range(1, 5):
            if line[j+1] == True:
                zip_file.write(csv_file.format(j))
