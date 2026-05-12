import logging
import os
from datetime import datetime

def setup_logger(name="quant_strategy"):
    """
    Configura um logger industrial que salva em arquivo e exibe no console.
    """
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formato do Log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler para Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Handler para Arquivo (Diário)
    log_filename = f"logs/session_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    
    # Adicionar handlers ao logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger

# Instância Global
logger = setup_logger()
