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

def load_parquet_to_pandasdf(dataset):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files.endswith("parquet"):
            return None
        with Timer(f"Read {dataset}"):
            df = pd.read_parquet(dataset + "/" + input_files[0])
            for file in tqdm(input_files[1:]):
                part = pd.read_parquet(dataset + "/" + file)    
                df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("parquet"):
            return None
        with Timer(f"Read {dataset}"):
            df = pd.read_parquet(dataset)
    return df

def run(cfg):
    workspace = cfg.workspace
    # *** Prepare ***
    config_yaml = os.path.join(workspace, "workflow.yaml")
    with open(config_yaml, 'r') as f:
        settings = yaml.safe_load(f)
        
    print(f"Configuration is {settings}")

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        os.mkdir(os.path.join(workspace, 'EDA'))
    
    df = pd.read_parquet(os.path.join(workspace, 'train_sample.parquet'))
    train_data = df

    # *** Save original data sample ***    
    original_shape = train_data.shape
    if train_data.shape[0] > 10000:
        train_data.iloc[:10000].to_csv(os.path.join(workspace, 'EDA', 'original_data_sample.csv'), index = False)
    else:
        train_data.to_csv(os.path.join(workspace, 'EDA', 'original_data_sample.csv'), index = False)
    
    # *** generate pipeline ***
    engine_type = settings['engine_type'] if 'engine_type' in settings else 'pandas'
    pipeline = FeatureWrangler(dataset=train_data, label=settings['target_label'])
    pipeline.export(os.path.join(workspace, 'EDA', 'pipeline.json'))

def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default=None, help='AutoFE workspace')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    if cfg.workspace is None:
        cfg.workspace = os.path.join(pathlib, "workspace")
    run(cfg)