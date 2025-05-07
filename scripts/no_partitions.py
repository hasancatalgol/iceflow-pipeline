from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, max as spark_max

def main():
    spark = SparkSession.builder.getOrCreate()

    jdbc_url = "jdbc:postgresql://dwh:5432/sipay"
    connection_properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver"
    }

    target_table = "hive_catalog.default.transactions"

    # 🔥 Create database if not exists
    spark.sql("CREATE DATABASE IF NOT EXISTS hive_catalog.default")

    # 🔥 Check if the target Iceberg table already exists
    table_exists = spark._jsparkSession.catalog().tableExists(target_table)

    if table_exists:
        # 🔥 If table exists, read the max CreatedDateUtc from it
        target_df = spark.table(target_table)
        max_created_date = target_df.select(spark_max("CreatedDateUtc")).collect()[0][0]

        print(f"🔵 Max CreatedDateUtc in Iceberg table: {max_created_date}")

        # 🔥 Read only new records from Postgres
        predicate = f"CreatedDateUtc > '{max_created_date}'"
        print(f"🔵 Applying filter: {predicate}")

        df = spark.read.jdbc(
            url=jdbc_url,
            table="public.transactions",
            properties=connection_properties,
            predicates=[predicate]
        )
    else:
        # 🔥 If table doesn't exist, read full table
        df = spark.read.jdbc(
            url=jdbc_url,
            table="public.transactions",
            properties=connection_properties
        )

    # 🚑 Force repartitioning
    df = df.repartition(6)

    if df.count() > 0:
        # 🔥 If new data exists, append it
        if table_exists:
            df.writeTo(target_table) \
              .using("iceberg") \
              .append()
            print("✅ Incremental records appended successfully.")
        else:
            df.writeTo(target_table) \
              .using("iceberg") \
              .createOrReplace()
            print("✅ Table created with full load.")
    else:
        print("⚪ No new records found. Skipping write.")

if __name__ == "__main__":
    main()
