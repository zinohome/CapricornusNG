# Capricornusng

## Develop

### Install command line extension

`pip install fastapi_amis_admin[cli]`

### How to start

1. create your app using `faa new app_name` .
2. writing your apps under `capricornusng/backend/apps` folder.
3. run your server using `faa run` .

### Documentation

See [Docs](https://docs.amis.work/)

## Deploy

### Install and run:

```shell
cd capricornusng
./scripts/run.sh
```

uvicorn main:app --host '0.0.0.0' --port 8000 --reload

hypercorn -c appconfig/hypercorn-dev.py -w 1 --reload main:app


