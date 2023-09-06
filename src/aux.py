
import eurostat as euro
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import shutil
import random
from datetime import datetime
import matplotlib.font_manager as font_manager

class Aux:

    ## FRED
    def fetch_fred_data(self, series_id):
        base_url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
        "series_id": series_id,
        "api_key": "f1f34b60038a5ed90784a340985b0e50",
        "file_type": "json",
        "realtime_end": "9999-12-31",
        "observation_start": "1947-01-01"
    }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['observations'])
            df = df[df.realtime_end=="9999-12-31"]
            df = df[['date', 'value']]
            df = df.set_index('date')
            for date in df.index:
                if df.loc[date,'value'] == '.':
                    df.loc[date,'value'] = np.nan
            df = df.astype(float)
            return df.dropna()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    ## TIME FUNCTIONS
    def initiate_timer(self, message=None):
        tic = time.time()
        if message is not None: print(message)
        return tic
    
    def end_timer(self, tic):
        toc = time.time()
        print(f"Done in {toc - tic:.4f}s...\n")

    ## FOLDER MANAGEMENT FUNCTIONS
    def file_exists(self, folder, file_name, format=".csv"):
        # Check if the file exists in the folder
        if format in file_name: format = ''
        file_path = os.path.join(folder, file_name) + format
        if not os.path.isfile(file_path):
            print("The file doesn't exist. Downloading...")
            return False
        else:
            return True
        
    def find_file(self,folder, file_name):
        return folder + file_name
    
    ## OTHER
    def remove_str_from_list(self, L, a):
        return ' '.join(L).replace(a, '').split()

    
    @property
    def img_folder(self):
        return "tex/img/"

    @property
    def euro_folder(self):
        return "data/euro/"
    
    @property
    def us_folder(self):
        return "data/us/"


    @property
    def new_line(self):
        print("\n")

    @property
    def hline(self):
        print(60*"-")
