#!/bin/bash
virtualenv -p python3 environment
chmod +x ./environment/bin/activate ./environment/bin/activate_this.py
source environment/bin/activate
source environment/bin/activate_this.py
pip3 install pandas
