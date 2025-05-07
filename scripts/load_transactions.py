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
        max_created_date = target_df.select(spark_max("createddateutc")).collect()[0][0]

        print(f"🔵 Max createddateutc in Iceberg table: {max_created_date}")

        # 🔥 Read only new records from Postgres
        predicate = f"createddateutc > '{max_created_date}'"
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

        # 🛠 Create Iceberg table manually (with partition by days(createddateutc))
        spark.sql("""
            CREATE TABLE hive_catalog.default.transactions (
                txcorrelationid BIGINT,
                tenantid BIGINT,
                txgroupcorrelationid BIGINT,
                txrefcorrelationid BIGINT,
                walletid BIGINT,
                transactiontypecode INT,
                transactionstatuscode INT,
                resultcode STRING,
                txadditionaldatajson STRING,
                createddateutc TIMESTAMP,
                updateddateutc TIMESTAMP,
                completeddateutc TIMESTAMP,
                financialprocesscompleteddateutc TIMESTAMP,
                isfinancialprocesscompleted BOOLEAN,
                towalletid BIGINT,
                txbaseamount DECIMAL(18,4),
                txadditionalfee DECIMAL(18,4),
                txamountwithadditionalfee DECIMAL(18,4),
                currencycode STRING,
                txenduserpreviewjson STRING,
                fromdescription STRING,
                todescription STRING,
                kyclevelcode STRING,
                fromaccounttypeid STRING,
                fromaccountid BIGINT,
                fromwalletnumber STRING,
                fromaccountnumber STRING,
                toaccountnumber STRING,
                toaccounttypeid STRING,
                toaccountid BIGINT,
                towalletnumber STRING,
                summarycreateddateutc TIMESTAMP,
                isneedsettlement BOOLEAN,
                settlementday INT,
                exttransactionid STRING,
                channeltype STRING,
                sourcetype STRING,
                mediaidentifier STRING,
                terminalno STRING,
                mediatype STRING,
                providerid STRING,
                toaccounttxbaseamount DECIMAL(18,4),
                toaccounttxadditionalfee DECIMAL(18,4),
                toaccounttxamountwithadditionalfee DECIMAL(18,4),
                settlementtypeid INT,
                isadjustlimitsuccessprocessed BOOLEAN,
                isadjustlimitcancelprocessed BOOLEAN,
                tenantname STRING,
                tenantcode STRING,
                ishidden BOOLEAN,
                ishiddenforreceiver BOOLEAN,
                ishiddenforsender BOOLEAN,
                fromextaccountnumber STRING,
                toextaccountnumber STRING,
                fromgroupcode STRING,
                togroupcode STRING,
                receiptnumber STRING
            )
            USING iceberg
            PARTITIONED BY (days(createddateutc))
        """)

    # 🚑 Repartition to distribute the load
    df = df.repartition(6)

    if df.count() > 0:
        # 🔥 Insert into Iceberg table
        df.writeTo(target_table) \
          .append()
        print("✅ Records written successfully.")
    else:
        print("⚪ No new records found. Skipping write.")

if __name__ == "__main__":
    main()
