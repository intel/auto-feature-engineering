from pathlib import Path
import os
from tqdm import tqdm
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
    target_label = cfg.target_label
    input_file = cfg.input_file
    print(f"Configuration is {cfg}")

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        os.mkdir(os.path.join(workspace, 'EDA'))
    
    df = pd.read_parquet(input_file)
    train_data = df

    # *** Save original data sample ***    
    original_shape = train_data.shape
    if train_data.shape[0] > 10000:
        train_data.iloc[:10000].to_csv(os.path.join(workspace, 'EDA', 'original_data_sample.csv'), index = False)
    else:
        train_data.to_csv(os.path.join(workspace, 'EDA', 'original_data_sample.csv'), index = False)
    
    # *** generate pipeline ***
    pipeline = FeatureWrangler(dataset=train_data, label=target_label)
    pipeline.export(os.path.join(workspace, 'EDA', 'pipeline.json'))

def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default="output", help='AutoFE workspace')
    parser.add_argument('--target_label', type=str, default="fare_amount", help='Dataset target label')
    parser.add_argument('--input_file', type=str, default=None, help='Dataset location')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)