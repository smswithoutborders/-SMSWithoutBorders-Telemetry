import logging
logger = logging.getLogger(__name__)

# configurations
from Configs import baseConfig
config = baseConfig()
api = config["API"]

from flask import Blueprint
from flask import jsonify

from models.statistics import Statistics_Model

Routes = Blueprint("Routes", __name__)

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