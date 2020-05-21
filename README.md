# NodeJsScan

Static security code scanner (SAST) for Node.js applications.

[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/ajinabraham/NodeJsScan)
[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://travis-ci.com/ajinabraham/nodejsscan.svg?branch=master)](https://travis-ci.com/ajinabraham/nodejsscan)
[![Requirements Status](https://requires.io/github/ajinabraham/nodejsscan/requirements.svg?branch=master)](https://requires.io/github/ajinabraham/nodejsscan/requirements/?branch=master)

## Configure & Run NodeJsScan

Install Postgres and configure `SQLALCHEMY_DATABASE_URI` in `core/settings.py`

```bash
pip3 install -r requirements.txt
python3 migrate.py # Run once to create database entries required
python3 app.py # Testing Environment
gunicorn -b 0.0.0.0:9090 app:app --workers 3 --timeout 10000 # Production Environment
```

This will run NodeJsScan on `http://0.0.0.0:9090`

If you need to debug, set `DEBUG = True` in `core/settings.py`

## Command Line Interface and Python API

* CLI: https://github.com/ajinabraham/njsscan#command-line-options
* API: https://github.com/ajinabraham/njsscan#python-api


## Docker

NodeJsScan Docker images can be built for both the Web UI and CLI version.

```bash
docker build -t nodejsscan .
docker run -it -p 9090:9090 nodejsscan
 ```

* CLI: https://github.com/ajinabraham/njsscan#build-locally

## DockerHub

Prebuilt Docker images are available from DockerHub.

```bash
docker pull opensecurity/nodejsscan
docker run -it -p 9090:9090 opensecurity/nodejsscan:latest
```

* CLI: https://github.com/ajinabraham/njsscan#prebuilt-image-from-dockerhub

## Learn Node.js Security: Pentesting and Exploitation

[![OpSecX Video Course](https://user-images.githubusercontent.com/4301109/43572791-f54e87f6-965d-11e8-8811-7a8900df3379.png)](https://opsecx.com/index.php/product/node-js-security-pentesting-and-exploitation/?uid=github)

## NodeJsScan Web UI

![NodeJsScan](https://cloud.githubusercontent.com/assets/4301109/22619224/26acd162-eb16-11e6-8f28-bd477c92991f.png)

## Static Analysis

![NodeJsScan Static Scan Results](https://user-images.githubusercontent.com/4301109/33951861-294062a0-e056-11e7-8472-3c101be52390.jpg)
![NodeJsScan Static Scan Vulnerability Details](https://user-images.githubusercontent.com/4301109/30637698-bfa68e04-9e16-11e7-8233-bfde503d7e5a.png)
![NodeJsScan CLI](https://user-images.githubusercontent.com/4301109/43541417-0a749362-95e8-11e8-9d5c-4d9a2fd9f765.png)
