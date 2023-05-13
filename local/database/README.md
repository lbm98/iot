### Sources

- https://earthly.dev/blog/docker-mysql/

### Commands for general debugging

```bash
netstat -ltnp | grep -w '5000' 
```

```bash
docker ps
````

### Commands for local API

Run to start the MySQL server
```bash
docker run --name iot-mysql -d \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=iot \
mysql:8
```

Run to debug the MySQL server
```bash
docker exec -it iot-mysql mysql -p
```

Run to check the sensor data
```bash
docker exec -it iot-mysql mysql -uroot -piot -e "USE iot_db; SELECT * FROM  sensor"
```

Run to remove the MySQL server
```bash
docker rm -f iot-mysql
````

### Commands for dockerized API

Run to build the images
```bash
docker compose build
```

Run to bring the containers up with log messages
```bash
docker compose up
```

Run to bring the containers up in the background
```bash
docker compose up -d
```

Run to debug the API container
```bash
docker compose exec api bash
```

Run to test a POST request
```bash
python post.py
```

Run to check the sensor data
```bash
docker compose exec db mysql -uroot -piot -e "USE iot_db; SELECT * FROM  sensor"
```

Run to bring the containers down
```bash
docker compose stop
```
