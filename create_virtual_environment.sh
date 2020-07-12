#!/bin/bash
virtualenv -p python3 enviroment
chmod +x ./enviroment/bin/activate
source enviroment/bin/activate
pip3 install pandas
