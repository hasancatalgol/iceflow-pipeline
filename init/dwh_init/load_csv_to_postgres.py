import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres(max_retries=10, delay=2):
    print("⏳ Waiting for Postgres to become available...")
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname="sipay",
                user="admin",
                password="admin",
                host="dwh",
                port="5432"
            )
            conn.close()
            print("✅ Postgres is ready!")
            return
        except OperationalError as e:
            print(f"Retry {i + 1}/{max_retries} failed: {e}")
            time.sleep(delay)
    raise Exception("🚨 Could not connect to Postgres after several attempts")

def main():
    wait_for_postgres()

    try:
        conn = psycopg2.connect(
            dbname="sipay",
            user="admin",
            password="admin",
            host="dwh",
            port="5432"
        )

        cur = conn.cursor()

        with open("dataset.csv", "r") as f:
            cur.copy_expert(
                """
                COPY public.transactions (
                    txcorrelationid,
                    tenantid,
                    txgroupcorrelationid,
                    txrefcorrelationid,
                    walletid,
                    transactiontypecode,
                    transactionstatuscode,
                    resultcode,
                    txadditionaldatajson,
                    createddateutc,
                    updateddateutc,
                    completeddateutc,
                    financialprocesscompleteddateutc,
                    isfinancialprocesscompleted,
                    towalletid,
                    txbaseamount,
                    txadditionalfee,
                    txamountwithadditionalfee,
                    currencycode,
                    txenduserpreviewjson,
                    fromdescription,
                    todescription,
                    kyclevelcode,
                    fromaccounttypeid,
                    fromaccountid,
                    fromwalletnumber,
                    fromaccountnumber,
                    toaccountnumber,
                    toaccounttypeid,
                    toaccountid,
                    towalletnumber,
                    summarycreateddateutc,
                    isneedsettlement,
                    settlementday,
                    exttransactionid,
                    channeltype,
                    sourcetype,
                    mediaidentifier,
                    terminalno,
                    mediatype,
                    providerid,
                    toaccounttxbaseamount,
                    toaccounttxadditionalfee,
                    toaccounttxamountwithadditionalfee,
                    settlementtypeid,
                    isadjustlimitsuccessprocessed,
                    isadjustlimitcancelprocessed,
                    tenantname,
                    tenantcode,
                    ishidden,
                    ishiddenforreceiver,
                    ishiddenforsender,
                    fromextaccountnumber,
                    toextaccountnumber,
                    fromgroupcode,
                    togroupcode,
                    receiptnumber
                )
                FROM STDIN WITH CSV HEADER DELIMITER ','
                """,
                f
            )

        conn.commit()
        cur.close()
        conn.close()

        print("✅ Data loaded successfully into 'public.transactions'")

    except Exception as e:
        print(f"❌ Error during CSV import: {e}")

if __name__ == "__main__":
    main()
