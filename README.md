# NodeJsScan

Static security code scanner (SAST) for Node.js applications.

[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/ajinabraham/NodeJsScan)
[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/)
[![Requirements Status](https://requires.io/github/ajinabraham/NodeJsScan/requirements.svg?branch=master)](https://requires.io/github/ajinabraham/NodeJsScan/requirements/?branch=master)

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

## NodeJsScan CLI

The command line interface (CLI) allows you to integrate NodeJsScan with DevSecOps CI/CD pipelines. The results are in JSON format. When you use CLI the results are never stored with NodeJsScan backend.

```bash
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

## Python API

```python
import core.scanner as njsscan
res_dir = njsscan.scan_dirs(['/Code/Node.Js-Security-Course'])
res_file = njsscan.scan_file(['/Code/Node.Js-Security-Course/deserialization.js'])
print(res_file)

[{'title': 'Deserialization Remote Code Injection', 'description': "User controlled data in 'unserialize()' or 'deserialize()' function can result in Object Injection or Remote Code Injection.", 'tag': 'rci', 'line': 11, 'lines': 'app.use(cookieParser())\n\napp.get(\'/\', function(req, res) {\n            if (req.cookies.profile) {\n                var str = new Buffer(req.cookies.profile, \'base64\').toString();\n                var obj = serialize.unserialize(str);\n                if (obj.username) {\n                    res.send("Hello " + escape(obj.username));\n                }\n            } else {', 'filename': 'deserialization.js', 'path': '/Users/ajin/Code/Node.Js-Security-Course/deserialization.js', 'sha2': '06f3f0ff3deed27aeb95955a17abc7722895d3538c14648af97789d8777cee50'}]

```

## Docker

NodeJsScan Docker images can be built for both the Web UI and CLI version.

* Web UI

  ```bash
  docker build -t nodejsscan .
  docker run -it -p 9090:9090 nodejsscan
  ```

* CLI

  ```bash
  # Use -f to override default Dockerfile
  docker build -t nodejsscan-cli -f cli.dockerfile  .
  # Mount a volume to the container that points to your source directory and reference it in -f, -d and -o arguments
  docker run -v /path-to-source-dir:/src nodejsscan-cli -d /src -o /src/results.json
  ```

## DockerHub

```bash
docker pull opensecurity/nodejsscan
docker run -it -p 9090:9090 opensecurity/nodejsscan:latest
```

## Learn Node.js Security: Pentesting and Exploitation

[![OpSecX Video Course](https://user-images.githubusercontent.com/4301109/43572791-f54e87f6-965d-11e8-8811-7a8900df3379.png)](https://opsecx.com/index.php/product/node-js-security-pentesting-and-exploitation/?uid=github)

## NodeJsScan Web UI

![NodeJsScan](https://cloud.githubusercontent.com/assets/4301109/22619224/26acd162-eb16-11e6-8f28-bd477c92991f.png)

## Static Analysis

![NodeJsScan Static Scan Results](https://user-images.githubusercontent.com/4301109/33951861-294062a0-e056-11e7-8472-3c101be52390.jpg)
![NodeJsScan Static Scan Vulnerability Details](https://user-images.githubusercontent.com/4301109/30637698-bfa68e04-9e16-11e7-8233-bfde503d7e5a.png)
![NodeJsScan CLI](https://user-images.githubusercontent.com/4301109/43541417-0a749362-95e8-11e8-9d5c-4d9a2fd9f765.png)
