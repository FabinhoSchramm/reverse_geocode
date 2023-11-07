import pandas as pd
import glob
from geopy.geocoders import Nominatim
import os
import subprocess

class geopy:

    LOGIN_OS = os.getlogin()

    OS_NAME = os.name

    LOCAL_PATH = os.getcwd()

    if OS_NAME == 'posix':
        DIR = os.path.join('/home', LOGIN_OS, 'Documentos', 'Relatorios')
    else:
        DIR = os.path.join('C:\\Users', LOGIN_OS, 'Documentos', 'Relatorios')

    def mkdir(self) -> os:
        if self.LOGIN_OS in self.LOCAL_PATH:
            verifica_dir = os.path.exists(os.path.join(self.DIR, 'Relatorios'))
            if not verifica_dir:
                os.mkdir(os.path.join(self.DIR, 'Relatorios'))

    def path(self) -> list:
        if self.OS_NAME == 'posix':
            path = glob.glob('arquivos/*.xlsx', recursive=True)
        else:
            path = glob.glob(r'arquivos\*.xlsx', recursive=True)
        return path

    def reverse_geocode(self, files: list) -> pd.DataFrame:
        if len(files) >= 1:
            for file in files:
                print(file)
                data_frame = pd.read_excel(file)
                for index, row in data_frame.iterrows():
                    ENDERECO = str(row['Endereço'])
                    LAT = str(row['Latitude'])
                    LONG = str(row['Longitude'])
                    CORDENADAS = LAT + ',' + LONG
                    if ENDERECO == 'nan':
                        if LAT == 'nan' and LONG == 'nan' or LAT == 'nan' or LONG == 'nan':
                            continue
                        locator = Nominatim(user_agent='mygeocoder')
                        location = locator.reverse(CORDENADAS)
                        data_frame.at[index, 'Endereço'] = str(location.raw['display_name'])
                    else:
                        continue
                name = os.path.basename(file).replace('.xlsx', '')
                data_frame.to_excel(os.path.join(self.DIR, f'{name}.xlsx'), index=False)
            list_dir = os.listdir(os.path.join(self.LOCAL_PATH, 'arquivos'))
            for file in list_dir:
                os.remove(os.path.join('arquivos', file))
        else:
            return []

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
        self.open_dir()

if __name__ == '__main__':
    reverse_geocode = geopy()
    reverse_geocode.run()