#!/usr/bin/python3
# encoding: utf-8

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
#import matplotlib.cm as cm
import pandas as pd
import geopandas
from itertools import product
from open_csv import get_DataFrames, get_pdf_name

# open data files
mapa_DataFrame = geopandas.read_file('data/neighborhood3.geojson')
#day=25
#month=7
for day, month in product(range(1, 32), range(7, 10)):
    pdf_name = get_pdf_name(day, month)
    if pdf_name is None:
        print('Not doing {:02d}/{:02d}.'.format(day, month))
        continue
    csv_DataFrames = get_DataFrames(pdf_name)
    if csv_DataFrames is None:
        print('Not doing {:02d}/{:02d}.'.format(day, month))
        continue
    t1 = csv_DataFrames[0]
    t2 = csv_DataFrames[1]
    t3 = csv_DataFrames[2]
    # correct names in map
    neighborhood = mapa_DataFrame['addr:place']
    neighborhood = neighborhood.str.replace('Vila Rute', 'Vila Ruth')
    neighborhood = neighborhood.str.replace('Eldorado', 'Jardim Eldorado')
    neighborhood = neighborhood.str.replace('Itiberê', 'Jardim Itiberê')
    neighborhood = neighborhood.str.replace('Alboit', 'Vila Alboit')
    mapa_DataFrame['addr:place'] = neighborhood
    # join tables
    confirmed = pd.DataFrame({'addr:place':t1['Bairro'], 'positive_tested':t1['Total']})
    mapa_DataFrame = mapa_DataFrame.merge(confirmed, on='addr:place', how='left')
    t33 = t3.value_counts('Bairro')
    t333 = pd.DataFrame({'addr:place': t33.index, 'mortes': t33})
    mapa_DataFrame = mapa_DataFrame.merge(t333, on='addr:place', how='left')
    mapa_DataFrame['mortes'] = mapa_DataFrame['mortes'].fillna(0)
    #plot
    fig, ax = plt.subplots(1, 1)
    plt.title('Casos Confirmados de Coronavírus em Paranaguá em {:02d}/{:02d}'.format(day, month))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax.set_axis_off()
    mapa_DataFrame.plot(column='positive_tested', ax=ax, legend=True, cax=cax, missing_kwds={'color':'lightgrey'})
    #plt.show()
    plt.savefig('plots/confirmados{:02d}-{:02d}.png'.format(day, month))#, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(1, 1)
    plt.title('Mortes por Coronavírus em Paranaguá até {:02d}/{:02d}'.format(day, month))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax.set_axis_off()
    mapa_DataFrame.plot(column='mortes', ax=ax, legend=True, cax=cax)
    plt.savefig('plots/mortes{:02d}-{:02d}.png'.format(day, month))#, bbox_inches='tight', pad_inches=0)
    plt.close()

    del mapa_DataFrame['positive_tested']
    del mapa_DataFrame['mortes']

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
