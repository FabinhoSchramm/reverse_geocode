import pandas as pd
import glob
from geopy.geocoders import Nominatim

arquivos = glob.glob('*.xlsx')
for arquivo in arquivos:
    df = pd.read_excel(arquivo)
    for index,row in df.iterrows():
        LAT = str(row['LATITUDE'])
        LONG = str(row['LONGITUDE'])
        CORDENADAS = LAT + ',' + LONG
        locator = Nominatim(user_agent='mygeocoder')
        location = locator.reverse(CORDENADAS)
        df.at[index,'ENDEREÇO'] = str(location.raw['display_name'])
    df.to_excel(f'reverse_geocode_{arquivo}',index=False)