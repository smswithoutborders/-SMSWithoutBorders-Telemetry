import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
api = config["API"]

from peewee import DatabaseError

from schemas.sessions import Sessions
from schemas.users import Users
from schemas.usersinfo import UsersInfos

from werkzeug.exceptions import InternalServerError

class Statistics_Model:
    def __init__(self) -> None:
        """
        """
        self.Sessions = Sessions
        self.Users = Users
        self.UsersInfos = UsersInfos

    def find(self) -> str:
        """
        """
        try:
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
                    ((self.Sessions.status == None) & (self.Sessions.type == "publisher")) |
                    ((self.Sessions.status == None) & (self.Sessions.type == "active"))
                )
                .dicts()
            )

            for session in sessions.iterator():
                result.append({
                    "date": session["createdAt"],
                    "type": session["type"]
                })

            logger.info("- Successfully fetched sessions")

            users = (
                self.Users.select(
                    self.Users.current_login
                )
                .where(
                    self.Users.current_login != None
                )
                .dicts()
            )

            for user in users:
                result.append({
                    "date": user["current_login"],
                    "type": "active"
                })

            logger.info("- Successfully fetched active users")

            usersinfos = (
                self.UsersInfos.select(
                    self.UsersInfos.createdAt,
                )
                .where(
                    self.UsersInfos.status == "verified"
                )
                .dicts()
            )

            for usersinfo in usersinfos.iterator():
                result.append({
                    "date": usersinfo["createdAt"],
                    "type": "available"
                })

            logger.info("- Successfully fetched available users")

            return result

        except DatabaseError as err:
            logger.error("FAILED TO FETCH STATISTICS. See logs below")
            raise InternalServerError(err)