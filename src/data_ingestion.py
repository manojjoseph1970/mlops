import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger   
from src.custom_exception import CustomException
import sys
from sklearn.model_selection import train_test_split
import yaml
from config.path_config import *
from utils.common_functions import read_yaml


logger = get_logger(__name__)
class DataIngestion: 
    def __init__(self,config):
        self.config = config["data_ingestion"]
        
        self.bucket_name = self.config["bucket_name"]  
        self.bucket_file_name= self.config["bucket_file_name"] 
        self.train_test_split_ratio = self.config["train_ratio"]
        
        os.makedirs(RAW_DATA_DIR,exist_ok=True)    
        logger.info(f"DataIngestion initialized with { self.bucket_name} and file name is {self.bucket_file_name}: %s")
    def download_csv_from_gcp(self):
        try:
            logger.info("Starting data download from GCS bucket")
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Data downloaded successfully to {RAW_FILE_PATH}") 
        except Exception as e:
            logger.error("Error occurred while downloading data from GCS bucket")
            raise CustomException(e,sys)   
    def split_data_as_train_test(self):
        try:
            logger.info("Starting train-test split")
            df = pd.read_csv(RAW_FILE_PATH)
            train_set, test_set = train_test_split(df, test_size=1 - self.train_test_split_ratio, random_state=42)
            train_set.to_csv(TRAIN_FILE_PATH, index=False)
            test_set.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Train-test split completed. Train file: {TRAIN_FILE_PATH}, Test file: {TEST_FILE_PATH}")
        except Exception as e:
            logger.error("Error occurred during train-test split")
            raise CustomException(e, sys)
    def run(self):
        try:
            self.download_csv_from_gcp()
            self.split_data_as_train_test()
            logger.info("Data ingestion process completed successfully")
        except Exception as e:
            logger.error("Error occurred in the data ingestion process")
            raise CustomException(e,sys)
        finally:
            logger.info("Data ingestion process finished")
if __name__ == "__main__":
    try:
        config = read_yaml(CONFIG_PATH)
        print("Config:",config)
        data_ingestion = DataIngestion(config)
        data_ingestion.run()
    except CustomException as ce:
        logger.error(f"Data ingestion failed: {ce}")                       