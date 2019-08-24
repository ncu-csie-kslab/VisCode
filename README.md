VisCode
=======

## Requirements
作業系統僅測試過 `Ubuntu 18.04`。
- Linux envirements
- docker
- docker-compose

## Clear data
注意：這兩個程式會清除所有資料。
```sh
bash ./clear-elasticsearch.sh
bash ./clear-postgres.sh
```

## Installation
請在 viscode 目錄下執行。
```sh
bash ./build-jupyter-image.sh
bash ./clear-elasticsearch.sh
sudo docker-compose build
sudo docker-compose up
```

## Control
關閉所有 container。
```sh
sudo docker-compose stop
```

啟動所有 container。
```sh
sudo docker-compose start
```

移除所有 container，不會移除 posrgres 與 elasticsearch 的資料。
```sh
sudo docker-compose rm
```

## Services
預設所有服務無對外，僅限 localhost 連線，有需求請修改`docker-compose.yml`的配置。

Service         | Port       
----------------|:-----------
jupyterhub      | 8000       
viscode-api     | 5000       
kibana          | 5601
elasticsearch01 | 9200, 9300 
elasticsearch02 | 9201, 9301
adminer         | 8080