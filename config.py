import os

database_config = {
    "host": os.environ.get("DB_HOST", "placeholder"),
    "port": os.environ.get("DB_PORTS", 3306),
    "user": os.environ.get("DB_USER", "placeholder"),
    "password": os.environ.get("DB_PASSWORD", "placeholder"),
    "database": os.environ.get("DB_NAME", "placeholder"),
}

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "host": os.environ.get("FLASK_HOST", "0.0.0.0"),
    "port": os.environ.get("FLASK_PORT", 5000),
}



# Power BI config
SECRET_VALUE = os.environ.get("SECRET_VALUE", "my_secret")
CLIENT_ID = os.environ.get("CLIENT_ID", "placeholder")
TENANT_ID = os.environ.get("TENANT_ID", "placeholder")
DATASET_ID = os.environ.get("DATASET_ID", "placeholder")
DATASET_NAME = os.environ.get("DATASET_NAME", "placeholder")
POWER_BI_EMAIL = os.environ.get("POWER_BI_EMAIL", "placeholder")
POWER_BI_PASSWORD = os.environ.get("POWER_BI_PASSWORD", "placeholder")

# SplitWise config
GROUP_ID = os.environ.get("GROUP_ID", "placeholder")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "placeholder")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "placeholder")
API_KEY = os.environ.get("API_KEY", "placeholder")
CSV_FILE_PATH = os.environ.get("CSV_FILE_PATH", "prova.csv")

DASHBOARD_HOSTNAME = os.environ.get("DASHBOARD_HOSTNAME","placeholder")
