import os
import shutil
import argparse
from urllib.parse import urlparse
import requests
from tqdm import tqdm
import shutil
import pandas as pd

def load_csv_to_pandasdf(dataset):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files.endswith("csv"):
            return None
        df = pd.read_csv(dataset + "/" + input_files[0])
        for file in tqdm(input_files[1:]):
            part = pd.read_csv(dataset + "/" + file)    
            df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("csv"):
            return None
        df = pd.read_csv(dataset)
    return df

def load_parquet_to_pandasdf(dataset):
    if os.path.isdir(dataset):
        input_files = sorted(os.listdir(dataset))
        if len(input_files) == 0 or not input_files.endswith("parquet"):
            return None
        df = pd.read_parquet(dataset + "/" + input_files[0])
        for file in tqdm(input_files[1:]):
            part = pd.read_parquet(dataset + "/" + file)    
            df = pd.concat([df, part],axis=0)
    else:
        if not dataset.endswith("parquet"):
            return None
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

def fetch_data(dataset_path):
    output_dir = "output/"
    if dataset_path.startswith("https://"):
        a = urlparse(dataset_path)
        to_save = os.path.join(output_dir, os.path.basename(a.path))
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
    if not os.path.exists(to_save):
        raise FileNotFoundError(f"{to_save} is not exists.")
    # if file is parquet
    df = load_parquet_to_pandasdf(to_save)
    if df is None:
        # if file is csv
        df = load_csv_to_pandasdf(to_save)
    if df is None:
        # if file is tsv
        df = load_tsv_to_pandasdf(to_save)
    if df is None:
        raise ValueError(f"can't read {to_save} either as parquet or csv.")
    
    to_save = os.path.join(output_dir, "dataset_cache.parquet")
    df.to_parquet(to_save)
    print(f"Data is fetched to {to_save}")
    
    return

def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--url', type=str, default=None, help='url used to fetch your data')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    if cfg.url is None:
        raise ValueError("Please specify your data url")
    fetch_data(cfg.url)
    #fetch_data("https://cnvrg-s3-singularity.s3.us-east-2.amazonaws.com/data_blob_versions/assets/000/154/111/original/sample.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA4WNH6RXCL3BT53UG%2F20230727%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230727T163249Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCIQD0WdmMu%2BQvJ7KvZu%2FuIqZbLfU%2FAbnj6%2B7nB3VS86z0dQIgXDkoRNDPvgff9tJsDxN73GXeHG3veGE2umZsd2r3KasqogIIYhACGgw4NzI3Njc0NTg3NTYiDFG8Pi7T1DejWmHwuSr%2FATE3Pr0Jp%2F2qzdqHCSTfXlaQ4dlpqiq%2FHffVYyvDYqA8cgADpZ7Cljl5F7jXiLO2DbF7ZZwzpH8RfrraeuycJb2Rax9jrnbF%2Ft0J4tmIJ0%2FmcD0rRd0VozCKpCehga3SmZz2X61vvV65IGRqUlR7FRVrajAIOaoYKIDdtHUVh2BNdQTTEoaOIppAPNHH5edluVOFn3r5yNxfadnYyxld%2BAs9hLB%2Fh1oaHQnE4eqpb8s3ExBVN6%2B3fVbgPTqqqFlhMAJib8LXEX33lJN86wqB43%2B95Xn9B2AvVs0dBY4XcW5HrKmhG7zni956oGzJuIVuHEPp9VsOi5SGJxyKc3MusjCxuIqmBjqdAZhGvSALtDXWLSWZRSN3wBehXyuNmyFfnT76GcLR3HuM7XgOf7mDlYnFh6u3BQdmjD5P%2FXTtLzwDVPPR8DSHCKEz66JT8m0txVtdiH6sFji2ccO5qxMLzBzDonaUlih1jmh58wqrRwiRE1vslqzECEqVGEdDIOZBkUWXppYF20O4hDX7kUeKA2NIdQQxhOhnfRbnOFAjz78eQ7x5Quo%3D&X-Amz-SignedHeaders=host&X-Amz-Signature=91518e6089c7063cde0498d4662634b13ba757865ca6fefec4ba410c936843fd")
    