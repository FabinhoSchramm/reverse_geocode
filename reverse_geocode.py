import pandas as pd
import glob
from geopy.geocoders import Nominatim
import os
import subprocess

class geopy:

    LOGIN_OS = os.getlogin()

    OS_NAME = os.name

    LOCAL_PATH = os.getcwd()

    COLUMNS = ['Unidade rastreada', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3','Unnamed: 4', 'Unnamed: 5']

    if OS_NAME == 'posix':
        DIR = os.path.join('/home', LOGIN_OS, 'Documentos', 'Relatorios')
    else:
        DIR = os.path.join('C:\\Users', LOGIN_OS, 'Documentos', 'Relatorios')

    def mkdir(self) -> os:
        if self.LOGIN_OS in self.LOCAL_PATH:
            verifica_dir = os.path.exists(os.path.join(self.DIR))
            if not verifica_dir:
                os.mkdir(os.path.join(self.DIR, 'Relatorios'))

    def path(self) -> list:
        if self.OS_NAME == 'posix':
            path = glob.glob('arquivos/*.xlsx', recursive=True)
        else:
            path = glob.glob(r'arquivos\*.xlsx', recursive=True)
        return path

    def reverse_geocode(self, files: list) -> pd.DataFrame:
        for file in files:
            data_frame = pd.read_excel(file)
            if data_frame.columns.equals(data_frame.columns):
                new_data_frame = self.drop_rename(data_frame)
                for index, row in new_data_frame.iterrows():
                    ENDERECO = str(row['Endereço'])
                    LAT = str(row['Latitude'])
                    LONG = str(row['Longitude'])
                    CORDENADAS = LAT + ',' + LONG
                    if ENDERECO == 'nan':
                        if LAT == 'nan' and LONG == 'nan' or LAT == 'nan' or LONG == 'nan':
                            continue
                        locator = Nominatim(user_agent='mygeocoder')
                        location = locator.reverse(CORDENADAS)
                        # geo = location.raw['address']
                        address_parts = []  # Lista para armazenar partes do endereço
                        geo = location.raw.get('address', {})
                        if 'road' in geo:
                            address_parts.append(geo['road'])
                        if 'house_number' in geo:
                            address_parts.append(geo['house_number'])
                        if 'suburb' in geo:
                            address_parts.append(geo['suburb'])
                        if 'city' in geo:
                            address_parts.append(geo['city'])
                        if 'state' in geo:
                            address_parts.append(geo['state'])
                        if 'postcode' in geo:
                            address_parts.append(geo['postcode'])
                        address = ', '.join(address_parts)
                        if not address:
                            address = "Endereço não disponível"
                        data_frame.at[index, 'Endereço'] = address
                        print(address)
                    else:
                        continue
            else:
                print(f'{file}_error')
            name = os.path.basename(file).replace('.xlsx', '')
            data_frame.to_excel(os.path.join(self.DIR, f'{name}.xlsx'), index=False)
        list_dir = os.listdir(os.path.join(self.LOCAL_PATH, 'arquivos'))
        for file in list_dir:
            os.remove(os.path.join('arquivos', file))
        self.open_dir()

    def drop_rename(self,data_frame:pd.DataFrame) -> pd.DataFrame:
        data_frame.rename(columns={'Unnamed: 1':'Data do evento', 'Unnamed: 2':'Data da atualização',
                'Unnamed: 3':'Latitude','Unnamed: 4':'Longitude','Unnamed: 5':'Endereço'},inplace=True)
        data_frame.drop(index=0,inplace=True)
        return data_frame

    def open_dir(self) -> None:
        if self.OS_NAME == 'posix':
            try:
                subprocess.call(["open", os.path.join('/home', self.LOGIN_OS, 'Documentos', 'Relatorios')])
            except subprocess.CalledProcessError:
                pass
        else:
            os.startfile(os.path.join('C:\\Users', self.LOGIN_OS, 'Documentos', 'Relatorios'))

    def run(self) -> None:
        self.mkdir()
        self.reverse_geocode(self.path())
        

if __name__ == '__main__':
    reverse_geocode = geopy()
    reverse_geocode.run()
