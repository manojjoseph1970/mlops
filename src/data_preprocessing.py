import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
import sys
from config.path_config import *
from utils.common_functions import load_data, read_yaml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier


logger = get_logger(__name__)


class DataPreprocessor:
    def __init__(self, config_path: str):
        try:
            self.config = read_yaml(config_path)
            self.train_path = TRAIN_FILE_PATH
            self.test_path = TEST_FILE_PATH
            if not os.path.exists(PROCESSED_DIR):
                os.makedirs(PROCESSED_DIR, exist_ok=True)
            
            logger.info("DataPreprocessor initialized with configuration.")
        except Exception as e:
            logger.error("Failed to initialize DataPreprocessor.")
            raise CustomException(e, sys)

    def preprocess_data(self, data: pd.DataFrame)-> pd.DataFrame:
        try:
            logger.info("Dropping booking Id  from the dataset.")
            data.drop(columns=['Booking_ID'], inplace=True)
            data.drop_duplicates(inplace=True)
            cat_cols = self.config['data_processing']['categorical_features']
            numerical_cols = self.config['data_processing']['numerical_features']   
            logger.info(f"Categorical columns: {cat_cols}")
            logger.info(f"Numerical columns: {numerical_cols}")
            logger.info("Starting preprocessing steps. Apping label Encoding .")
            label_encoder = LabelEncoder()    
            mapping_dict = {}
            for col in cat_cols:
                data[col] = label_encoder.fit_transform(data[col])
                mapping_dict[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))  
            logger.info("Label Encoding applied to categorical columns.")
            for col, mapping in mapping_dict.items():
                logger.info(f"Mapping for {col}: {mapping}")

            logger.info("Handling skewness .")
            skewness_threshold=self.config["data_processing"]["skewness_threshold"]
            for col in numerical_cols:
                skewness = data[col].skew()
                if abs(skewness) > skewness_threshold:
                    data[col] = np.log1p(data[col])
                    logger.info(f"Applied log transformation to {col} due to skewness of {skewness}.")
            # Example preprocessing steps
            # Handle missing values
            #data.fillna(method='ffill', inplace=True)
            logger.info("Missing values handled.")
            return data
        except Exception as e:
            logger.error("Error during data preprocessing.")
            raise CustomException(e, sys)
        
    def balance_dataframe(self, df: pd.DataFrame):

        """
            Balances the dataset using SMOTE.
        """
        try:
            target_col=self.config['data_processing']['target_column']  

            logger.info("Starting data balancing using SMOTE.")

            X = df.drop(columns=[target_col])
            y = df[target_col]
            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            logger.info("Data balancing using SMOTE completed.")
            balanced_df = pd.concat([X_resampled, y_resampled], axis=1)
            return balanced_df
        except Exception as e:
            logger.error("Error during data balancing.")
            raise CustomException(e, sys)
    def feature_selection(self, df: pd.DataFrame):

        """
         Selects important features using RandomForestClassifier.
        """
        try:
            target_col=self.config['data_processing']['target_column']  
            no_of_features=self.config['data_processing']['no_of_features']

                
            X = df.drop(columns=[target_col])
            y = df[target_col]
            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)
            importances = model.feature_importances_
            feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
            feature_importance_df.sort_values(by='Importance', ascending=False, inplace=True)
            selected_features = feature_importance_df.head(no_of_features)['Feature'].values.tolist()
            logger.info(f"Selected features: {selected_features}")
            logger.info(f"Feature selection completed.")
            return df[selected_features + [target_col]]
        except Exception as e:
            logger.error("Error during feature selection step.")
            raise CustomException(e, sys)
    def save_processed_data(self, df: pd.DataFrame, file_path: str):
        """
                Saves the processed DataFrame to a CSV file.
        """
        try:
            df.to_csv(file_path, index=False)
            logger.info(f"Processed data saved to {file_path}.")
        except Exception as e:
            logger.error("Error saving processed data.")
            raise CustomException(e, sys)
    def process_and_save(self):
        try:
                # Preprocess training data
            df_train=load_data(self.train_path)
            df_test=load_data(self.test_path)
            logger.info(f"Loaded training and testing data. {df_train.columns}")    
            df_train = self.preprocess_data(df_train)  
            df_test = self.preprocess_data(df_test)  
                   
            df_train = self.balance_dataframe(df_train)
            df_train = self.feature_selection(df_train)
            df_test = df_test[df_train.columns]  # Ensure test set has same features as train set   

            self.save_processed_data(df_train, PROCESSED_TRAIN_DATA_PATH) 
            self.save_processed_data(df_test, PROCESSED_TEST_DATA_PATH) 
        except Exception as e:
            logger.error("Error in process_and_save method.")
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        data_preprocessor = DataPreprocessor(CONFIG_PATH)
        data_preprocessor.process_and_save()
    except CustomException as ce:
        logger.error(f"Caught a CustomException in main: {ce}")                    