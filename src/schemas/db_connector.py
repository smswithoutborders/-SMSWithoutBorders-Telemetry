from peewee import MySQLDatabase, DatabaseError

from settings import Configurations
db_name = Configurations.MYSQL_DATABASE
db_host = Configurations.MYSQL_HOST
db_password = Configurations.MYSQL_PASSWORD
db_user = Configurations.MYSQL_USER

try:
    db = MySQLDatabase(
        db_name,
        user=db_user,
        password=db_password,
        host=db_host,
    )

except DatabaseError as error:
    raise error