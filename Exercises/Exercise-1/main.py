import requests
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

def download_files(url):
    csv_filename = f"./Downloads/{url.split('/')[-1]}".replace(".zip", ".csv")
    if not os.path.exists(csv_filename):
        zipped_filename = f"./Downloads/{url.split('/')[-1]}"

        df = requests.get(url)
        if df.ok:
            with open(zipped_filename, 'wb') as fd:
                for chunk in df.iter_content(chunk_size=128):
                    fd.write(chunk)
            subprocess.run(["unzip","-q",zipped_filename,"-d","Downloads"])
            subprocess.run(["rm","-f",zipped_filename])
            return f"Success ------------ {url}"
        else:
            return f"Failed ------------ {url}"
    else:
        return f"File {csv_filename} Already Exists"

def main():
    # your code here
    path = "./Downloads"
    macosx_path = f"{path}/__MACOSX"
    if not os.path.exists(path):
        subprocess.run(["mkdir","Downloads"])
    with ThreadPoolExecutor() as executor:
        results = executor.map(download_files, download_uris)
        for result in results:
            print(result)
    #remove __MACOSX folder
    if os.path.exists(macosx_path):
        subprocess.run(['rm','-rf',macosx_path])


if __name__ == '__main__':
    main()
