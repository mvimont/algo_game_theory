import pandas as pd

def TransposeDF(df, spark_session):
    df = df.toPandas()
    df = df.T
    return spark_session.createDataFrame(df)
