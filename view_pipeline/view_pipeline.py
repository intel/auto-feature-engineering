from pathlib import Path
import os
from pyrecdp.autofe import FeatureWrangler
import pandas as pd
import yaml
import argparse
pathlib = str(Path(__file__).parent.parent.resolve())


def run(cfg):
    workspace = cfg.workspace
    config_yaml = os.path.join(workspace, "workflow.yaml")
    with open(config_yaml, 'r') as f:
        settings = yaml.safe_load(f)
    print(f"Configuration is {settings}")
    if not os.path.exists(os.path.join(workspace, 'EDA')):
        raise FileNotFoundError(f"No EDA folder under {workspace}, please execute pipeline first")

    pipeline = FeatureWrangler(os.path.join(workspace, settings['dataset_path']), settings['target_label'])
    pipeline.import_from_json(os.path.join(workspace, 'EDA', 'pipeline.json'))
    graph = pipeline.plot()
    print(graph)


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