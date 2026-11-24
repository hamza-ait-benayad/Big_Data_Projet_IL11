# Big Data Project - IL11

This repository contains the infrastructure for a big data pipeline involving event generation and data ingestion.

## Project Structure

### event-generator/
A module for generating synthetic events and publishing them to Kafka.

- `src/generators/event_generator.py` - Event generation logic
- `src/kafka/producer.py` - Kafka producer for publishing events
- `src/main.py` - Main entry point

### data-engineering/
A module for consuming and processing events from Kafka.

- `src/ingestion/kafka_consumer.py` - Kafka consumer for event ingestion

## Prerequisites

- Docker and Docker Compose
- Python 3.8+

## Running the Project

### Using Docker Compose

Start the infrastructure (Zookeeper and Kafka):

```bash
docker-compose up -d
```

This will start:
- Zookeeper on port 2181
- Kafka on port 9092

### Running the Event Generator

```bash
cd event-generator
python -m src.main
```

### Running the Data Ingestion

```bash
cd data-engineering
python -m src.ingestion.kafka_consumer
```

## Development

### Generating Events

The event generator can produce synthetic events of various types:
- `click` - User clicking on a page element
- `view` - Page view event
- `purchase` - Purchase transaction
- `signup` - User signup
- `login` - User login

### Consuming Events

The Kafka consumer reads events from the `events` topic and can be extended
to process them according to the data engineering requirements.