import logging

from flask import Blueprint, jsonify, request

from src.models.statistics import Statistics_Model
from src.models.users import Users_Model

from src.schemas.db_connector import db

Routes = Blueprint("Routes", __name__)

logger = logging.getLogger(__name__)

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

@Routes.before_request
def before_request():
    db.connect()

@Routes.after_request
def after_request(response):
    db.close()
    return response

@Routes.route("/users", methods=["GET"])
def users():
    """
    """
    try:
        start = request.args.get("start")
        end = request.args.get("end")
        type = request.args.get("type")
        format = request.args.get("format")

        Users = Users_Model()

        data = Users.find(
            start=start,
            end=end,
            type=type,
            format=format
        )

        return jsonify(data), 200
                
    except BadRequest as err:
        return str(err), 400
    
    except InternalServerError as err:
        logger.exception(err)
        return "internal server error", 500

    except Exception as err:
        logger.exception(err)
        return "internal server error", 500