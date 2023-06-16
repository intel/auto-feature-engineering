Twitter Recsys demo data

* Download raw data
internal share only

* config workflow.yaml
```
dataset_path: ./raw_data/twitter_recsys.csv
target_label: reply
engine_type: twitter
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/twitter_recsys autofe-notebook-UI
```