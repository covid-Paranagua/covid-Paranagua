##!/usr/bin/python3
# 
# Baixar arquivos pdf do site http://www.paranagua.pr.gov.br/boletim-epidemiologico.php
#   - Baixar o sitee listar os links terminando com .pdf
#   - Baixar o que não possuo
# Converter os PDF para CSV
#   - Encontrar a página correta
#   - Há em algum lugar o número de pacientes? Criar uma tabela gigantesca? Gravar diretamente no arquivo sem fazer uma tabela no programa?
#

# download all pdf that are not available
def download_missing_pdf():
    import urllib
    from urllib import request
    from pathlib import Path
    import re
    page = request.urlopen("http://www.paranagua.pr.gov.br/boletim-epidemiologico.php")
    html = page.read().decode('utf8')
    pattern = re.compile('href=[\'"]?downloads/boletins/([^\'">]+)')
    links = pattern.findall(html)
    for l in links:
        if not Path(l).is_file():
            try:
                request.urlretrieve ("http://www.paranagua.pr.gov.br/downloads/boletins/" + urllib.request.pathname2url(l), filename=l)
            except:
                print("File not found: {0}.".format("http://www.paranagua.pr.gov.br/downloads/boletins/" + l))
    # write a file with all downloaded PDF file names order
    f = open('order.txt', 'w')
    for l in links:
        f.write(l + '\n')
    f.close()

# read order.txt and convert
def convert_new_pdfs():
    print('converting\n')
    from pathlib import Path
    with open('order.txt', 'r') as f:
        for l in f.readlines():
            l = l[:len(l)-1]
            expected_csv_name = l[:len(l)-4] + 't1.csv'
            print('Read line: ' + l)
            if Path(l).is_file() and not Path(expected_csv_name).is_file():
                print("Converting file" + l + '\n')
                read_pdf(l)

# read a PDF file and generate the four csv files.
def read_pdf(pdf_name):
    import camelot
    length = len(pdf_name)
    output = pdf_name[0:(len(pdf_name)-4)]
    day_string = pdf_name[(length - 14):(length - 4)]
    tables =  camelot.read_pdf(pdf_name, pages='1-end')

    t1 = open(output + 't1.csv', 'w')
    t1.write('Bairro,Feminino,Masculino,Total\n')
    t2 = open(output + 't2.csv', 'w')
    t3 = open(output + 't3.csv', 'w')
    t3.write('Bairro,Idade,Sexo\n')
    t4 = open(output + 't4.csv', 'w')
    t4.write('Confirmados,Bairro,Idade,Sexo\n')
    for i in range(len(tables)):
        data = tables[i].df
        text = data[0][0]
        d = data[1:]
        last_index = d.shape[0] -1
        table_number = 2
        if text.endswith('CASOS CONFIRMADOS POR BAIRRO'):
            table_number = 1
        elif text.endswith('ÓBITOS'):
            table_number = 3
        elif text.endswith('CASOS CONFIRMADOS POR BAIRRO E IDADE'):
            table_number = 4
        if table_number in (1, 3, 4):
            td = [] # table data, html inspired name
            rows = d.shape[0] - 1
            cols = d.shape[1] - 1
            for j in range(1, rows):
                for k in range(1, cols):
                    cell = d.iloc[j][k]
                    for l in cell.split(' \n'):
                        td.append(l)
            if table_number == 3:
                if td.__contains__('Total'):
                    pos = td.index('Total')
                    td = td[0:pos] + td[pos+1:pos+4] + td[pos+5:]

        if table_number == 1:
            for a, b, c, d in zip(td[0::4], td[1::4], td[2::4], td[3::4]):
                t1.write(a + ',' + b + ',' + c + ',' + d + '\n')
        elif table_number == 2:
            t2.write('Aguardando Resultados,' + d[2][1] + ',' + d[2][2] + '\n')
            t2.write('Descartados,' + d[1][6] + ',' + d[1][5] + '\n')
            t2.write('Recuperados,' + d[2][6] + ',' + d[2][5] + '\n')
        elif table_number == 3:
            for a, b, c in zip(td[0::3], td[1::3], td[2::3]):
                t3.write(a + ',' + b + ',' + c + '\n')
        elif table_number == 4:
            for a, b, c, d in zip(td[0::4], td[1::4], td[2::4], td[3::4]):
                t4.write(a + ',' + b + ',' + c + ',' + d + '\n')

    t1.close()
    t2.close()
    t3.close()
    t4.close()

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
    download_missing_pdf()
    convert_new_pdfs()
