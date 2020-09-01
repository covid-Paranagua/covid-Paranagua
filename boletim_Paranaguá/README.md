# Boletim Paranaguá

The script download data from Paranaguá Counsil Website and convert the pdf to csv to be easier to machine read. PDF's website source is http://www.paranagua.pr.gov.br/boletim-epidemiologico.php . The csv are intended to be used to plot maps.

Three libraries to process PDF were tested: pypdf4, tabula-py and camelot. The latter one was the best because is intended to read tables and can read portuguese accents in characters.

## PDF Structure

From 02-06-2020 until 19-07-2020 the PDFs have four groups of page displaying tables that we call T1, T2, T3 and T4. Beginning in 20-07-2020 until recently the PDFs have only the firsts three table types.

### T1
Show number of confirmed cases by neighbourhood. It is identified by a string ending with "CASOS CONFIRMADOS POR BAIRRO".

| Bairro | Feminino | Masculino | Total |
| ------ | -------- | --------- | ----- |
|'string'| 'Int64'  | 'Int64'   |'Int64'|

### T2
Show tests results. Inform how many are waiting results, how many were tested negative for COVID-19 and how many have healed.

 * Waiting results:
 * * d[2][1] "Feminino - NN"
 * * d[2][2] "Masculino - NN"
 * Tested Negative:
 * * d[1][5] "Masculino - NN"
 * * d[1][6] "Feminino - NN"
 * Healed:
 * * d[2][5] "Masculino - NN"
 * * d[2][6] "Feminino - NN"

### T3
Number of deaths. It is identifyied by a string ending with "ÓBITOS".

| Bairro | Idade | Sexo   |
| ------ | ----- | ----   |
|'string'|'Int64'|'string'|

### T4
Number of confirmed tests for each neighbourhood. It is identifyied by a string ending with "CASOS CONFIRMADOS POR BAIRRO E IDADE". This table is not available anymore in 20-07-2020 onward.

| Confirmados | Bairro | Idade | Sexo   |
| ----------- | ------ | ----- | ----   |
| 'Int64'     |'string'|'Int64'|'string'|

## Output
Each PDF file have four csv files. The ".pdf" ending is removed and a tN.csv is added, where N can be 1, 2, 3 or 4, one file for each table kind.
