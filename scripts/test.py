from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder.appName("IcebergHiveMinioTest").getOrCreate()

# Fully qualify catalog to avoid AnalysisException
spark.sql("DROP TABLE IF EXISTS hive_catalog.default.people")

# Create Iceberg table in Hive catalog
spark.sql("""
    CREATE TABLE hive_catalog.default.people (
        id INT,
        name STRING
    )
    USING iceberg
""")

# Insert records — again, fully qualified with catalog
spark.sql("INSERT INTO hive_catalog.default.people VALUES (1, 'Hasan'), (2, 'ChatGPT')")

# Query the table
spark.sql("SELECT * FROM hive_catalog.default.people").show()
