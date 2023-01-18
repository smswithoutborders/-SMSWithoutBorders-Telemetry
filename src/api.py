import logging

from flask import Blueprint
from flask import jsonify

from src.models.statistics import Statistics_Model
from src.schemas.db_connector import db

Routes = Blueprint("Routes", __name__)

logger = logging.getLogger(__name__)

from werkzeug.exceptions import InternalServerError

@Routes.before_request
def before_request():
    db.connect()

@Routes.after_request
def after_request(response):
    db.close()
    return response

@Routes.route("/statistics", methods=["GET"])
def statistics():
    """
    """
    try:
        Session = Statistics_Model()

        res = Session.find()

        return jsonify(res), 200
                
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500