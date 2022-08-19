import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()
database = config["DATABASE"]

import os
import json

from schemas.baseModel import db
from contextlib import closing
from mysql.connector import connect
from mysql.connector import Error

from schemas.sessions import Sessions
from schemas.users import Users

def create_database() -> None:
    """
    """
    try:
        with closing(
            connect(
                user=database["MYSQL_USER"],
                password=database["MYSQL_PASSWORD"],
                host=database["MYSQL_HOST"],
                auth_plugin="mysql_native_password",
            )
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS %s;" % database['MYSQL_DATABASE']

            with closing(connection.cursor()) as cursor:
                logger.debug("Creating database %s ..." % database['MYSQL_DATABASE'])

                cursor.execute(create_db_query)

                logger.info("- Database %s successfully created" % database['MYSQL_DATABASE'])

    except Error as error:
        raise error

    except Exception as error:
        raise error

def create_tables() -> None:
    """
    """
    try:
        logger.debug("Syncing database %s ..." % database['MYSQL_DATABASE'])

        db.create_tables([
            Sessions,
            Users
        ])

        logger.info("- Successfully Sync database %s" % database['MYSQL_DATABASE'])

    except Exception as error:
        raise error