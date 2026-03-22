import requests
import pandas as pd
from dotenv import load_dotenv
import os
import json
from config import TMDB_TOKEN, movie_data_endpoint, genre_id_endpoint, raw_path, bronze_path, date_of_collect
from datetime import datetime

from config import raw_path, bronze_path, silver_path, gold_path

dirs = [raw_path, bronze_path, silver_path, gold_path]
def create_dirs(dirs_list:list):
    for dir_path in dirs_list:
        os.makedirs(dir_path, exist_ok=True)
    return None
create_dirs(dirs)

def get_movie_data (endpoint:str, token:str):
    headers = {"accept": "application/json",
                "Authorization":f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    movie_data = response.json()['results']
    ingestion_time = datetime.now().isoformat()
    for movie in movie_data:
        movie["ingestion_time"] = ingestion_time
    return movie_data

def get_genre_id (genre_id_endpoint: str, token:str):
    headers = {"accept": "application/json",
                "Authorization":f"Bearer {token}"}
    response = requests.get(genre_id_endpoint, headers=headers)
    response.raise_for_status()
    genre_data = response.json()['genres']
    return genre_data

def save_raw_json(path:str, getted_data:str, archive_name:str):
    os.makedirs(f"{path}/{date_of_collect}", exist_ok=True)
    with open (f'{path}/{date_of_collect}/{archive_name}.json', 'w') as w:
        json.dump(getted_data, w, indent=4)

def run_extraction():
    movie_data = get_movie_data(movie_data_endpoint, TMDB_TOKEN)
    genre_data = get_genre_id(genre_id_endpoint,TMDB_TOKEN)
    save_raw_json (raw_path, movie_data, "popular_movie")
    save_raw_json (raw_path, genre_data, "genre_data")  



