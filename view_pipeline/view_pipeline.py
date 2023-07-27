from pathlib import Path
import os
from pyrecdp.autofe import FeatureWrangler
import pandas as pd
import yaml
import argparse


def run(cfg):
    workspace = cfg.workspace
    target_label = cfg.target_label
    print(f"Configuration is {cfg}")
    if not os.path.exists(os.path.join(workspace, 'EDA')):
        raise FileNotFoundError(f"No EDA folder under {workspace}, please execute pipeline first")

    pipeline = FeatureWrangler(os.path.join(workspace, 'train_sample.parquet'), target_label)
    pipeline.import_from_json(os.path.join(workspace, 'EDA', 'pipeline.json'))
    graph = pipeline.plot()
    print(graph)


def parse_args():
    parser = argparse.ArgumentParser('AutoFE-Workflow')
    parser.add_argument('--workspace', type=str, default="output", help='AutoFE workspace')
    parser.add_argument('--target_label', type=str, default="target_amount, help='Dataset target label')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)