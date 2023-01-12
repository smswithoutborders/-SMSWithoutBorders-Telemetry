import logging
import argparse

from settings import Configurations

HOST = Configurations.HOST
PORT = Configurations.PORT

from flask import Flask
from flask_cors import CORS

from src.api import Routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(Routes)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", help="Set log level")
    args = parser.parse_args()

    log_level = args.logs or "info"
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)

    logging.basicConfig(level=numeric_level)

    app.logger.info("Running on un-secure port: %s" % PORT)
    app.run(host=HOST, port=PORT)