# NodeJsScan

Static security code scanner (SAST) for Node.js applications.

### Configure & Run NodeJsScan

Install Postgres and configure `SQLALCHEMY_DATABASE_URI` in `core/settings.py`

```
pip3 install -r requirements.txt
python3 migrate.py # Run once to create database entries required
python3 app.py # Testing Environment
gunicorn -b 0.0.0.0:9090 app:app # Production Environment
```

This will run NodeJsScan on `http://0.0.0.0:9090`

If you need to debug, set `DEBUG = True` in `core/settings.py`

### NodeJsScan CLI

The command line interface (CLI) allows you to integrate NodeJsScan with DevSecOps CI/CD pipelines. The results are in JSON format. When you use CLI the results are never stored with NodeJsScan backend.

```
virtualenv venv -p python3
source venv/bin/activate
(venv)pip install nodejsscan
(venv)$ nodejsscan
usage: nodejsscan [-h] [-f FILE [FILE ...]] [-d DIRECTORY [DIRECTORY ...]]
                  [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Node.js file(s) to scan
  -d DIRECTORY [DIRECTORY ...], --directory DIRECTORY [DIRECTORY ...]
                        Node.js source code directory/directories to scan
  -o OUTPUT, --output OUTPUT
                        Output file to save JSON report
  -v, --version         Show nodejsscan version
```

### Learn Node.js Security: Pentesting and Exploitation
[OpSecX Video Course](https://opsecx.com/index.php/product/node-js-security-pentesting-and-exploitation/)

### Docker

```
docker build -t nodejsscan .
docker run -it -p 9090:9090 nodejsscan
```

### DockerHub

```
docker pull opensecurity/nodejsscan
docker run -it -p 9090:9090 opensecurity/nodejsscan:latest
```

#### NodeJsScan Web UI
![NodeJsScan](https://cloud.githubusercontent.com/assets/4301109/22619224/26acd162-eb16-11e6-8f28-bd477c92991f.png)

#### Static Analysis
![NodeJsScan Static Scan Results](https://user-images.githubusercontent.com/4301109/33951861-294062a0-e056-11e7-8472-3c101be52390.jpg)
![NodeJsScan Static Scan Vulnerability Details](https://user-images.githubusercontent.com/4301109/30637698-bfa68e04-9e16-11e7-8233-bfde503d7e5a.png)
![NodeJsScan CLI](https://user-images.githubusercontent.com/4301109/43541417-0a749362-95e8-11e8-9d5c-4d9a2fd9f765.png)

