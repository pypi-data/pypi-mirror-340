from pymongo import MongoClient, errors
from inception_db_connect.settings_db_connect import get_db_connect_setting
from inception_db_connect.helper import mask_url
import logging

# Set up logger
logger = logging.getLogger("db_connect.mongo")
logger.setLevel(logging.INFO)

# Retrieve settings
db_connect_setting = get_db_connect_setting()

# Validate MongoDB settings
if not db_connect_setting.mongodb_database or not db_connect_setting.mongodb_url:
    logger.error("❌ Environment misconfiguration: 'mongodb_database' and 'mongodb_url' must be set.")
    raise ValueError("Both 'mongodb_database' and 'mongodb_url' environment variables must be set.")

logger.info(
    f"🔌 Connecting to MongoDB...\n🌐 URL: {mask_url(db_connect_setting.mongodb_url)}\n📁 Database: {db_connect_setting.mongodb_database}"
)
client = MongoClient(db_connect_setting.mongodb_url)

try:
    client.admin.command("ping")
    logger.info("✅ Successfully connected to MongoDB!")
except errors.ServerSelectionTimeoutError as e:
    logger.error("❌ Failed to connect to MongoDB.")
    raise ConnectionError(f"MongoDB connection failed: {e}")

# MongoDB dependency for FastAPI
def get_mongo_db():
    db = client[db_connect_setting.mongodb_database]
    try:
        yield db
    finally:
        client.close()

# On-demand MongoDB access
def get_mongo_db_on_demand():
    db = client[db_connect_setting.mongodb_database]
    return db
