import os

class Configurations:
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

    SHARED_KEY = os.environ.get("SHARED_KEY")

    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")