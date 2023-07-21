from pathlib import Path
import os
from tqdm import tqdm
#import warnings
#warnings.filterwarnings('ignore')
pathlib = str(Path(__file__).parent.parent.resolve())

from pyrecdp.autofe import FeatureWrangler
from pyrecdp.core.utils import Timer
import pandas as pd
import yaml
import shutil
import argparse

def auto_fe(train_data, label, engine_type):
    
    return transformed_data

def run(cfg):
    workspace = cfg.workspace
    # *** Prepare ***
    config_yaml = os.path.join(workspace, "workflow.yaml")
    with open(config_yaml, 'r') as f:
        settings = yaml.safe_load(f)
        
    print(f"Configuration is {settings}")

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        os.mkdir(os.path.join(workspace, 'EDA'))
    
    # *** Read Data ***
    if cfg.train:
        df = pd.read_parquet(os.path.join(workspace, 'train_sample.parquet'))
    else:
        df = pd.read_parquet(os.path.join(workspace, 'test_sample.parquet'))
    train_data = df
    
    # *** call autofe ***
    engine_type = settings['engine_type'] if 'engine_type' in settings else 'pandas'
    pipeline = FeatureWrangler(dataset=train_data, label=settings['target_label'])
    pipeline.import_from_json(os.path.join(workspace, 'EDA', 'pipeline.json'))
    transformed_data = pipeline.fit_transform(engine_type = engine_type)
    # *** save results ***
    if cfg.train:
        transformed_data.to_parquet(os.path.join(workspace, 'transformed_train_data.parquet'))
    else:
        transformed_data.to_parquet(os.path.join(workspace, 'transformed_test_data.parquet'))
    # *** prepare EDA ***
    original_shape = train_data.shape
    if train_data.shape[0] > 10000:
        transformed_data.iloc[:10000].to_csv(os.path.join(workspace, 'EDA', 'transformed_data_sample.csv'), index = False)
    else:
        transformed_data.to_csv(os.path.join(workspace, 'EDA', 'transformed_data_sample.csv'), index = False)
    shutil.copyfile(
        os.path.join(pathlib, 'assets', 'UI_notebook.ipynb'), 
        os.path.join(workspace, 'EDA', 'UI_notebook.ipynb'))  
    
    # *** final print ***
    print("\n************ Completed! ************")
    print(f"original data shape is {original_shape}, after transformed data shape is {transformed_data.shape}")
    print(f"Transformed Data and EDA analysis are saved in your workspace")
    print("\n".join([f"\t{i}" for i in os.listdir(workspace)]))
    print("EDA folder:")
    print("\n".join([f"\t{i}" for i in os.listdir(os.path.join(workspace, 'EDA'))]))
    print(f"Please visit EDA/UI_notebook.ipynb for details")
    print("**************************************\n")

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
