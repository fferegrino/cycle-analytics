# Cycle analytics

## Setup

### 1. Setup containers

```
docker compose up --build -d
```

### 2. Setup Kafka infra

```
python scripts/setup_topic.py
```

### 3. Start producing events

```
python scripts/events_simulator.py
```

#### 3.1 Verify events are being sent (optional)

```
python scripts/dummy_consumer.py
```
