# nodejsscan

Static security code scanner (SAST) for Node.js applications powered by [njsscan](https://github.com/ajinabraham/njsscan) and [semgrep](https://github.com/returntocorp/semgrep)

Made with ![Love](https://cloud.githubusercontent.com/assets/4301109/16754758/82e3a63c-4813-11e6-9430-6015d98aeaab.png) in India

[![platform](https://img.shields.io/badge/platform-osx%2Flinux-green.svg)](https://github.com/ajinabraham/nodejsscan)
[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ajinabraham/nodejsscan.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ajinabraham/nodejsscan/context:python)
[![Requirements Status](https://requires.io/github/ajinabraham/nodejsscan/requirements.svg?branch=master)](https://requires.io/github/ajinabraham/nodejsscan/requirements/?branch=master)
[![Build](https://github.com/ajinabraham/nodejsscan/workflows/Test/badge.svg)](https://github.com/ajinabraham/nodejsscan/actions?query=workflow%3ATest)

### e-Learning Courses & Certifications
[![OpSecX Video Course](https://user-images.githubusercontent.com/4301109/82597198-99fa8600-9b76-11ea-8243-c604bc7b06b1.png)](https://opsecx.com/index.php/product/node-js-security-pentesting-and-exploitation/?uid=github) [OpSecX Node.js Security: Pentesting and Exploitation - NJS](https://opsecx.com/index.php/product/node-js-security-pentesting-and-exploitation/?uid=github)

## Run nodejsscan

```bash
docker pull opensecurity/nodejsscan:latest
docker run -it -p 9090:9090 opensecurity/nodejsscan:latest
```

Try nodejsscan online:
[![Try in PWD](https://user-images.githubusercontent.com/4301109/76351696-494bee80-62e4-11ea-894a-cb1cd07c86fc.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/ajinabraham/nodejsscan/master/docker-compose.yml)

## Setup nodejsscan locally

Install Postgres and configure `SQLALCHEMY_DATABASE_URI` in `nodejsscan/settings.py`.

From version 4 onwards, windows support is dropped.

```bash
git clone https://github.com/ajinabraham/nodejsscan.git
cd nodejsscan
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py recreate_db # Run once to create database entries
```

To run nodejsscan 

`./run.sh`

This will run nodejsscan web user interface on `http://127.0.0.1:9090`


## Command Line Interface(CLI) and Python API

![njsscan_cli](https://user-images.githubusercontent.com/4301109/83962395-ecbc8900-a86a-11ea-9fe7-40703a7e6d4b.gif)

* CLI: https://github.com/ajinabraham/njsscan#command-line-options
* API: https://github.com/ajinabraham/njsscan#python-api


## Docker

NodeJsScan Docker images can be built for both the Web UI and CLI version.

```bash
docker build -t nodejsscan .
docker run -it -p 9090:9090 nodejsscan
 ```

* CLI Docker Image: https://github.com/ajinabraham/njsscan#build-locally

## nodejsscan screenshots

![NodeJsScan](https://cloud.githubusercontent.com/assets/4301109/22619224/26acd162-eb16-11e6-8f28-bd477c92991f.png)
![NodeJsScan Static Scan Results](https://user-images.githubusercontent.com/4301109/33951861-294062a0-e056-11e7-8472-3c101be52390.jpg)
![NodeJsScan Static Scan Vulnerability Details](https://user-images.githubusercontent.com/4301109/30637698-bfa68e04-9e16-11e7-8233-bfde503d7e5a.png)
![NodeJsScan CLI](https://user-images.githubusercontent.com/4301109/43541417-0a749362-95e8-11e8-9d5c-4d9a2fd9f765.png)
