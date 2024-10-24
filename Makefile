flink-client:
	docker compose run flink-sql-client

start:
	docker compose up --build -d

shutdown:
	docker compose down -v

setup:
	python scripts/setup.py
