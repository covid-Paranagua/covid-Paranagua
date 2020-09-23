# covid-watch
Visualization of Covid-19 evolution in Paranaguá/Curitiba.

## Some useful sources

Map visualizations using Python:

 * https://towardsdatascience.com/how-safe-are-the-streets-of-santiago-e01ba483ce4b

Data sources:

 * http://www.saude.pr.gov.br/Pagina/Coronavirus-COVID-19
 * http://www.paranagua.pr.gov.br/boletim-epidemiologico.php
 * https://www.curitiba.pr.gov.br/dadosabertos/busca/?grupo=16
 * ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2015/UFs/PR/
 * http://download.geofabrik.de/south-america/brazil/sul-latest-free.shp.zip

## Scripts
You need to make *Setup* just one time. Then, activate the virtual enviroment with:

    source environment/bin/activate

With the libraries available use these scripts:

 * boletim_Paranaguá/parse_paranagua_pdf.py download new PDFs from Paranaguá's website, convert they to CSV and warn if something went wrong.
 * teste/teste.py plot Paranaguá city contour through a shape (shp) file.
 * teste/mapa_confirmados.py draw a map with Paranguá's neighborhoods with colors representing the confirmed cases.
 * teste/open_csv.py some functions to get file names and open the files. It has some functions with the same funcionality of parse_paranagua_pdf.py.
 * teste/geojson_converter.py transform a geojson file with a LineString to a Poolygon
 * teste/plot_maps.py open all CSV files and draw colored maps informing number of confirmed cases and deaths in each neighboorhood.

## Setup
Install virtual env:

    # apt install virtualenv

Create environment with script:

    $ ./create_virtual_environment
