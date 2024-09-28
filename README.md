# Airflow
 
### Run:

## Init, Webservice, Scheduler, Triggerer, Postgres
```
docker-compose up -d --no-deps --build
```

## MinIO (To simulate AWS API connection in local)
```
docker run -d -p 9000:9000 -p 9001:9001 --name minio1 -v /e/minio/data:/data -e "MINIO_ROOT_USER=USER" -e "MINIO_ROOT_PASSWORD=PASSWORD" quay.io/minio/minio server /data --console-address ":9001"
```

## Usage:
```
access http://localhost:8080 to see all the DAGs
access http://localhost:9001 to see MinIO Storage
```
