from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from inception_db_connect.settings_db_connect import get_db_connect_setting
import logging
from inception_db_connect.helper import mask_url

logger = logging.getLogger("sqlalchemy.db")
logger.setLevel(logging.INFO)
logger.propagate = True

# Retrieve settings
db_connect_setting = get_db_connect_setting()

if not db_connect_setting.postgres_url or not db_connect_setting.postgres_database:
    logger.error(
        "❌ Environment misconfiguration: 'postgres_url' and 'postgres_database' must be set."
    )
    raise ValueError(
        "Both 'postgres_url' and 'postgres_database' environment variables must be set."
    )

SQLALCHEMY_DATABASE_URL = (
    f"{db_connect_setting.postgres_url}/{db_connect_setting.postgres_database}"
)

logger.info(f"🐘 Connecting to PostgreSQL: {mask_url(SQLALCHEMY_DATABASE_URL)}")

# Set up engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    engine.connect()
    logger.info("✅ Successfully connected to PostgreSQL!")
except Exception as e:
    logger.error("❌ Failed to connect to PostgreSQL.")
    raise ConnectionError(f"PostgreSQL connection failed: {e}")


# Dependency (e.g., for FastAPI)
def get_pg_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_pg_db_on_demand():
    db = SessionLocal()
    return db
