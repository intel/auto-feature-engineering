NYC Taxi Fare Prediction demo data

* Download raw data
We use [kaggle API](https://github.com/Kaggle/kaggle-api) to download dataset, you can also download [dataset](https://www.kaggle.com/competitions/new-york-city-taxi-fare-prediction/data) manually. 
```
pip install kaggle==1.5.3
apt install unzip

export KAGGLE_USERNAME=${your_kaggle_username}
export KAGGLE_KEY=${your_kaggle_key}
export KAGGLE_PROXY=${your_proxy}

# download NYC taxi dataset, usually took ~2 mins
cd ${AUTOFE_WORKSPACE}/applications/nyc_taxi_fare/; mkdir -p raw_data; cd raw_data;
kaggle competitions download -c new-york-city-taxi-fare-prediction; unzip new-york-city-taxi-fare-prediction.zip
```

* config workflow.yaml
```
dataset_path: ./raw_data/train.csv
target_label: fare_amount
engine_type: spark
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/nyc_taxi_fare autofe-notebook-UI
```