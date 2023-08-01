# Auto Feature Engineering Blueprint
Auto Feature Engineering helps to shorten the time required for data scientists to process and transform large-scale raw tabular dataset to ready-to-train features, reducing the necessity of human domain-specific knowledge to explore and identify new useful features, and thus enabling data scientists to be able to focus and iterate on the rest stages of the E2E AI pipelines more efficiently.

The Blueprint leverages Intel Auto-Feature-Engineering toolkit (codename: RecDP) to automatically transform raw tabular data to enriched useful new features on pluggable execution engine such as Pandas and Spark, with the capability of integrating 3rd party feature engineering primitives, and thus significantly improve developer productivity and efficiency.

## How to Use:
### [CNVRG IO Flows]
> Note: you can experience the workflow step by step and view each step logs and results.
* How to Execute: Flows -> AutoFE -> click ‘Run’
* How to view results: Files -> click ‘output’ folder.
![image](https://github.com/intel/auto-feature-engineering/assets/4355494/01dc58c6-c6d7-4eaf-a45c-24548964d023)

* Step by step explanation:
    1) fetch data: default config will use sampled NYC taxi fare dataset. You can also specify your own dataset by providing dataset public URL.
    2) train test split: use random select to select train and test by 9:1
    3) AutoFE create pipeline: analyze train data and automatically create data pipeline, data pipeline will be saved as ‘pipeline.json’ to your ‘Files’. E.g.: If datetime features detected, datetime will be transformed to ‘day’, ‘hour’…  
    4) fit transform train: execute pre-generated data pipeline to train dataset.
    5) transform test: execute pre-generated data pipeline to test dataset.
    6) train: using LightGBM to train on transformed train data
    7) test: using transformed test data to do prediction validation with step6 trained model.

### [CNVRG IO Serving]
> Note: You can use public dataset url to test to get Auto Feature Engineered result
* How to execute: Serving -> Try it Live -> Execute
  ![image](https://github.com/intel/auto-feature-engineering/assets/4355494/985db1cb-1284-41e5-b381-830600336272)

* How to use your own data:
Following this format to do input <code>{"dataset_path": "$your_dataset_url", "target_label": "$your_target"}</code>

Example as below:
![image](https://github.com/intel/auto-feature-engineering/assets/4355494/239c4a27-c9dc-4ceb-9ca2-5f13f0951dff)




