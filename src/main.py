import logging

from extract import run_extraction
from transform import run_transform

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Iniciando o Pipeline de Dados...")
    
    try:
        logging.info(">>> Iniciando Passo 1: Extração (TMDB API) <<<")
        run_extraction()
        logging.info(">>> Passo 1 Concluído! <<<")
        
        logging.info(">>> Iniciando Passo 2: Transformação (JSON para Parquet) <<<")
        run_transform()
        logging.info(">>> Passo 2 Concluído! <<<")
        
        logging.info("Pipeline executado com sucesso! Carga de dados finalizada.")
        
    except Exception as e:
        logging.error(f"Ocorreu um erro durante a execução do pipeline: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
