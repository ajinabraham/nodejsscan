# NodeJsScan

Static Security code scanner for node.js applications.

## How to Configure

1. Install postgres and configure `SQLALCHEMY_DATABASE_URI` in `core/settings.py`
2. Run `pip install -r requirements.txt`
3. Run `python createdb.py`
4. Run `python app.py`

This will run NodeJsScan on `http://0.0.0.0:9090`
If you need to debug, set `DEBUG = True` in `core/settings.py`

![NodeJsScan V2](https://cloud.githubusercontent.com/assets/4301109/22619224/26acd162-eb16-11e6-8f28-bd477c92991f.png)
