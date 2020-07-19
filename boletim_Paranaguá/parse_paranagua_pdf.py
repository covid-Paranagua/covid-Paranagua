##!/usr/bin/python3
# 
# Baixar arquivos pdf do site http://www.paranagua.pr.gov.br/boletim-epidemiologico.php
#   - Baixar o sitee listar os links terminando com .pdf
#   - Baixar o que não possuo
# Converter os PDF para CSV
#   - Encontrar a página correta
#   - Há em algum lugar o número de pacientes? Criar uma tabela gigantesca? Gravar diretamente no arquivo sem fazer uma tabela no programa?
#

def download_missing_pdf():
    import urllib
    from urllib import request
    from pathlib import Path
    import re
    page = request.urlopen("http://www.paranagua.pr.gov.br/boletim-epidemiologico.php")
    html = page.read().decode('utf8')
#    pattern = re.compile('\"[^\"]pdf\"')
    pattern = re.compile('href=[\'"]?downloads/boletins/([^\'">]+)')
    links = pattern.findall(html)
    #'downloads/boletins/Boletim Epidemiológico 06-04-2020.pdf'
    for l in links:
        if not Path(l).is_file():
            request.urlretrieve ("http://www.paranagua.pr.gov.br/downloads/boletins/" + urllib.request.pathname2url(l), filename=l)

def read_pdf():
    from PyPDF4 import PdfFileReader
    file = open('Boletim_CORONAVIRUS_11-07-2020.pdf', 'rb')
    document = PdfFileReader(file)
    document.numPages
    document.numPages
    document.documentInfo
    document.pages[0]
    document.pages[0].extractText()
    p0 = document.pages[0]
    p0.getContents()
    p0.items
    p0.items()
    p0.extractText()
    document.pages[0].extractText()
    document.pages[0].extractText()
    document.pages[1].extractText()
    document.pages[3].extractText()
    document.pages[7].extractText()
    document.pages[6].extractText()
    document.pages[0].extractText()
    document.pages[3].extractText()
    document.pages[4].extractText()
    document.pages[5].extractText()
