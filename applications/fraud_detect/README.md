Fraud Detection demo data

* Download raw data
```
cd ${AUTOFE_WORKSPACE}/applications/fraud_detect/
mkdir -p raw_data
cd raw_data
```

download data from https://ibm.box.com/v/tabformer-data to `raw_data`, 
expected saved file is 'transactions.tgz', 
untar tgz as card_transaction.v1.csv
```
tar zxvf transactions.tgz
```

* config workflow.yaml
```
dataset_path: ./raw_data/card_transaction.v1.csv
target_label: 'Is Fraud?'
engine_type: pandas
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/fraud_detect autofe-notebook-UI
```