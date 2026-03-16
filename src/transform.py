# %% 
import os
import pandas as pd
from datetime import datetime
from config import raw_path, bronze_path, silver_path, date_of_collect, movie_json_path, genre_json_path, movie_parquet_output, genre_parquet_output, cleared_movie_parquet_output
# %%
def json_to_parquet(input_path:str, output_path:str) -> pd.DataFrame:
    df = pd.read_json(f"{input_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(f"{output_path}", index=False)
    return print(f"Successfully converted {input_path} to {output_path}")
# %% 
def read_popular_movie(path:str) -> pd.DataFrame:
    popular_movie_df = pd.read_parquet(f"{path}")
    popular_movie_df.head(2)
    return popular_movie_df

def read_genre_data (path:str):
    genre_df = pd.read_parquet(f"{path}")
    return genre_df

def clear_popular_movie_df (df:pd.DataFrame, genre_df) -> pd.DataFrame:
    df = (df 
    .explode("genre_ids")
    .merge(genre_df,
    how="left",
    left_on="genre_ids",
    right_on="id")
    .drop(
        ["backdrop_path", "poster_path", "video", "id_y"], axis=1
    )
    .rename(columns={"id_x":"movie_id", "name":"genre_name"})
    )
    return df

def save_cleared_df(df:pd.DataFrame, output_path:str) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(f"{output_path}", index=False)
    return print(f"Successfully converted to {output_path}")
#%%
json_to_parquet(movie_json_path, movie_parquet_output)
json_to_parquet(genre_json_path, genre_parquet_output)
# %%
movie_df = read_popular_movie(movie_parquet_output)
genre_df = read_genre_data(genre_parquet_output)
# %%
cleared_df = clear_popular_movie_df(movie_df, genre_df)
save_cleared_df(cleared_df, cleared_movie_parquet_output)
# %% 
