## SMSWithoutBorders-Telemetry

## Requirements

- [Python](https://www.python.org/) (version >= [3.8.10](https://www.python.org/downloads/release/python-3810/))
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Installation

Create a Virtual Environments **(venv)**

```
python3 -m venv venv
```

Move into Virtual Environments workspace

```
. venv/bin/activate
```

Install all python packages

```
pip install -r requirements.txt
```

## Configurations

Copy `example.default.ini` to `default.ini`

```bash
cp configs/example.default.ini configs/default.ini
```

## How to use

### Start api

```bash
python3 server.py
```

set log levels with the `--logs` variable. Default = "INFO"

```bash
python3 server.py --logs=debug
```

## API Endpoints

### Get statistics

> `GET /statistics`

```json
{}
```

> - Success - 200
> - Server Error - 500
