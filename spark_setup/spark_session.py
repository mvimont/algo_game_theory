from pyspark.sql import SparkSession

def get_spark_session(app_name):
    return SparkSession.builder \
            .master("local") \
            .appName(app_name) \
            .getOrCreate()
