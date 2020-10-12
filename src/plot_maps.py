#!/usr/bin/python3
# encoding: utf-8

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
#import matplotlib.cm as cm
import pandas as pd
import geopandas
from itertools import product
from open_csv import get_DataFrames, get_pdf_name
from matplotlib.dates import datestr2num

def sum_row(serie):
    try:
        separator = ' - '
        if serie[0].find('–') != -1:
            separator = ' – '
        first = serie[0].split(separator)[1]
        second = serie[1].split(separator)[1]
        s1 = first.split('.')
        n1 = int(''.join(s1))
        s2 = second.split('.')
        n2 = int(''.join(s2))
        return n1 + n2
    except:
        return -1

all_days = []

# open data files
mapa_DataFrame = geopandas.read_file('data/neighborhood3.geojson')
# correct names in map
neighborhood = mapa_DataFrame['addr:place']
neighborhood = neighborhood.str.replace('Alboit', 'Vila Alboit')
neighborhood = neighborhood.str.replace('Alvorada', 'Jardim Alvorada')
neighborhood = neighborhood.str.replace('Centro Histórico', 'Centro')
neighborhood = neighborhood.str.replace('Divinéia', 'Vila Divineia')
neighborhood = neighborhood.str.replace('Eldorado', 'Jardim Eldorado')
neighborhood = neighborhood.str.replace('Itiberê', 'Jardim Itiberê')#?
neighborhood = neighborhood.str.replace('Jardim Yamaguchi', 'Loteamento Yamaguchi')
neighborhood = neighborhood.str.replace('Ouro Fino', 'Jardim Ouro Fino')
neighborhood = neighborhood.str.replace('Santa Helena', 'Vila Santa Helena')
neighborhood = neighborhood.str.replace('Vila Rute', 'Vila Ruth')
neighborhood = neighborhood.str.replace('Vila dos Comerciários', 'Comerciários')
mapa_DataFrame['addr:place'] = neighborhood
# Industrial
# None
# Oceania
# Dom Pedro II
# Divinéia
# Correia Velho

for month, day in product(range(7, 10), range(1, 32)):
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
    plt.savefig('../public/confirmados{:02d}-{:02d}.png'.format(day, month))#, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(1, 1)
    plt.title('Mortes por Coronavírus em Paranaguá até {:02d}/{:02d}'.format(day, month))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax.set_axis_off()
    mapa_DataFrame.plot(column='mortes', ax=ax, legend=True, cax=cax)
    plt.savefig('../public/mortes{:02d}-{:02d}.png'.format(day, month))#, bbox_inches='tight', pad_inches=0)
    plt.close()

    # [data casos_confirmados óbitos aguardando_result descartados recuperados] [casos_confirmados_acc óbitos_acc]
    line = [0]*6
    # date
    data = "2020-{:02d}-{:02d}".format(month, day)
    date = datestr2num(data)
    line[0] = date
    line[1] = t1['Total'].sum() # total casos confirmados
    line[2] = t3.shape[0]       # total óbitos
#    waiting = int(t2['Aguardando Resultados'][0].split(' - ')[1]) + int(t2['Aguardando Resultados'][1].split(' - ')[1])     # waiting exam result
    line[3] = sum_row(t2['Aguardando Resultados'])
    line[4] = sum_row(t2['Descartados'])
    line[5] = sum_row(t2['Recuperados'])
    if line.count(-1) == 0:
        all_days.append(line)
    else:
        print('Not doing T2 in {:02d}/{:02d}.'.format(day, month))

    del mapa_DataFrame['positive_tested']
    del mapa_DataFrame['mortes']

mapas_t2 = pd.DataFrame(all_days, columns=['Data', 'Casos Confirmados', 'Óbitos', 'Aguardando Resultado', 'Descartados', 'Recuperados'])

# include not accumulate data
cc = mapas_t2['Casos Confirmados'].to_numpy(copy=True)
cc[1:] -= cc[:-1]
mapas_t2['Casos Confirmados n_acc'] = cc
cc = mapas_t2['Óbitos'].to_numpy(copy=True)
cc[1:] -= cc[:-1]
mapas_t2['Óbitos n_acc'] = cc
cc = mapas_t2['Descartados'].to_numpy(copy=True)
cc[1:] -= cc[:-1]
mapas_t2['Descartados n_acc'] = cc
cc = mapas_t2['Recuperados'].to_numpy(copy=True)
cc[1:] -= cc[:-1]
mapas_t2['Recuperados n_acc'] = cc


# plot and save data
# individual days data: Aguardando Resultado, Descartados, Recuperados, Casos Confirmados n_acc, Óbitos n_acc
#plt.plot_date(mapas_t2['Data'], mapas_t2['Casos Confirmados'], xdate=True)
plt.plot_date(mapas_t2['Data'], mapas_t2['Aguardando Resultado'], xdate=True, label='Aguardando Resultado', linestyle='-', markersize=3)
plt.plot_date(mapas_t2['Data'][1:], mapas_t2['Descartados n_acc'][1:], xdate=True, label='Teste negativo', linestyle='-', markersize=3)
plt.plot_date(mapas_t2['Data'][1:], mapas_t2['Recuperados n_acc'][1:], xdate=True, label='Recuperados', linestyle='-', markersize=3)
plt.plot_date(mapas_t2['Data'][1:], mapas_t2['Casos Confirmados n_acc'][1:], xdate=True, label='Casos Confirmados', linestyle='-', markersize=3)
plt.plot_date(mapas_t2['Data'][1:], mapas_t2['Óbitos n_acc'][1:], xdate=True, label='Óbitos', linestyle='-', markersize=3)
plt.xticks(rotation=15)
plt.title('Dados diários')
plt.legend()
plt.savefig('../public/casos_confirmados.png')
plt.close()

# accumulate data
plt.plot_date(mapas_t2['Data'], mapas_t2['Casos Confirmados'], xdate=True, label='Casos Confirmados', linestyle='-', markersize=3)
plt.plot_date(mapas_t2['Data'], mapas_t2['Óbitos'], xdate=True, label='Óbitos', linestyle='-', markersize=3)
plt.xticks(rotation=15)
plt.title('Dados Acumulados')
plt.legend()
#plt.show()

plt.savefig('../public/obitos.png')
plt.close()

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
