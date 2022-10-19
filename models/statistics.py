import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
api = config["API"]

from peewee import DatabaseError

from schemas.sessions import Sessions
from schemas.usersinfo import UsersInfos

from security.data import Data

from werkzeug.exceptions import InternalServerError

class Statistics_Model:
    def __init__(self) -> None:
        """
        """
        self.Sessions = Sessions
        self.UsersInfos = UsersInfos
        self.Data = Data

    def find(self) -> str:
        """
        """
        try:
            data = self.Data()

            logger.debug("finding statistics ...")

            result = []

            sessions = (
                self.Sessions.select(
                    self.Sessions.createdAt,
                    self.Sessions.type
                )
                .where(
                    ((self.Sessions.status == "verified") & (self.Sessions.type == "signup")) |
                    ((self.Sessions.status == "updated") & (self.Sessions.type == "recovery")) |
                    ((self.Sessions.status == None) & (self.Sessions.type == "publisher"))
                )
                .dicts()
            )

            for session in sessions.iterator():
                result.append({
                    "date": session["createdAt"],
                    "type": session["type"]
                })

            logger.info("- Successfully fetched sessions")

            usersinfos = (
                self.UsersInfos.select(
                    self.UsersInfos.createdAt,
                    self.UsersInfos.country_code,
                    self.UsersInfos.iv
                )
                .where(
                    self.UsersInfos.status == "verified"
                )
                .dicts()
            )

            for usersinfo in usersinfos.iterator():
                result.append({
                    "date": usersinfo["createdAt"],
                    "type": "available",
                    "country_code": data.decrypt(
                        data = usersinfo["country_code"],
                        iv = usersinfo["iv"]
                    )
                })

            logger.info("- Successfully fetched available users")

            return result

        except DatabaseError as err:
            logger.error("FAILED TO FETCH STATISTICS. See logs below")
            raise InternalServerError(err)