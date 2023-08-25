Segmentation TabularUtils demo data

* prepare application folder
```
mkdir ${AUTOFE_WORKSPACE}/applications/segmentation_tabutils/
cd ${AUTOFE_WORKSPACE}/applications/segmentation_tabutils/
```

* config workflow.yaml
```
dataset_path: ./raw_data/test_data.csv
target_label: None
engine_type: pandas
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/segmentation_tabutils autofe-notebook-UI
```