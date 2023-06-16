import os
from tqdm import tqdm
workspace = "/home/vmagent/app/workspace/"

from pyrecdp.core.utils import Timer
import pandas as pd
import yaml

def get_load_function(dataset, lazy_load):
    data_type = None
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0:
            pass
        elif input_files[0].endswith("csv"):
            data_type = 'csv'
        elif input_files[0].endswith("parquet"):
            data_type = 'parquet'
        elif input_files[0].endswith("tsv"):
            data_type = 'tsv'
    else:
        if dataset.endswith("csv"):
            data_type = 'csv'
        elif dataset.endswith("parquet"):
            data_type = 'parquet'
        elif dataset.endswith("tsv"):
            data_type = 'tsv'
            
    if data_type == 'csv':
        def load_data(nrows = -1):
            return load_csv_to_pandasdf(dataset, nrows=nrows, lazy_load=lazy_load)
        return load_data
    if data_type == 'parquet':
        def load_data(nrows = -1):
            return load_parquet_to_pandasdf(dataset, lazy_load=lazy_load)
        return load_data
    if data_type == 'tsv':
        def load_data(nrows = -1):
            return load_tsv_to_pandasdf(dataset, lazy_load=lazy_load)
        return load_data
    return None

def get_load_dict_function(dataset_dict, lazy_load):
    ret = dict()
    for f_name, f_path in dataset_dict.items():
        ret[f_name] = get_load_function(os.path.join(workspace, f_path), lazy_load)
    def load_data(nrows = -1):
        return dict((f_name, ld_func(nrows)) for f_name, ld_func in ret.items())
    return load_data
      
def load_csv_to_pandasdf(dataset, nrows=-1, lazy_load=False):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files[0].endswith("csv"):
            return None
        if lazy_load:
            return input_files
        with Timer(f"Read {dataset}"):
            df = pd.read_csv(dataset + "/" + input_files[0])
            for file in tqdm(input_files[1:]):
                if nrows != -1:
                    part = pd.read_csv(dataset + "/" + file, nrows = nrows)
                else:
                    part = pd.read_csv(dataset + "/" + file)
                df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("csv"):
            return None
        if lazy_load:
            return dataset
        with Timer(f"Read {dataset}"):
            if nrows != -1:
                df = pd.read_csv(dataset, nrows = nrows)
            else:
                df = pd.read_csv(dataset)
    return df

def load_parquet_to_pandasdf(dataset, nrows=-1, lazy_load=False):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files[0].endswith("parquet"):
            return None
        if lazy_load:
            return input_files
        with Timer(f"Read {dataset}"):
            df = pd.read_parquet(dataset + "/" + input_files[0])
            for file in tqdm(input_files[1:]):
                part = pd.read_parquet(dataset + "/" + file)    
                df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("parquet"):
            return None
        if lazy_load:
            return dataset
        with Timer(f"Read {dataset}"):
            df = pd.read_parquet(dataset)
    return df

def load_tsv_to_pandasdf(dataset, nrows=-1, lazy_load=False):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files[0].endswith("tsv"):
            return None
        if lazy_load:
            return input_files
        with Timer(f"Read {dataset}"):
            df = pd.read_table(dataset + "/" + input_files[0])
            for file in tqdm(input_files[1:]):
                part = pd.read_table(dataset + "/" + file, on_bad_lines="skip")    
                df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("tsv"):
            return None
        if lazy_load:
            return dataset
        with Timer(f"Read {dataset}"):
            df = pd.read_table(dataset, on_bad_lines="skip")
    return df

# *** Prepare ***
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

config_yaml = os.path.join(workspace, "workflow.yaml")
with open(config_yaml, 'r') as f:
    settings = yaml.safe_load(f)
if 'lazy_load' not in settings:
    settings['lazy_load'] = False
    
print(f"Configuration is {settings}")
print("start up executed")
if 'dataset_path' in settings:
    load_data = get_load_function(os.path.join(workspace, settings['dataset_path']), settings['lazy_load'])
elif 'dataset_path_dict' in settings:
    load_data = get_load_dict_function(settings['dataset_path_dict'], settings['lazy_load'])
else:
    def load_data(nrows = -1):
        print("In correct configuration, not be able to load data")
        return None
engine_type = settings['engine_type'] if 'engine_type' in settings else 'pandas'
target_label = settings['target_label']