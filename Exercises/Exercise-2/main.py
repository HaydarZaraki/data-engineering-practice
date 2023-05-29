import requests
import pandas as pd
from bs4 import BeautifulSoup
import subprocess
import os

def main():
    # your code here
    path = './Downloads'
    if not os.path.exists(path):
        subprocess.run(['mkdir','Downloads'])
    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/?C=S;O=D'
    generic_url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    soup.prettify()
    rows = soup.find_all('tr')
    urls = []
    file_name = ""
    for i in rows:
        if len(i.contents) == 4:
            if "2022-02-07 14:03" in "".join(i.contents[1].contents[0]):
                file_name = "".join(i.a.contents)
                if not os.path.exists(f"{path}/{file_name}"):
                    subprocess.run(['wget',f'{generic_url}{"".join(i.a.contents)}','-P',path])
                break

    df = pd.read_csv(f"{path}/{file_name}")
    df = df[df.HourlyDryBulbTemperature.apply(lambda x: str(x).isdigit())]
    print(df.shape[0])
    print(f"\n\n\n\n\n {df.HourlyDryBulbTemperature.max(axis=0)} \n\n\n\n\n")
    # df = df[df.HourlyDryBulbTemperature == df.HourlyDryBulbTemperature.max()]
    # print(df.shape[0])
    
    pass


if __name__ == '__main__':
    main()
