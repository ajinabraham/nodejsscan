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

Install Postgres and configure `SQLALCHEMY_DATABASE_URI` in `nodejsscan/settings.py` or as environment variable.

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

This will run nodejsscan web user interface at `http://127.0.0.1:9090`


## Command Line Interface(CLI) and Python API

![njsscan_cli](https://user-images.githubusercontent.com/4301109/83962395-ecbc8900-a86a-11ea-9fe7-40703a7e6d4b.gif)

* CLI: https://github.com/ajinabraham/njsscan#command-line-options
* API: https://github.com/ajinabraham/njsscan#python-api

## Integrations

### Slack Alerts

Create your slack app [Slack App](https://api.slack.com/messaging/webhooks) and set `SLACK_WEBHOOK_URL` in `nodejsscan/settings.py` or as environment variable.

![nodejsscan slack alert](https://user-images.githubusercontent.com/4301109/83978059-d64a1800-a8d2-11ea-9ef8-7a17d8904324.png)

### Email Alerts

Configure SMTP settings in `nodejsscan/settings.py` or as environment variable.

## Build Docker image

```bash
docker build -t nodejsscan .
docker run -it -p 9090:9090 nodejsscan
 ```

* CLI Docker Image: https://github.com/ajinabraham/njsscan#build-locally

## nodejsscan screenshots

