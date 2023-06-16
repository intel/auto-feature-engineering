CDP Covid TabularUtils demo data

* prepare application folder
```
mkdir ${AUTOFE_WORKSPACE}/applications/cdp_tabular_utils/
cd ${AUTOFE_WORKSPACE}/applications/cdp_tabular_utils/
```

* download data and third_party 'TabularUtils' package
```
git clone https://github.com/intel-sandbox/tabutils.git

mkdir -p raw_data
cd raw_data
cp tabutils/Covid_19_ICU_prediction.csv raw_data/Covid_19_ICU_prediction.csv
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
make workspace=`pwd`/applications/cdp_tabular_utils autofe-notebook-UI
```