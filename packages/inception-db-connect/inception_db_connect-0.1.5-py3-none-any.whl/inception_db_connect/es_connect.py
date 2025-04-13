from elasticsearch import Elasticsearch
from inception_db_connect.settings_db_connect import get_db_connect_setting
from inception_db_connect.helper import mask_url
import logging

logger = logging.getLogger("elasticsearch")
logger.setLevel(logging.INFO)
logger.propagate = True


# Get settings
db_connect_setting = get_db_connect_setting()
logger.info(
    f"📡 Connecting to Elasticsearch at: {mask_url(db_connect_setting.elasticsearch_url)}"
)

# Connect to ES
es = Elasticsearch(db_connect_setting.elasticsearch_url)

# ✅ Confirm connection
if es.ping():
    logger.info("✅ Successfully connected to Elasticsearch!")
else:
    logger.error("❌ Failed to connect to Elasticsearch.")
    raise ConnectionError("Could not connect to Elasticsearch.")


def get_es_client():
    return es
