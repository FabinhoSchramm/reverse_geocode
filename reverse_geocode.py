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
        DIR = f'/home/{LOGIN_OS}/Documentos/Relatorios'
    else:
        DIR = f'C://Users//{LOGIN_OS}//Documentos/Relatorios'

    def mkdir(self) -> os:
        if self.OS_NAME == 'posix':
            DIR = f'/home/{self.LOGIN_OS}/Documentos'
        else:
            DIR = f'C://Users//{self.LOGIN_OS}//Documentos'

        if self.LOGIN_OS in self.LOCAL_PATH:
            verifica_dir = os.path.exists(DIR + '/Relatorios')
            if verifica_dir == True:
                return []
            else:
                PATH = os.path.join(DIR,'Relatorios')
                os.mkdir(PATH)

    def path(self) -> list:
        if self.OS_NAME == 'posix':
            path = glob.glob('arquivos/*.xlsx',recursive=True)
        else:
            path = glob.glob(r'arquivos\*.xlsx',recursive=True)
        return path
     
    def reverse_geocode(self, files: list) -> pd.DataFrame:
        if len(files) >= 1:
            for file in files:
                print(file)
                data_frame = pd.read_excel(file)
                for index,row in data_frame.iterrows():
                    ENDERECO = str(row['ENDEREÇO'])
                    if len(ENDERECO) > 1:
                        continue
                    else:
                        LAT = str(row['LATITUDE'])
                        LONG = str(row['LONGITUDE'])
                        CORDENADAS = LAT + ',' + LONG
                        locator = Nominatim(user_agent='mygeocoder')
                        location = locator.reverse(CORDENADAS)
                        data_frame.at[index,'ENDEREÇO'] = str(location.raw['display_name'])
                name = file.replace('.xlsx','')
                data_frame.to_excel(f'{self.DIR}/{name[9:-1]}.xlsx',index=False)
                list_dir = os.listdir(f'{self.LOCAL_PATH}/arquivos/')
                for file in list_dir:
                    os.remove('arquivos/'+file)
        else:
            return []
        
    def open_dir(self) -> None:
        if self.OS_NAME == 'posix':
            try:
                subprocess.call(["open",f'/home/{self.LOGIN_OS}/Documentos/Relatorios'])
            except subprocess.CalledProcessError:
                pass
        else:
            os.startfile(rf'C:\Users\{self.LOGIN_OS}\Documentos\Relatorios')

    def run(self) -> None:
        self.mkdir()
        self.reverse_geocode(self.path())
        self.open_dir()

if __name__ == '__main__':
    reverse_geocode = geopy()
    reverse_geocode.run()