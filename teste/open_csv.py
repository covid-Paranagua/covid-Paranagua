##!/usr/bin/python3
# encoding: utf-8

# open CSVs files generated in /boletim-Paranaguá as pandas.DataFrame
# names in boletim-Paranaguá/order.txt
# august names "Boletim CORONAVÍRUS DD-MM -2020.pdf"
# june, july, september names "Boletim CORONAVÍRUS DD-MM-2020.pdf"

from pathlib import Path
import pandas

# get pdf's name by date and validates its existence
def get_pdf_name(day:int, month:int):
    name_pattern = "../boletim_Paranaguá/Boletim CORONAVÍRUS {:02d}-{:02d}{}-2020.pdf"
    name = ''
    if month in (6, 7, 9):
        space = ''
        name = name_pattern.format(day, month, space)
    elif month == 8:
        space = ' '
        name = name_pattern.format(day, month, space)
    else:
        return None

    if Path(name).is_file():
        return name
    return None

def get_csv_names(pdf_name:str):
    assert Path(pdf_name).is_file(), 'get_csv_names: pdf_name should be a valid file name'

    leng = len(pdf_name)
    pattern = pdf_name[:leng-4] + 't{}.csv'
    names = [pattern.format(i) for i in range(1, 5)]

    for name in names:
        if not Path(name).is_file():
            return None

    return names

def get_DataFrames(pdf_name:str):
    names = get_csv_names(pdf_name)
    if names is None:
        return None

    dataFrames = [pandas.read_csv(name) for name in names]
    return dataFrames

# T1 "CASOS CONFIRMADOS POR BAIRRO"
# T1 | Bairro | Feminino | Masculino | Total |
# T2 ...
# T3 "ÓBITOS"
# T3 | Bairro | Idade | Sexo |
# T4 "CASOS CONFIRMADOS POR BAIRRO E IDADE"
# T4 | Confirmados | Bairro | Idade | Sexo |
# Files
# Boletim CORONAVÍRUS (20|21|22|23|24)-07-2020.pdf
# T1, T2, T3
# Boletim CORONAVÍRUS (02-06 <-> 19-07)-2020.pdf
# T1, T2, T3, T4
if __name__ == "__main__":
    day = 15
    month = 8
    pdf_name = get_pdf_name(day, month)
    dataFrames = get_DataFrames(pdf_name)
    t1 = dataFrames[0]
    t2 = dataFrames[1]
    t3 = dataFrames[2]
    t4 = dataFrames[3]
