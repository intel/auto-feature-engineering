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
from urllib.parse import urlparse
import requests
from tqdm import tqdm
import shutil
import json
import io

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)

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

def predict(*input):
    return str(input)

def prepare_dataframe(dataset_path):
    workspace = ""
    if dataset_path.startswith("https://"):
        a = urlparse(dataset_path)
        to_save = os.path.basename(a.path)
        print(to_save)
        if not os.path.exists(to_save):
            with requests.get(dataset_path, stream=True) as r:
                # check header to get content length, in bytes
                total_length = int(r.headers.get("Content-Length"))
                # implement progress bar via tqdm
                with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw: 
                    # save the output to a file
                    with open(f"{to_save}", 'wb')as output:
                        shutil.copyfileobj(raw, output)
    else:
        to_save = dataset_path

    # *** Read Data ***
    if not os.path.exists(os.path.join(workspace, to_save)):
        raise FileNotFoundError(f"{to_save} is not exists.")
    # if file is parquet
    df = load_parquet_to_pandasdf(os.path.join(workspace, to_save))
    if df is None:
        # if file is csv
        df = load_csv_to_pandasdf(os.path.join(workspace, to_save))
    if df is None:
        # if file is tsv
        df = load_tsv_to_pandasdf(os.path.join(workspace, to_save))
    if df is None:
        raise ValueError(f"can't read {to_save} either as parquet or csv.")
    return df

def load_setting(cfg):
    try:
        setting = json.loads(cfg)    
        if "engine_type" not in setting:
            setting['engine_type'] = "pandas"
        dataset_path, target_label, engine_type = setting['dataset_path'], setting['target_label'], setting['engine_type']
    except:
        ret = "Input Format Error, please follow example to provide data\n"
        ret += '{"dataset_path": "sample.csv", "target_label": "fare_amount"}\n'
        ret += f'We received input as {cfg}\n'
        raise ValueError(ret)
    return dataset_path, target_label, engine_type

def predict(data):
    workspace = ""
    cfg = data['vars']
    try:
        dataset_path, target_label, engine_type = load_setting(cfg)
    except Exception as e:
        return str(e)
    with open('workflow.yaml', 'w') as f:
        f.write(cfg)
    
    try:
        train_data = prepare_dataframe(dataset_path)

        original_shape = train_data.shape
        original_columns = train_data.columns

        # *** call autofe ***
        pipeline, transformed_data = auto_fe(train_data, target_label, engine_type)   
        
        # *** save results ***
        transformed_data.to_parquet(os.path.join(workspace, 'transformed_data.parquet'))
        new_features = [i for i in transformed_data.columns if i not in original_columns]
        new_features = transformed_data[new_features]
        
        buffer = io.StringIO()
        new_features.info(verbose=True, buf=buffer)
        new_features_s = buffer.getvalue()

        buffer = io.StringIO()
        print(train_data, file=buffer)
        original_train_data = buffer.getvalue()

        buffer = io.StringIO()
        print(transformed_data, file=buffer)
        transformed_train_data = buffer.getvalue()

    except Exception as e:
        ret = f"Failed. Error msg is {e}"
        return ret
    
    ret = ""
    # *** final print ***
    ret += "\n************ Completed! ************\n"
    ret += f"original data shape is {original_shape}, \nafter transformed data shape is {transformed_data.shape}\n"
    ret += f"original data is \n{original_train_data}\n"
    ret += f"transformed data is \n{transformed_train_data}\n"
    ret += f"new created features are {new_features_s}\n"
    ret += f"transformed data is stored as {os.path.join(workspace, 'transformed_data.parquet')}\n"
    ret += "**************************************\n"
    print(ret)

    return ret
