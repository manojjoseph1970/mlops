import os
from pathlib import Path
############################# DATA INGESTIONS PATHS ##################################
RAW_DATA_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DATA_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DATA_DIR,"train.csv")
TEST_FILE_PATH = os.path.join(RAW_DATA_DIR,"test.csv")
CONFIG_PATH = "config/config.yaml"

############################# DATA PROCESSING PATH ##################################
PROCESSED_DIR='artifacts/processed'
PROCESSED_TRAIN_DATA_PATH=os.path.join(PROCESSED_DIR,'processed_train.csv')
PROCESSED_TEST_DATA_PATH=os.path.join(PROCESSED_DIR,'processed_test.csv')
TARGET_ENCODER_PATH=os.path.join(PROCESSED_DIR,'target_encoder.pkl')    


######################### model output path ################################
MODEL_DIR='artifacts/models/lgbm_model.pkl'
