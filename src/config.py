from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_TOKEN")
movie_data_endpoint = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
genre_id_endpoint = "https://api.themoviedb.org/3/genre/movie/list?language=en"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_path = os.path.join(BASE_DIR, 'data', 'raw')
bronze_path = os.path.join(BASE_DIR, 'data', 'bronze')
silver_path = os.path.join(BASE_DIR, 'data', 'silver')
gold_path = os.path.join(BASE_DIR, 'data', 'gold')
date_of_collect = datetime.now().strftime("%d-%m-%Y")
movie_json_path = f'{raw_path}/{date_of_collect}/popular_movie.json'
genre_json_path = f'{raw_path}/{date_of_collect}/genre_data.json'
movie_parquet_output = f'{bronze_path}/{date_of_collect}/popular_movie.parquet'
genre_parquet_output = f'{bronze_path}/{date_of_collect}/genre_data.parquet'
cleared_movie_parquet_output = f'{silver_path}/{date_of_collect}/cleared_movie.parquet'