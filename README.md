## Going to do a quick README for now

### Running the Postgres container

```shell
docker compose up -d
```

### Building the ingestion pipeline

```shell
docker build -t data_ingester:0.01 .
```

### Two lines specifically needed for the homework

```shell
docker run -it --network=de_zoomcamp_course_default data_ingester:0.01 --user=root --password=root --host=pg-database --port=5432 --db=ny_taxi --table_name=green_taxi_trips --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz --if_exists=replace
```

```shell
docker run -it --network=de_zoomcamp_course_default data_ingester:0.01 --user=root --password=root --host=pg-database --port=5432 --db=ny_taxi --table_name=taxi_zones --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv --if_exists=replace
```