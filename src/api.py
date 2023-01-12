import logging

from flask import Blueprint
from flask import jsonify

from src.models.statistics import Statistics_Model

Routes = Blueprint("Routes", __name__)

logger = logging.getLogger(__name__)

from werkzeug.exceptions import InternalServerError

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