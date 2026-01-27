from scipy.stats import uniform, randint
LIGHTGBM_PARAM_GRID = {
    'num_leaves': randint(20, 150),
    'max_depth': randint(5, 30),
    'learning_rate': uniform(0.01, 0.3),
    'n_estimators': randint(50, 500),
    'min_child_samples': randint(5, 100),
    'subsample': uniform(0.5, 0.5),
    'colsample_bytree': uniform(0.5, 0.5),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1),
    'boosting_type': ['gbdt', 'dart', 'goss']
    
}
RAMDOM_SEARCH_PARAMS={
    'n_iter': 4,
    'scoring': 'accuracy',
    'cv': 3,
    'verbose': 1,
    'random_state': 42,
    'n_jobs': -1
}