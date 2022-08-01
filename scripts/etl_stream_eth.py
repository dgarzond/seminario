import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StringType,
    DoubleType,
    StructType,
    StructField,
    TimestampType,
)
def validate_params(args):
    if len(args) != 3:
        print(f"""
         |Usage: {args[0]} <brokers> <topics>
         |  <brokers> is a list of one or more Kafka brokers
         |  <topic> is a a kafka topic to consume from
         |
         |  {args[0]} kafka:9092 crypto
        """)
        sys.exit(1)
    pass


def create_spark_session():
    return (
        SparkSession
        .builder
        .appName("Crypto:Stream:ETL")
        .config("spark.driver.memory", "512m")
        .config("spark.executor.memory", "512m")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )


def start_stream(args=None):

    spark = create_spark_session()

    json = (
        spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "crypto")
        .load()
    )
    json.printSchema()

    # Explicitly set schema
    schema = StructType([
        StructField("date", TimestampType(), False),
        StructField("price", DoubleType(), False),
        StructField("currency", StringType(), False)
    ])

    json_options = {"timestampFormat": "yyyy-MM-dd'T'HH:mm'Z'"}
    crypto_json = json.select(
        F.from_json(F.col("Value").cast("string"), schema, json_options).alias("content")
    )

    crypto_json.printSchema
    crypto= crypto_json.select("content.*")
    #############################################################################
    # query3 | Postgres Output | Simple insert
    #############################################################################
    query3 = stream_to_postgres(crypto)
    query3.awaitTermination()
     
    pass


def define_write_to_postgres(table_name):
    print("define_write_to_postgres")
    def write_to_postgres(df, epochId):
        print("write_to_postgres")
        print(f"Bacth (epochId): {epochId}")
        return (
            df.write
            .format("jdbc")
            .option("url", "jdbc:postgresql://postgres/workshop")
            .option("dbtable", f"workshop.{table_name}")
            .option("user", "workshop")
            .option("password", "w0rkzh0p")
            .option("driver", "org.postgresql.Driver")
            .mode("append")
            .save()
        )
    return write_to_postgres


def stream_to_postgres(crypto, output_table="crypto"):
    print("stream_to_postgres")
    wcrypto = (
        crypto
        .withWatermark("date", "10 seconds")
        .select("date", "price", "currency")
    )
    print(wcrypto)

    write_to_postgres_fn = define_write_to_postgres("crypto")

    query = (
        wcrypto
        .writeStream
        .foreachBatch(write_to_postgres_fn)
        .outputMode("append")
        .trigger(processingTime="10 seconds")
        .start()
    )

    return query

start_stream()
