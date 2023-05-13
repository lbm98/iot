### Sources

- https://earthly.dev/blog/docker-mysql/

### Commands

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

Run to check if the MySQL server is running
```bash
docker ps
````