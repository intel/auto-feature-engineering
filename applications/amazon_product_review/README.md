Amazon Product Review demo data

* Install pyrecdp
```
pip install pyrecdp --pre
cd ${AUTOFE_WORKSPACE}/applications/amazon_product_review/
mkdir -p raw_data
```

* Download raw data
``` python
from pyrecdp.datasets import amazon_product_review
df = amazon_product_review().to_pandas()
df.to_parquet("raw_data/amazon_product_review.parquet")
```

* config workflow.yaml
```
dataset_path: ./raw_data/amazon_product_review.parquet
target_label: star_rating
engine_type: spark
```

* run interactive notebook
```
cd applications.ai.frameworks.workflow.autofe/
make workspace=`pwd`/applications/amazon_product_review autofe-notebook-UI
```