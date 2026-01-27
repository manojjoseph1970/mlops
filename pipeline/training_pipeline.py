from  src.custom_exception import CustomException
import sys
from src.logger import get_logger
from config.path_config import *
from src.data_preprocessing import DataPreprocessor
from utils.common_functions import read_yaml
from src.data_ingestion import DataIngestion
from src.model_training import NodelTrainer
import os


logger = get_logger(__name__)


if __name__ == "__main__":
        try:
            
            # data ingestion    
            data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
            data_ingestion.run()
            logger.info("Data ingestion completed successfully.")
            
            # data preprocessing
            data_preprocessor = DataPreprocessor(CONFIG_PATH)
            data_preprocessor.process_and_save()
            logger.info("Data preprocessing completed successfully.")

            # model training

            model_trainer = NodelTrainer(config_path=CONFIG_PATH)
            metrics = model_trainer.run_model_trainer()            
            logger.info("Data preprocessing completed successfully.")
        except CustomException as ce:
            logger.error(f"Pipeline failed with CustomException: {ce}")
            raise CustomException(ce, sys)
        
