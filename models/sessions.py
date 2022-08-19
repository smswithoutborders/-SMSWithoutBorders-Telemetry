import logging
from unittest import result
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
api = config["API"]

from peewee import DatabaseError

from schemas.sessions import Sessions

from werkzeug.exceptions import InternalServerError

class Session_Model:
    def __init__(self) -> None:
        """
        """
        self.Sessions = Sessions

    def find(self) -> str:
        """
        """
        try:
            logger.debug("finding session ...")

            result = []

            sessions = (
                self.Sessions.select()
                .where(
                    ((self.Sessions.status == "verified") & (self.Sessions.type == "signup")) |
                    ((self.Sessions.status == "updated") & (self.Sessions.type == "recovery")) |
                    ((self.Sessions.status == None) & (self.Sessions.type == "publisher"))
                )
                .dicts()
            )

            for session in sessions:
                del session["data"]
                del session["expires"]
                del session["sid"]
                del session["user_agent"]
                del session["unique_identifier"]
                del session["status"]

                result.append(session)

            logger.info("- Successfully fetched sessions")
            return result

        except DatabaseError as err:
            logger.error("FAILED FETCH SESSION")
            raise InternalServerError(err)