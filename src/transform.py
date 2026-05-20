from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def create_spark_session() -> SparkSession:
    """Create a local Spark session for development."""
    return (
        SparkSession.builder
        .appName("city-weather-etl")
        .master("local[*]")  # use all available CPU cores locally
        .getOrCreate()
    )


def transform_weather(raw_data: list[dict]) -> "DataFrame":
    """
    Takes raw extracted records and returns a clean Spark DataFrame.
    Transformations:
      - Enforce schema explicitly (never trust raw data)
      - Add a comfort_level column derived from temp + humidity
      - Add a loaded_at timestamp
    """
    spark = create_spark_session()

    schema = StructType([
        StructField("city",         StringType(),  nullable=False),
        StructField("extracted_at", StringType(),  nullable=False),
        StructField("temp_c",       IntegerType(), nullable=True),
        StructField("feels_like_c", IntegerType(), nullable=True),
        StructField("humidity_pct", IntegerType(), nullable=True),
        StructField("weather_desc", StringType(),  nullable=True),
        StructField("wind_kmph",    IntegerType(), nullable=True),
    ])

    df = spark.createDataFrame(raw_data, schema=schema)

    df = df.withColumn(
        "comfort_level",
        when((col("temp_c") >= 18) & (col("humidity_pct") <= 60), "comfortable")
        .when(col("temp_c") < 5, "cold")
        .when(col("humidity_pct") > 80, "humid")
        .otherwise("moderate")
    )

    df = df.withColumn("loaded_at", current_timestamp())

    return df


if __name__ == "__main__":
    # Import extract so we can test the full extract → transform flow
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.extract import extract_all_cities

    raw = extract_all_cities()
    df = transform_weather(raw)

    print(f"\nSchema:")
    df.printSchema()

    print(f"\nSample data:")
    df.show(truncate=False)