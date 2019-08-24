#!/bin/bash
sudo rm -r ./elasticsearch/esdata01
sudo rm -r ./elasticsearch/esdata02

mkdir ./elasticsearch/esdata01
mkdir ./elasticsearch/esdata02

sudo chown -R 1000:1000 ./elasticsearch/esdata01
sudo chown -R 1000:1000 ./elasticsearch/esdata02