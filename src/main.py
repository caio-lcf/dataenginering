import logging

from extract import run_extraction
from transform import run_transform

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Starting the Data Pipeline...")
    
    try:
        logging.info(">>> Starting Step 1: Extraction (TMDB API) <<<")
        run_extraction()
        logging.info(">>> Step 1 Complete! <<<")
        
        logging.info(">>> Starting Step 2: Transformation (JSON to Parquet) <<<")
        run_transform()
        logging.info(">>> Step 2 Complete! <<<")
        
        logging.info("Pipeline executed successfully! Data load finished.")
        
    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
