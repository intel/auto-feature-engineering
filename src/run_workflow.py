from pathlib import Path
import os
from tqdm import tqdm
#import warnings
#warnings.filterwarnings('ignore')
# pathlib = str(Path(__file__).parent.parent.resolve())
# workspace = os.path.join(pathlib, "workspace")

from pyrecdp.autofe import FeatureWrangler
from pyrecdp.core.utils import Timer
import pandas as pd
import yaml
import shutil
import argparse

def auto_fe(train_data, label, engine_type):
    pipeline = FeatureWrangler(dataset=train_data, label=label)
    transformed_data = pipeline.fit_transform(engine_type = engine_type)
    return pipeline, transformed_data

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
    pathlib = str(Path(cfg.workspace).parent.parent.resolve())
    workspace = cfg.workspace
    # *** Prepare ***
    config_yaml = os.path.join(workspace, "workflow.yaml")
    with open(config_yaml, 'r') as f:
        settings = yaml.safe_load(f)
        
    print(f"Configuration is {settings}")

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        os.mkdir(os.path.join(workspace, 'EDA'))
    
    # *** Read Data ***
    if not os.path.exists(os.path.join(workspace, settings['dataset_path'])):
        raise FileNotFoundError(f"{settings['dataset_path']} is not exists.")
    # if file is parquet
    df = load_parquet_to_pandasdf(os.path.join(workspace, settings['dataset_path']))
    if df is None:
        # if file is csv
        df = load_csv_to_pandasdf(os.path.join(workspace, settings['dataset_path']))
    if df is None:
        # if file is tsv
        df = load_tsv_to_pandasdf(os.path.join(workspace, settings['dataset_path']))
    if df is None:
        raise ValueError(f"can't read {settings['dataset_path']} either as parquet or csv.")
    train_data = df
        
    # *** Save original data sample ***    
    original_shape = train_data.shape
    if train_data.shape[0] > 10000:
        train_data.iloc[:10000].to_csv(os.path.join(workspace, 'EDA', 'original_data_sample.csv'), index = False)
    else:
        train_data.to_csv(os.path.join(workspace, 'EDA', 'original_data_sample.csv'), index = False)
        
    # *** call autofe ***
    engine_type = settings['engine_type'] if 'engine_type' in settings else 'pandas'
    pipeline, transformed_data = auto_fe(train_data, settings['target_label'], engine_type)    
    
    # *** save results ***
    transformed_data.to_parquet(os.path.join(workspace, 'transformed_data.parquet'))

    # *** prepare EDA ***
    pipeline.export(os.path.join(workspace, 'EDA', 'pipeline.json'))
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
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    if cfg.workspace is None:
        pathlib = str(Path(__file__).parent.parent.resolve())
        cfg.workspace = os.path.join(pathlib, "workspace")
    run(cfg)
