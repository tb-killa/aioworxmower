# aioworxmower

Async Python library for Worx Landroid mowers with OAuth, discovery, MQTT/WS, ACK, schedules.

## Requirements
- Python 3.11+
- Poetry

## First run
```bash
git clone <THIS-REPO>
cd <THIS-REPO>
poetry install
cp _secrets.yaml secrets.yaml
poetry run python example.py
```

## Realtime MQTT
```bash
poetry run python example_mqtt.py
```

## Tests
```bash
poetry run pre-commit run --all-files
poetry run pytest -m "unit"
poetry run pytest -m "integration"
```
