import logging
from datetime import datetime
import calendar
import phonenumbers

from peewee import DatabaseError
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers import geocoder

from src.schemas.sessions import Sessions
from src.schemas.usersinfo import UsersInfos

from src.security.data import Data

logger = logging.getLogger(__name__)

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

class Users_Model:
    def __init__(self) -> None:
        """
        """
        self.Sessions = Sessions
        self.UsersInfos = UsersInfos
        self.Data = Data

    def find(self, start: str, end: str, type: str, format: str) -> dict:
        """
        """
        try:
            data = self.Data()

            logger.debug("[*] Start: %s" % start)
            logger.debug("[*] End: %s" % end)
            logger.debug("[*] Type: %s" % type)
            logger.debug("[*] Format: %s" % format)

            result = {
                "total_users": 0,
                "total_countries": 0
            }

            start = datetime.strptime(start, '%Y-%m-%d').date()
            end = datetime.strptime(end, '%Y-%m-%d').date()

            if type == "signup":
                if format == "month":
                    new_start = datetime(start.year, start.month, 1, 0, 0, 0)
                    new_end = datetime(end.year, end.month, calendar.monthrange(end.year, end.month)[1], 23, 59, 59)

                    sessions = (
                        self.Sessions.select(
                            self.Sessions.createdAt,
                            self.Sessions.type
                        )
                        .where(
                            self.Sessions.status == "verified",
                            self.Sessions.type == "signup",
                            self.Sessions.createdAt.between(new_start, new_end)
                        )
                        .order_by(self.Sessions.createdAt.asc())
                    )

                    for session in sessions.iterator():
                        session_date = session.createdAt
                        month_name = calendar.month_name[session_date.month]

                        if not result.get(str(session_date.year)):
                            result[str(session_date.year)] = []

                        if any(month_name in x for x in result[str(session_date.year)]):
                            for x in result[str(session_date.year)]:
                                if x[0] == month_name:
                                    x[1]+=1
                        else:
                            result[str(session_date.year)].append([month_name, 1])

                    result["total_users"] = len(sessions)

                    logger.info("- Success!")

                elif format == "day":
                    new_start = datetime(start.year, start.month, start.day, 0, 0, 0)
                    new_end = datetime(end.year, end.month, end.day, 23, 59, 59)

                    sessions = (
                        self.Sessions.select(
                            self.Sessions.createdAt,
                            self.Sessions.type
                        )
                        .where(
                            self.Sessions.status == "verified",
                            self.Sessions.type == "signup",
                            self.Sessions.createdAt.between(new_start, new_end)
                        )
                        .order_by(self.Sessions.createdAt.asc())
                    )

                    for session in sessions.iterator():
                        session_date = session.createdAt
                        day_name = session_date.strftime("%c")

                        if not result.get(str(session_date.year)):
                            result[str(session_date.year)] = []

                        if any(day_name in x for x in result[str(session_date.year)]):
                            for x in result[str(session_date.year)]:
                                if x[0] == day_name:
                                    x[1]+=1
                        else:
                            result[str(session_date.year)].append([day_name, 1])

                    result["total_users"] = len(sessions)
                
                    logger.info("- Success!")

                else:
                    logger.error("[x] Invalid format '%s'" % format)
                    raise BadRequest()

            elif type == "available":
                if format == "month":
                    new_start = datetime(1970, 1, 1, 0, 0, 0)
                    new_end = datetime(end.year, end.month, calendar.monthrange(end.year, end.month)[1], 23, 59, 59)

                    usersinfos = (
                        self.UsersInfos.select(
                            self.UsersInfos.createdAt,
                            self.UsersInfos.country_code,
                            self.UsersInfos.iv
                        )
                        .where(
                            self.UsersInfos.status == "verified",
                            self.UsersInfos.createdAt.between(new_start, new_end)
                        )
                        .order_by(self.UsersInfos.createdAt.asc())
                    )

                    for usersinfo in usersinfos.iterator():
                        usersinfo_date = usersinfo.createdAt
                        month_name = calendar.month_name[usersinfo_date.month]

                        if not result.get(str(usersinfo_date.year)):
                            result[str(usersinfo_date.year)] = []

                        if any(month_name in x for x in result[str(usersinfo_date.year)]):
                            for x in result[str(usersinfo_date.year)]:
                                if x[0] == month_name:
                                    x[1]+=1
                        else:
                            result[str(usersinfo_date.year)].append([month_name, 1])
                            
                        country_prefix = int(data.decrypt(data = usersinfo.country_code))
                        region_code = region_code_for_country_code(country_prefix)
                        country_name = geocoder._region_display_name(region_code, "en")

                        if not result.get("countries"):
                            result["countries"] = []

                        if any(country_name in x for x in result["countries"]):
                            for x in result["countries"]:
                                if x[0] == country_name and x[1] == region_code:
                                    x[2]+=1
                        else:
                            result["countries"].append([country_name, region_code, 1])

                    result["total_users"] = len(usersinfos)
                    result["total_countries"] = len(result["countries"])

                    logger.info("- Success!")

                elif format == "day":
                    new_start = datetime(1970, 1, 1, 0, 0, 0)
                    new_end = datetime(end.year, end.month, end.day, 23, 59, 59)

                    usersinfos = (
                        self.UsersInfos.select(
                            self.UsersInfos.createdAt,
                            self.UsersInfos.country_code,
                            self.UsersInfos.iv
                        )
                        .where(
                            self.UsersInfos.status == "verified",
                            self.UsersInfos.createdAt.between(new_start, new_end)
                        )
                        .order_by(self.UsersInfos.createdAt.asc())
                    )

                    for usersinfo in usersinfos.iterator():
                        usersinfo_date = usersinfo.createdAt
                        day_name = usersinfo_date.strftime("%c")

                        if not result.get(str(usersinfo_date.year)):
                            result[str(usersinfo_date.year)] = []

                        if any(day_name in x for x in result[str(usersinfo_date.year)]):
                            for x in result[str(usersinfo_date.year)]:
                                if x[0] == day_name:
                                    x[1]+=1
                        else:
                            result[str(usersinfo_date.year)].append([day_name, 1])
                            
                        country_prefix = int(data.decrypt(data = usersinfo.country_code))
                        region_code = region_code_for_country_code(country_prefix)
                        country_name = geocoder._region_display_name(region_code, "en")

                        if not result.get("countries"):
                            result["countries"] = []

                        if any(country_name in x for x in result["countries"]):
                            for x in result["countries"]:
                                if x[0] == country_name and x[1] == region_code:
                                    x[2]+=1
                        else:
                            result["countries"].append([country_name, region_code, 1])

                    result["total_users"] = len(usersinfos)
                    result["total_countries"] = len(result["countries"])

                    logger.info("- Success!")

                else:
                    logger.error("[x] Invalid format '%s'" % format)
                    raise BadRequest()

            else:
                logger.error("[x] Invalid type '%s'" % type)
                raise BadRequest()

            return result

        except DatabaseError as err:
            logger.error("FAILED TO FETCH STATISTICS. See logs below")
            raise InternalServerError(err)