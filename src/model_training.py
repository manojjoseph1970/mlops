import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException        
import sys
from config.path_config import *
from config.model_params import *
from utils.common_functions import load_data, read_yaml
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix ,roc_auc_score,f1_score,precision_score, recall_score 
from scipy.stats import randint, uniform
from sklearn.model_selection import RandomizedSearchCV
import mlflow
from datetime import datetime
import warnings 
warnings.filterwarnings("ignore")


logger = get_logger(__name__)

class NodelTrainer:
    def __init__(self, config_path: str):
        try:
            self.config = read_yaml(config_path)
            self.train_path = PROCESSED_TRAIN_DATA_PATH
            self.test_path = PROCESSED_TEST_DATA_PATH

            if not os.path.exists(os.path.dirname(MODEL_DIR)):
                os.makedirs(os.path.dirname(MODEL_DIR), exist_ok=True)
            self.model_path = MODEL_DIR    
            self.param_grid = LIGHTGBM_PARAM_GRID
            self.random_search_params = RAMDOM_SEARCH_PARAMS
            logger.info("NodelTrainer initialized with configuration.")
        except Exception as e:
            logger.error("Failed to initialize NodelTrainer.")
            raise CustomException(e, sys)
    def load_and_split_data(self):
        try:
            logger.info("Loading processed training and testing data.")
            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)

            X_train = train_data.drop(columns=[self.config['data_processing']['target_column']])
            y_train = train_data[self.config['data_processing']['target_column']]
            X_test = test_data.drop(columns=[self.config['data_processing']['target_column']])
            y_test = test_data[self.config['data_processing']['target_column']]

            logger.info("Data loaded and split into features and target.")
            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error("Error occurred while loading and splitting data.")
            raise CustomException(e, sys)    

    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> LGBMClassifier:
        try:
            logger.info("Starting model training.")
            model = LGBMClassifier()
            model.set_params(**self.param_grid)
            logger.info("Model hyper parameter tuning started using RandomizedSearchCV.")
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.param_grid,
                **self.random_search_params
            )
            model = random_search.fit(X_train, y_train)
            logger.info("Model hyper parameter tuning  completed.")
            best_params = model.best_params_
            best_model = model.best_estimator_
            logger.info(f"Best parameters found: {best_params}")
            
            return best_model
        except Exception as e:
            logger.error("Error occurred during model training.")
            raise CustomException(e, sys)

    def evaluate_model(self, model: LGBMClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        try:
            logger.info("Starting model evaluation.")
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
            report = classification_report(y_test, y_pred)
            conf_matrix = confusion_matrix(y_test, y_pred)
            precision_score_value = precision_score(y_test, y_pred, average='weighted')
            recall_score_value = recall_score(y_test, y_pred, average='weighted')

            logger.info(f"Model Accuracy: {accuracy}")
            logger.info(f"Model F1 Score: {f1}")
            logger.info(f"Model ROC AUC Score: {roc_auc}")
            logger.info(f"Classification Report:\n{report}")
            logger.info(f"Confusion Matrix:\n{conf_matrix}")
            logger.info(f"Precision Score: {precision_score_value}")
            logger.info(f"Recall Score: {recall_score_value}")

            return {
                'accuracy': accuracy,
                'f1_score': f1,
                'roc_auc': roc_auc,
                'precision_score': precision_score_value,
                'recall_score': recall_score_value
            }
        except Exception as e:
            logger.error("Error occurred during model evaluation.")
            raise CustomException(e, sys)

    def save_model(self, model: LGBMClassifier):
        try:
            joblib.dump(model, MODEL_DIR)
            logger.info(f"Model saved at {MODEL_DIR}.")
        except Exception as e:
            logger.error("Error occurred while saving the model.")
    def run_model_trainer(self):
        try:
            run_name = f"{self.config['mlflow']['experiment_name']}_{datetime.now():%Y%m%d_%H%M}" 
            mlflow.set_experiment(self.config['mlflow']['experiment_name'])
            with mlflow.start_run(run_name=run_name):    
                logger.info("Model training process started.")
                logger.info("Starting  our mlflow expirment.")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                logger.info("logging the  dataset to mlflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")
                best_model = self.train_model(X_train, y_train)
                logger.info("logging the  model to mlflow")  
                
                mlflow.log_artifact(self.model_path, artifact_path="models")
                logger.info("logging the  model  params to mlflow")
                mlflow.log_params(best_model.get_params())
                evaluation_metrics = self.evaluate_model(best_model, X_test, y_test)
                logger.info("logging the  model  metrics to mlflow")
                mlflow.log_metrics(evaluation_metrics)  
                self.save_model(best_model)
                logger.info("Model training process completed.")
                return evaluation_metrics
        except Exception as e:
            logger.error("Error occurred in the model training process.",e)   
            raise CustomException(e, sys)
if __name__ == "__main__":
    try:
        model_trainer = NodelTrainer(config_path=CONFIG_PATH)
        metrics = model_trainer.run_model_trainer()
        logger.info(f"Final evaluation metrics: {metrics}")
    except CustomException as ce:
        logger.error(f"Model training failed with CustomException: {ce}")
        raise CustomException(e, sys)
            