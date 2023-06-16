Predictive Assets Maintenance demo data

* Download raw data
We use [kaggle API](https://github.com/Kaggle/kaggle-api) to download dataset, you can also download [dataset](https://www.kaggle.com/datasets/shivamb/elevator-predictive-maintenance-dataset) manually.

```
mkdir ${AUTOFE_WORKSPACE}/applications/predictive_assets_maintenance/
cd ${AUTOFE_WORKSPACE}/applications/predictive_assets_maintenance/
mkdir -p raw_data;
cd raw_data; unzip predictive-maintenance-dataset.csv.zip; cd ..
```

* config workflow.yaml
```
dataset_path: ./raw_data/predictive-maintenance-dataset.csv
target_label: vibration
engine_type: pandas
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/predictive_assets_maintenance autofe-notebook-UI
```