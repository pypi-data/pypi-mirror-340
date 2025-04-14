from elasticsearch import Elasticsearch
from inception_db_connect.settings_db_connect import get_db_connect_setting
from inception_db_connect.helper import mask_url


# Get settings
db_connect_setting = get_db_connect_setting()
print(
    f"📡 Connecting to Elasticsearch at: {mask_url(db_connect_setting.elasticsearch_url)}"
)

# Connect to ES
es = Elasticsearch(db_connect_setting.elasticsearch_url)

# ✅ Confirm connection
if es.ping():
    print("✅ Successfully connected to Elasticsearch!")
else:
    print("❌ Failed to connect to Elasticsearch.")
    raise ConnectionError("Could not connect to Elasticsearch.")


def get_es_client():
    return es
