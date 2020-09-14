##!/usr/bin/python3
# encoding: utf-8

# manually:
# # inserted Porto Seguro last point
# # removed empty neighborhood after Bockman 

# abre o geojson como um Feature Collection
# cria um vetor
# percorre o vetor
# # abre o LineString
# # cria um Polígono e coloca os pontos do LineString
# cria um Feature Collection e salva em disco



import geojson

feature_collection = geojson.load(open('data/neighborhood.geojson'))

features = []
for i in range(56):# feature_collection:
    feature = feature_collection[i]
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    polygon = geojson.Polygon([coordinates])
    feature.geometry = polygon
    features.append(feature)

feature_collection_of_polygons = geojson.FeatureCollection(features)

for i in range(57):
    if not feature_collection_of_polygons[i].is_valid:
        print(i)
        print(feature_collection_of_polygons[i].errors())

output = open('data/neighborhood4.geojson', 'w')
string = geojson.dump(feature_collection_of_polygons, output)
