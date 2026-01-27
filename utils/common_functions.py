import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import sys
import yaml
logger = get_logger(__name__)
def read_yaml(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (str): The path to the YAML file. 
    """    
    try :
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file {file_path} read successfully.")
            return config
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException(e)
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException("failed to read yaml ",e)
    
def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}.")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise CustomException("Failed to load data",e)    
    
