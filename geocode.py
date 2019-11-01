"""
Instalation:

1. Make sure you installed all the requirments: pip install -r requirements.txt
2. Make sure, that you have 2 CVS files in your Project folder.
    "Motels in NZ.csv" - origin CSV file you need to geocode
    "Motels in NZ with addresses.csv" - where all decoded information will be saved.
3. Enjoy the result

"""
import geopy
import numpy as np
import pandas as pd
from geopandas.tools import geocode
import certifi
import ssl

from pandas import DataFrame

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx  #Create an SSL certificate, as currently there is a problem with that on Python 3

companies = pd.read_csv("Motels in NZ.csv", delimiter=',') #Reading CVS files


def companies_geocoder(row):
    try:
        address_full = geocode(row, provider='nominatim', timeout=5, scheme='http')
        address = address_full.address.iloc[0] #Getting an adress line as a string
        point = address_full.geometry.iloc[0]
        return pd.Series({'Y': point.y, 'X': point.x, 'Address': address})
    except:
        return None


companies[['Y', 'X', 'Address']] = companies.apply(lambda x: companies_geocoder(x['Name']), axis=1) #Creating an list of geocoded information

df = DataFrame(companies, columns= ['ID','Name','Address','X','Y','Country'])
df.to_csv(r'Motels in NZ with addresses.csv') #Creating a final CSV file

