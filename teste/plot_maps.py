##!/usr/bin/python3
# encoding: utf-8

import matplotlib.pyplot as plt
#import matplotlib.cm as cm
import pandas as pd
import geopandas
from open_csv import get_DataFrames, get_pdf_name

# open data files
day=25
month=7
pdf_name = get_pdf_name(day, month)
csv_DataFrames = get_DataFrames(pdf_name)
t1 = csv_DataFrames[0]
t2 = csv_DataFrames[1]
t3 = csv_DataFrames[2]
mapa_DataFrame = geopandas.read_file('data/neighborhood3.geojson')
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

#plot
fig, ax = plt.subplots(1, 1)
mapa_DataFrame.plot(column='positive_tested', ax=ax, legend=True, missing_kwds={'color':'lightgrey'})
#mapa_DataFrame.plot(column='positive_tested', missing_kwds={'color':'lightgrey'})
plt.show()

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
