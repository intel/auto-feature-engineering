## LGBM Training
`lgbm train` library uses transformed dataset to train a LightGBM model.

## Input Arguments:
* `--workspace`: AutoFE workspace, eg. `/cnvrg/applications/nyc_taxi_fare/`
* `--target_label`: Target label of dataset
* `--train`: Set true for training pipeline and false for test pipeline
* `--input_file`: Dataset location
* `--pipeline_output`: AutoFE pipeline output dir