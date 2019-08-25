#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE DATABASE jupyterhub;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "jupyterhub" <<-EOSQL
CREATE TABLE system_announcements (
   id       SERIAL PRIMARY KEY,
   type     VARCHAR (255),
   title    VARCHAR (255),
   content  TEXT,
   shown    BOOLEAN NOT NULL DEFAULT TRUE,
   created  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE user_passwords (
   id       SERIAL PRIMARY KEY,
   name     VARCHAR (31) NOT NULL,
   password VARCHAR (31) NOT NULL,
   active   BOOLEAN NOT NULL DEFAULT TRUE,
   created  TIMESTAMP NOT NULL DEFAULT NOW()
);
INSERT INTO system_announcements(type, title, content) VALUES ('normal', '公告', '一般公告');
INSERT INTO user_passwords(name, password) VALUES ('admin', 'kslab35356');
EOSQL