VisCode
=======

## Requirements
主機最低配置：
- RAM: 4G

作業系統 (測試過)：
- Ubuntu 20.04
- Ubuntu 18.04

環境需求：
- Linux envirements
- docker: 17.12.0+
- docker-compose

## Clone code
Clone時需要注意目的地資料夾的位置，以`viscode`最佳，其餘者需要自行注意docker網路配置，主因是Jupyterhub及其DockerSpwner是透過docker的網路互動
```bash
git clone https://github.com/ncu-csie-kslab/VisCode.git viscode

```

## System setting
由於elasticsearch的需要，需修改`/etc/sysctl.conf`，新增下方設定，並重新啟動系統，或使用一次性指令設定。
```conf
vm.max_map_count=262144
```

一次性指令設定，立即生效，重開機後消失。
```bash
sudo sysctl -w vm.max_map_count=262144
```

查看目前系統設定值。
```bash
sysctl vm.max_map_count
```

## Clear data
注意：這程式會清除所有資料。
```sh
bash ./clear-all-data.sh
```

個別清除資料：
```sh
bash ./clear-elasticsearch.sh
bash ./clear-postgres.sh
bash ./clear-jupyterhub.sh
```

## Installation
請在 viscode 目錄下執行。
```sh
bash ./build-jupyter-image.sh
bash ./clear-all-data.sh
sudo docker-compose build
sudo docker-compose up
```

## Upgrade
首先關閉所有運行中的 container，並且移除。
```sh
sudo docker-compose stop
sudo docker-compose rm
sudo docker rmi viscode_jupyterhub
```

更新程式碼，例如使用 git 取得新版本:
```sh
git pull
```

如果有更新 `viscode-extension`，請重新 build 一個新的 docker image。
```sh
bash ./build-jupyter-image.sh
```

最後使用 `docker-compose` build，建立新的 container。
```sh
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
postgres        | 5432
viscode-api     | 5000       
kibana          | 5601
elasticsearch01 | 9200, 9300 
elasticsearch02 | 9201, 9301
adminer         | 8080

Jupyter 預設 admin 帳密。
- 帳號：admin
- 密碼：kslab35356

## Data storage
Jupyter 使用者的 workspace，透過 docker volume bind，會在 local 端的 `/jupyterhub_users` 底下。

其餘的 postgres、elasticsearch01 與 elasticsearch02，存放在各自 Dockerfile 資料夾底下。

Service         | path       
----------------|:-----------
jupyterhub      | /jupyterhub_users      
postgres        | ./postgres/data
elasticsearch01 | ./elasticsearch/esdata01
elasticsearch02 | ./elasticsearch/esdata01

## Auth setting

### Default
預設使用 Postgres 記錄使用者帳號、密碼與驗證。

```yml
jupyterhub:
    environment:
        JUPYTERHUB_AUTH_METHOD: Default
```

### LTI
請修改 `docker-compose.yml` 中 jupyterhub 的環境參數設定。

```yml
jupyterhub:
    environment:
        JUPYTERHUB_AUTH_METHOD: LTI
        LTI_CLIENT_KEY: your_key
        LTI_CLIENT_SECRET: your_secret
        JUPYTERHUB_CRYPT_KEY: your_crypt_key
```

`JUPYTERHUB_CRYPT_KEY` 生成指令：
```bash
openssl rand -hex 32
```

#### 使用者辨別欄位設定
預設使用 `user_id` 作為識別不同使用者的參考，如果需要改使用其他參數，請指定 `LTI_USER_ID_FIELD` 參數。

##### 使用 Moodle 帳號
```yml
LTI_USER_ID_FIELD: ext_user_username
```

## Resource Saving
由於當使用者登入後，使用者的 Jupyter Notebook Server 與開啟的 Notebook 會一直存在，除非使用者手動關閉，因此會一直占用系統資源。

提供兩個參數在 Jupyterhub 進行節省資源：
- NOTEBOOK_TIMEOUT: Notebook 存活時間(分鐘)，當使用者把執行的 Notebook 網頁關閉或斷線時，超過時間關閉該 Notebook。
- JUPYTER_SERVER_TIMEOUT: 當 Jupyter Notebook Server 超過時間(分鐘)沒有動作時關閉，也就是使用者的 container 會被關閉。

以下方設置為例，使用者執行的 Notebook 會在 60 分鐘關閉，整個使用者的 Jupyter 如果沒有任何活動則在 180 分鐘關閉。
```yml
jupyterhub:
    environment:
        NOTEBOOK_TIMEOUT: 60
        JUPYTER_SERVER_TIMEOUT: 180
```

當使用者 Jupyter Notebook Server 因為閒置被關閉可以看到以下類似的 log。。
```log
jupyterhub_1   | [W 2020-07-02 16:32:59.966 JupyterHub base:1047] User admin server stopped, with exit code: ExitCode=0, Error='', FinishedAt=2020-07-02T16:32:32.292891995Z
```