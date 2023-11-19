#!/bin/bash

# Silly script to show how it works with a real example
python ../pdf-form-identify-fields.py GEF30-UAH.pdf -o GEF30-UAH.sh
python ../pdf-form-fill.py GEF30-UAH.pdf --ini GEF30-UAH.ini
