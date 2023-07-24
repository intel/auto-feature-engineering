from pathlib import Path
import os
from pyrecdp.autofe import FeatureWrangler
import pandas as pd
import yaml
import argparse
import pandas as pd
from sklearn.metrics import mean_squared_error
import lightgbm as lgbm
import numpy as np
pathlib = str(Path(__file__).parent.parent.resolve())


def run(cfg):
    workspace = cfg.workspace
    config_yaml = os.path.join(workspace, "workflow.yaml")
    with open(config_yaml, 'r') as f:
        settings = yaml.safe_load(f)
    print(f"Configuration is {settings}")
    if not os.path.exists(os.path.join(workspace, 'EDA')):
        raise FileNotFoundError(f"No EDA folder under {workspace}, please execute pipeline first")

    params = {
        'boosting_type':'gbdt',
        'objective': 'regression',
        'nthread': 4,
        'num_leaves': 31,
        'learning_rate': 0.05,
        'max_depth': -1,
        'subsample': 0.8,
        'bagging_fraction' : 1,
        'max_bin' : 5000 ,
        'bagging_freq': 20,
        'colsample_bytree': 0.6,
        'metric': 'rmse',
        'min_split_gain': 0.5,
        'min_child_weight': 1,
        'min_child_samples': 10,
        'scale_pos_weight':1,
        'zero_as_missing': True,
        'seed':0,
        'num_rounds':2000,
        'num_boost_round': 2000,
        'early_stopping_rounds': 50
    }

    if cfg.train:
        transformed_data = pd.read_parquet(os.path.join(workspace, 'transformed_train_data.parquet'))
        test_sample = transformed_data.sample(frac = 0.1)
        train_sample = transformed_data.drop(test_sample.index)

        x_train = train_sample.drop(columns=['fare_amount'])
        y_train = train_sample['fare_amount'].values
        x_val = test_sample.drop(columns=['fare_amount'])
        y_val = test_sample['fare_amount'].values
        lgbm_train = lgbm.Dataset(x_train, y_train, silent=False)
        lgbm_val = lgbm.Dataset(x_val, y_val, silent=False)

        model = lgbm.train(params=params, train_set=lgbm_train, valid_sets=lgbm_val, verbose_eval=100)
        model.save_model(os.path.join(workspace, 'lgbm_model'))
    else:
        transformed_data = pd.read_parquet(os.path.join(workspace, 'transformed_test_data.parquet'))
        x_val = transformed_data.drop(columns=['fare_amount'])
        y_val = transformed_data['fare_amount'].values
        lgbm_val = lgbm.Dataset(x_val, y_val, silent=False)
        model = lgbm.Booster(model_file=os.path.join(workspace, 'lgbm_model'))
        pred = model.predict(x_val)
        rmse = np.sqrt(mean_squared_error(y_val, pred))
        print('Test dataset RMSE', rmse)


def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default=None, help='AutoFE workspace')
    parser.add_argument('--train', type=bool, default=False, help='Train/Test flag')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    if cfg.workspace is None:
        cfg.workspace = os.path.join(pathlib, "workspace")
    run(cfg)