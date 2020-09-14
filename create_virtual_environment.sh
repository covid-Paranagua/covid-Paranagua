#!/bin/bash
if [[ ! -d "environment" ]]
then
    virtualenv -p python3 environment
    chmod +x ./environment/bin/activate ./environment/bin/activate_this.py
fi
source environment/bin/activate
pip3 install pandas ipython camelot-py geopandas opencv-python matplotlib descartes geojson
