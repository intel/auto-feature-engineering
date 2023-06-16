Outbrain Click Through Rate demo data

* Download raw data
We use [kaggle API](https://github.com/Kaggle/kaggle-api) to download dataset, you can also download [dataset](https://www.kaggle.com/competitions/outbrain-click-prediction/data) manually. 
```
pip install kaggle==1.5.3
apt install unzip

export KAGGLE_USERNAME=${your_kaggle_username}
export KAGGLE_KEY=${your_kaggle_key}
export KAGGLE_PROXY=${your_proxy}

# download Outbrain Click Through Rate dataset
cd ${AUTOFE_WORKSPACE}/applications/outbrain_ctr/; mkdir -p raw_data; cd raw_data;
kaggle competitions download -c outbrain-click-prediction
for file in `ls *.zip`; do unzip $file; done
```

* config workflow.yaml
```
dataset_path_dict:
  clicks: ./raw_data/clicks_train.csv
  documents_categories: ./raw_data/documents_categories.csv
  documents_entities: ./raw_data/documents_entities.csv
  documents_meta: ./raw_data/documents_meta.csv
  documents_topics: ./raw_data/documents_topics.csv
  events: ./raw_data/events.csv
  page_views: ./raw_data/page_views_sample.csv
  promoted_content: ./raw_data/promoted_content.csv
target_label: clicked
engine_type: spark
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/outbrain_ctr autofe-notebook-UI
```