import os
import pandas as pd

# Storage account SAS token - set as environment variable, never hardcode
STORAGE_SAS_TOKEN = os.getenv("STORAGE_SAS_TOKEN")
STORAGE_ACCOUNT = "dluberprojectdevsai"
CONTAINER = "raw/ingestion"

files = [
    {"file": "map_cities"},
    {"file": "map_cancellation_reasons"},
    {"file": "map_payment_methods"},
    {"file": "map_ride_statuses"},
    {"file": "map_vehicle_makes"},
    {"file": "map_vehicle_types"},
    {"file": "bulk_rides"},
]

for file in files:
    url = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/{CONTAINER}/{file['file']}.json?{STORAGE_SAS_TOKEN}"

    df = pd.read_json(url)
    df_spark = spark.createDataFrame(df)

    df_spark.write.format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .saveAsTable(f"uber.bronze.{file['file']}")