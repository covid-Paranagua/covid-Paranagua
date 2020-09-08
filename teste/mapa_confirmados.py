##!/usr/bin/python3
# encoding: utf-8

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import fiona

from open_csv import get_DataFrames, get_pdf_name

day=13
month=7

pdf_name = get_pdf_name(day, month)
DataFrames = get_DataFrames(pdf_name)

t1 = DataFrames[0]
bairro = t1['Bairro']
casos_confirmados = t1['Total']

dicionario = {}
for bar, tot in zip(bairro, casos_confirmados):
    dicionario[bar] = tot

MAX_casos_confirmados = max(casos_confirmados)
MIN_casos_confirmados = min(casos_confirmados)

colormap = cm.get_cmap('Greens')
cor_bairro = {
    bairro: colormap(
        (casos - MIN_casos_confirmados) / (MAX_casos_confirmados - MIN_casos_confirmados)
    )
    for bairro, casos in dicionario.items()
}

bairro_contorno = {}
with fiona.open('data/neighborhood.geojson') as fd:
    for neighborhood in fd:
        bairro_contorno[neighborhood['properties']['addr:place']] = neighborhood['geometry']
bairro_contorno['Vila Alboit'] = bairro_contorno['Alboit'] # different name
bairro_contorno['Jardim Itiberê'] = bairro_contorno['Itiberê']
bairro_contorno['Jardim Eldorado'] = bairro_contorno['Eldorado']
bairro_contorno['Vila Ruth'] = bairro_contorno['Vila Rute']

# remove unknown

# remove unknown on the fly
for neigh, geometry in bairro_contorno.items():
    if not neigh in dicionario:
        print(neigh)
        continue

    coordinates = geometry['coordinates']
    data_x = [point[0] for point in coordinates]
    data_y = [point[1] for point in coordinates]
    colour = cor_bairro[neigh]
    plt.fill(data_x, data_y, c=colour)
    # Draw a line surrounding the area
    plt.plot(data_x, data_y, c='black', linewidth=0.2)

plt.show()

#data_x = [x for x, y in data['geometry']['coordinates'][0]]
#data_y = [y for x, y in data['geometry']['coordinates'][0]]
#plt.fill(data_x, data_y, c=colour)
# Draw a line surrounding the area
#plt.plot(data_x, data_y, c='black', linewidth=0.2)

#bairro_contorno.items()
#for b, _ in bairro_contorno.items():
#    if not b in dicionario:
#        print(b)

# 40/55 15 faltantes
# Eldorado = Jardim Eldorado
# Vila dos Comerciários = Comerciários
# Industrial
# Oceania
# Vila Rute (Deveria ser dicionario['Vila Ruth'] = bairro_contorno['Vila Rute'])
# Itiberê = Vila Itiberê
# None
# Dom Pedro II
# Alvorada = Jardim Alvorada
# Divinéia
# Correia Velho
# Ouro Fino = Jardim Ouro Fino
# Centro Histórico = Centro (verificar)
# Santa Helena = Vila Santa Helena
# Alboit = Vila Alboit

# Colônia Pereira ## bairros rurais
# Jardim Jacarandá
# Jardim Ouro Fino == Ouro Fino
# Cominese
# Vila Caic inside Yamaguchi
# Jardim Eldorado = Eldorado
# Vila Divineia = Divineia
# Vila Itiberê = Itiberê
# Centro = Centro Histório (verificar)
# Outros municípios = Outros municípios (colocar uma legenda)
# Vila Santa Maria
# Vale do Sol
# Comerciários = Vila dos Comerciários
# Parque Agari
# João Gualberto
# Jardim Alvorada = Alvorada
# Vila São Jorge
# Colônia Maria Luíza ## bairros rurais
# Morro Inglês ## bairros rurais
# Jardim Yamaguchi
# Santos Dumont dentro do Vila São Vicente ou Guaraituba
# Vila São Carlos
# Labra
# Vila Santa Helena = Santa Helena
# Colônia São Luiz ## bairros rurais
# Vila Marinho
# Jardim Santa Rosa
# Jardim Figueira
# Vila Alboit = Alboit
# Vila Primavera
# Jardim Guadalupe
# Embocui
