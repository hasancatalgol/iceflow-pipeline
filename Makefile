up-dwh:
	docker compose --profile dwh up --build -d

down-dwh:
	docker compose --profile dwh down -v
	docker volume rm pgadmin_data

up-iceberg:
	docker compose --profile iceberg up --build -d

down-iceberg:
	docker compose --profile iceberg down -v
	docker volume rm hive_metastore_db

up-airflow:
	docker compose --profile airflow up --build -d

down-airflow:
	docker compose --profile airflow down -v
	docker volume rm airflow-backend-db-volume

