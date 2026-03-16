# Data Engineering Project: TMDB Data Pipeline

This project is a data engineering pipeline that extracts popular movie data and genres from The Movie Database (TMDB) API, stores the raw data, and transforms it into cleaned Parquet files for further analysis.

## Pipeline Steps

1. **Extract (`src/extract.py`)**: 
   - Fetches popular movies and genres from the TMDB API.
   - Adds an ingestion timestamp.
   - Saves the raw JSON data in `data/raw/YYYY-MM-DD`.

2. **Transform (`src/transform.py`)**:
   - Converts the raw JSON files into Parquet format.
   - Cleans the movie data by mapping genre IDs to genre names and dropping unnecessary columns.
   - Saves the final processed data to Parquet format.

## Setup

- Ensure you have a `.env` file with your `TMDB_TOKEN`.
- Install the required packages (e.g., `requests`, `pandas`, `python-dotenv`, `pyarrow`/`fastparquet`).
