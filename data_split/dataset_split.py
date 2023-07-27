from pathlib import Path
import os
import pandas as pd
import yaml
import shutil
import argparse

def run(cfg):
    workspace = cfg.workspace
    dataset_path = "dataset_cache.parquet"
    print(f"Configuration is {cfg}")

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        os.mkdir(os.path.join(workspace, 'EDA'))
    
    # *** Read Data ***
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"{dataset_path} is not exists.")
    df = df = pd.read_parquet(dataset_path)
    total_len = df.shape[0]
    test_len = int(total_len * 0.1)
    test_sample = df.iloc[-test_len:]
    train_sample = df.drop(test_sample.index)
    train_sample.to_parquet(os.path.join(workspace, 'train_sample.parquet'))
    test_sample.to_parquet(os.path.join(workspace, 'test_sample.parquet'))

def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default="output", help='AutoFE workspace')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)