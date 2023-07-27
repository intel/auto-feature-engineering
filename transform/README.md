## Data Transform
`data transform` library will load generated AutoFE pipeline and execute the whole pipeline for data transformation.

## Input Arguments:
* `--workspace`: AutoFE workspace, eg. `/cnvrg/applications/nyc_taxi_fare/`
* `--target_label`: Target label of dataset
* `--engine_type`: AutoFE execution engine, options [pandas, spark]
* `--train`: Set true for training pipeline and false for test pipeline