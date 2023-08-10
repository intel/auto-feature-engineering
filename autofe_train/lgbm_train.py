from pathlib import Path
import os
import pandas as pd
import yaml
import argparse
import pandas as pd
from sklearn.metrics import mean_squared_error
import lightgbm as lgbm
import numpy as np
import shutil
pathlib = str(Path(__file__).parent.parent.resolve())


def run(cfg):
    workspace = cfg.workspace
    target_label = cfg.target_label
    input_file = cfg.input_file
    print(f"Configuration is {cfg}")

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

    if str(cfg.train).lower() == 'true':
        print("Train")
        transformed_data = pd.read_parquet(input_file)
        test_sample = transformed_data.sample(frac = 0.1)
        train_sample = transformed_data.drop(test_sample.index)

        x_train = train_sample.drop(columns=[target_label])
        y_train = train_sample[target_label].values
        x_val = test_sample.drop(columns=[target_label])
        y_val = test_sample[target_label].values
        lgbm_train = lgbm.Dataset(x_train, y_train, silent=False)
        lgbm_val = lgbm.Dataset(x_val, y_val, silent=False)

        model = lgbm.train(params=params, train_set=lgbm_train, valid_sets=lgbm_val, verbose_eval=100)
        model.save_model(os.path.join(workspace, 'lgbm_model'))
        shutil.copy(input_file, os.path.join(workspace, 'transformed_train_data.parquet'))
    else:
        transformed_data = pd.read_parquet(input_file)
        x_val = transformed_data.drop(columns=[target_label])
        y_val = transformed_data[target_label].values
        lgbm_val = lgbm.Dataset(x_val, y_val, silent=False)
        model = lgbm.Booster(model_file=os.path.join(workspace, 'lgbm_model'))
        pred = model.predict(x_val)
        rmse = np.sqrt(mean_squared_error(y_val, pred))
        print('Test dataset RMSE', rmse)
        
        shutil.copy(input_file, os.path.join(workspace, 'transformed_test_data.parquet'))
        shutil.copy(os.path.join(cfg.pipeline_output, 'EDA', 'pipeline.json'), os.path.join(workspace, 'pipeline.json'))

        print("To obtain transformed data and feature engineering pipeline, please go to Files -> output.")


def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default="output", help='AutoFE workspace')
    parser.add_argument('--target_label', type=str, default="fare_amount", help='Dataset target label')
    parser.add_argument('--train', type=str, default='False', help='Train/Test flag')
    parser.add_argument('--input_file', type=str, default=None, help='Dataset location')
    parser.add_argument('--pipeline_output', type=str, default=None, help='AutoFE pipeline output dir')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)