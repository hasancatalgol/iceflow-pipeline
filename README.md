# 🚀 Data Platform - Local Development Environment

![Project Directory Structure](./pictures/architecture.svg)

> _Screenshot of the local repo layout showing where the `pictures/architecture.svg` lives_

## 🧩 Services & Ports

| Service                    | Description                                          | Host Port → Container Port |
|----------------------------|------------------------------------------------------|-----------------------------|
| **Airflow Web UI**         | Airflow API/Web Interface                            | `localhost:8080`            |
| **Flower**                 | Celery monitoring UI for Airflow                     | `localhost:5555`            |
| **PostgreSQL (Airflow)**   | Backend DB for Airflow                               | _Internal only_             |
| **PostgreSQL (DWH)**       | Your data warehouse database                | `localhost:5432`            |
| **pgAdmin**                | GUI for managing PostgreSQL                          | `localhost:5050`            |
| **Redis**                  | Celery broker for Airflow                            | _Internal only_             |
| **Spark Master**           | Spark master node & UI                               | `localhost:7077` (RPC), `localhost:8081` (UI) |
| **Spark Worker 1**         | Spark executor(Inactive)                                       | _Internal only_             |
| **Spark Worker 2**         | Spark executor(Inactive)                                       | _Internal only_             |
| **Hive Metastore Catalog**           | Hive Metastore                          | `localhost:8181`            |
| **MinIO**                  | S3-compatible object storage                         | `localhost:9000` (API), `localhost:9001` (Console) |
| **MinIO Client (mc)**      | Initializes MinIO bucket & policy                    | _Internal only_             |

---

## 📁 Volumes

| Volume                      | Purpose                                      |
|-----------------------------|----------------------------------------------|
| `airflow-backend-db-volume` | Persists Airflow metadata DB (Postgres)      |
| `pgadmin_data`              | Persists pgAdmin config & session state      |
| `dwh_data`                  | Persists data warehouse Postgres database    |

---

## 📦 Features

- **Airflow with Celery Executor** and Redis as broker.  
- **Spark Cluster** with custom Iceberg support and REST catalog.  
- **MinIO** as S3-compatible storage for Iceberg tables.  
- **pgAdmin** for local PostgreSQL interaction.  
- **Hive Metastore Catalog** for easier Flink/Spark/Trino integration and meta data management.

---

## 🚀 Usage

```bash
# Start everything
docker compose up --build -d

# Tear down everything and remove volumes
docker compose down -v
