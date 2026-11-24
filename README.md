# Mobile Analytics Platform

A comprehensive mobile analytics platform for tracking user events, processing data pipelines, and enabling churn prediction models.

## Overview

This project is a collaborative effort across three students, each responsible for different components of the analytics pipeline:

- **Student 1**: Event generation and Kafka production
- **Student 2**: Data engineering pipeline (Bronze → Silver → Gold)
- **Student 3**: Analytics, models, and Airflow orchestration

## Directory Structure

```
mobile-app-analytics/
│
├── event-generator/                 # STUDENT 1
│   ├── src/
│   │   ├── generators/
│   │   │   ├── user_generator.py
│   │   │   └── event_generator.py
│   │   │
│   │   ├── kafka/
│   │   │   └── producer.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── event.py
│   │   │
│   │   └── main.py
│   │
│   ├── schemas/
│   │   └── event_schema.json
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── data-engineering/                # STUDENT 2
│   ├── src/
│   │   ├── ingestion/
│   │   │   └── kafka_consumer.py
│   │   │
│   │   ├── bronze/
│   │   │   └── bronze_writer.py
│   │   │
│ │   ├── silver/
│   │   │   ├── clean_events.py
│   │   │   └── silver_writer.py
│   │   │
│   │   ├── gold/
│   │   │   ├── calculate_dau.py
│   │   │   ├── calculate_mau.py
│   │   │   ├── calculate_retention.py
│   │   │   └── calculate_sessions.py
│   │   │
│   │   ├── utils/
│   │       ├── spark_session.py
│   │       └── hudi_config.py
│   │
│   │   jobs/
│   │       ├── bronze_job.py
│   │       ├── silver_job.py
│   │       └── gold_job.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── analytics/                       # STUDENT 3
│   ├── churn_prediction/
│   │   ├── data_preparation.py
│   │   ├── feature_engineering.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   │
│   ├── queries/
│   │   ├── dau.sql
│   │   ├── mau.sql
│   │   └── retention.sql
│   │
│   ├── models/
│   │
│   └── requirements.txt
│
├── airflow/                         # STUDENT 3
│   ├── dags/
│   │   ├── mobile_analytics_dag.py
│   │   └── churn_prediction_dag.py
│   │
│   ├── plugins/
│   ├── logs/
│   └── config/
│
├── dashboards/                      # STUDENT 3
│   ├── superset/
│   │   ├── dashboards/
│   │   ├── datasets/
│   │   └── exports/
│   │
│   └── screenshots/
│
├── infrastructure/                  # SHARED
│   ├── kafka/
│   │   └── config/
│   │
│   ├── spark/
│   │   └── config/
│   │
│   ├── hudi/
│   │   └── config/
│   │
│   ├── storage/
│   │
│   └── docker/
│       └── Dockerfiles/
│
├── data/                             # SHARED
│   ├── sample/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── scripts/
│   ├── start.sh
│   ├── stop.sh
│   └── generate_sample_data.py
│
├── tests/                            # SHARED
│   ├── integration/
│   └── end_to_end/
│
├── docs/
│   ├── cahier_des_charges/
│   ├── architecture/
│   ├── api/
│   ├── installation/
│   └── screenshots/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
└── README.md
```

## Event Schema

The standard event format follows this JSON schema:

```json
{
  "type": "object",
  "required": [
    "event_id",
    "user_id",
    "event_type",
    "timestamp",
    "device"
  ],
  "properties": {
    "event_id": {
      "type": "string"
    },
    "user_id": {
      "type": "string"
    },
    "event_type": {
      "type": "string"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "device": {
      "type": "string",
      "enum": ["Android", "iOS"]
    },
    "screen": {
      "type": ["string", "null"]
    }
  }
}
```

## Student Responsibilities

### Student 1 - Event Generator
- Generates synthetic mobile events with user, event type, and device information
- Produces events to Kafka topic
- Handles event schema validation

### Student 2 - Data Engineering
- **Bronze Layer**: Ingest raw events from Kafka, write to persistent storage (HDFS/S3)
- **Silver Layer**: Clean and transform raw events, deduplication, basic enrichment
- **Gold Layer**: Aggregated analytics (DAU, MAU, retention, sessions)
- Uses Apache Spark and Hudi for incremental processing

### Student 3 - Analytics
- **Churn Prediction**: Train machine learning models to predict user churn
- **Airflow Orchestration**: DAGs for ETL pipelines and model training
- **SQL Queries**: DAU, MAU, retention analysis queries
- **Dashboards**: Visualizations in Superset

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Apache Spark (for data-engineering components)
- Apache Airflow (for orchestration)

### Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and configure settings
3. Start infrastructure:
   ```bash
   docker-compose up -d
   ```

### Running Components

#### Event Generator (Student 1)
```bash
cd event-generator
docker build -t event-generator .
# or run directly:
python -m src.main
```

#### Data Engineering Pipeline (Student 2)
```bash
cd data-engineering
# Start Spark session and run jobs
python -m src.ingestion.kafka_consumer
# or submit Spark jobs:
spark-submit jobs/bronze_job.py
```

#### Analytics & Models (Student 3)
```bash
cd analytics
# Train models
python churn_prediction/train.py
# Run Airflow DAGs
airflow dags trigger mobile_analytics_dag
```

## Development

### Event Flow

1. **Generation**: Student 1 generates mobile events → publishes to Kafka
2. **Ingestion**: Student 2's bronze job consumes from Kafka → writes raw data
3. **Transformation**: Student 2's silver job cleans/transforms data
4. **Aggregation**: Student 2's gold layer computes metrics
5. **Analysis**: Student 3 uses aggregated data for models/queries

### Testing

- Unit tests located in each module's `tests/` directory
- Integration tests in `tests/integration/`
- End-to-end tests in `tests/end_to_end/`

## License

This project is for educational purposes as part of the Big Data course (IL11).