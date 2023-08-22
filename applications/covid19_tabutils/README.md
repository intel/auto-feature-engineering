Covid TabularUtils demo data

* prepare application folder
```
mkdir ${AUTOFE_WORKSPACE}/applications/covid19_tabutils/
cd ${AUTOFE_WORKSPACE}/applications/covid19_tabutils/
```

* download dataset
https://www.kaggle.com/datasets/S%C3%ADrio-Libanes/covid19

```
mkdir -p raw_data
cd raw_data
cp covid19/Covid_19_ICU_prediction.csv raw_data/Covid_19_ICU_prediction.csv
```

* config workflow.yaml
```
dataset_path: ./raw_data/Covid_19_ICU_prediction.csv
target_label: ICU
engine_type: pandas
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/covid19_tabutils autofe-notebook-UI
```