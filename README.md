## SMSWithoutBorders-Telemetry

## Requirements

- [MySQL](https://www.mysql.com/) (version >= 8.0.28) ([MariaDB](https://mariadb.org/))
- [Python](https://www.python.org/) (version >= [3.8.10](https://www.python.org/downloads/release/python-3810/))
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Dependencies

On Ubuntu

```bash
$ sudo apt install python3-dev libmysqlclient-dev apache2 apache2-dev make libapache2-mod-wsgi-py3
```

## Linux Environment Variables

Variables used for the Project:

- MYSQL_HOST=STRING
- MYSQL_USER=STRING
- MYSQL_PASSWORD=STRING
- MYSQL_DATABASE=STRING
- SHARED_KEY=PATH
- HOST=STRING
- PORT=STRING
- SSL_SERVER_NAME=STRING
- SSL_PORT=STRING
- SSL_CERTIFICATE=PATH
- SSL_KEY=PATH
- SSL_PEM=PATH
- MODE=STRING

## Installation

Install all python packages

### Pip

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## How to use

### Start API

**Python**

```bash
$ MYSQL_HOST= \
  MYSQL_USER= \
  MYSQL_PASSWORD= \
  MYSQL_DATABASE= \
  HOST= \
  PORT= \
  SSL_SERVER_NAME= \
  SSL_PORT= \
  SSL_CERTIFICATE= \
  SSL_KEY= \
  SSL_PEM= \
  MODE=production \
  python3 server.py
```

**MOD_WSGI**

```bash
$ MYSQL_HOST= \
  MYSQL_USER= \
  MYSQL_PASSWORD= \
  MYSQL_DATABASE= \
  HOST= \
  PORT= \
  SSL_SERVER_NAME= \
  SSL_PORT= \
  SSL_CERTIFICATE= \
  SSL_KEY= \
  SSL_PEM= \
  MODE=production \
  mod_wsgi-express start-server wsgi_script.py \
  --user www-data \
  --group www-data \
  --port '${PORT}' \
  --ssl-certificate-file '${SSL_CERTIFICATE}' \
  --ssl-certificate-key-file '${SSL_KEY}' \
  --ssl-certificate-chain-file '${SSL_PEM}' \
  --https-only \
  --server-name '${SSL_SERVER_NAME}' \
  --https-port '${SSL_PORT}'
```

## API Endpoints

### Get statistics

> `GET /statistics`

```json
{}
```

> - Success - 200
> - Server Error - 500
