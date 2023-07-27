from pathlib import Path
import os
from tqdm import tqdm
from pyrecdp.core.utils import Timer
import pandas as pd
import yaml
import shutil
import argparse

def load_csv_to_pandasdf(dataset):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files.endswith("csv"):
            return None
        with Timer(f"Read {dataset}"):
            df = pd.read_csv(dataset + "/" + input_files[0])
            for file in tqdm(input_files[1:]):
                part = pd.read_csv(dataset + "/" + file)    
                df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("csv"):
            return None
        with Timer(f"Read {dataset}"):
            df = pd.read_csv(dataset)
    return df

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

def load_tsv_to_pandasdf(dataset):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files.endswith("tsv"):
            return None
        with Timer(f"Read {dataset}"):
            df = pd.read_table(dataset + "/" + input_files[0])
            for file in tqdm(input_files[1:]):
                part = pd.read_table(dataset + "/" + file, on_bad_lines="skip")    
                df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("tsv"):
            return None
        with Timer(f"Read {dataset}"):
            df = pd.read_table(dataset, on_bad_lines="skip")
    return df

def run(cfg):
    workspace = cfg.workspace
    dataset_path = cfg.dataset_path
    print(f"Configuration is {cfg}")

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        os.mkdir(os.path.join(workspace, 'EDA'))
    
    # *** Read Data ***
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"{dataset_path} is not exists.")
    # if file is parquet
    df = load_parquet_to_pandasdf(dataset_path)
    if df is None:
        # if file is csv
        df = load_csv_to_pandasdf(dataset_path)
    if df is None:
        # if file is tsv
        df = load_tsv_to_pandasdf(dataset_path)
    if df is None:
        raise ValueError(f"can't read {dataset_path} either as parquet or csv.")
    
    total_len = df.shape[0]
    test_len = int(total_len * 0.1)
    test_sample = df.iloc[-test_len:]
    train_sample = df.drop(test_sample.index)
    train_sample.to_parquet(os.path.join(workspace, 'train_sample.parquet'))
    test_sample.to_parquet(os.path.join(workspace, 'test_sample.parquet'))

def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default=None, help='AutoFE workspace')
    parser.add_argument('--dataset_path', type=str, default=None, help='Dataset location')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)