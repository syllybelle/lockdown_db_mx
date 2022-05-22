# covidDB properties

import mysql
from mysql.connector import MySQLConnection


class DbProperties:
    def __init__(self, host: str = "default",
                 user: str = "default",
                 password: str = "default",
                 db_name="default") -> None:
        if host == "default":
            self.host = "localhost"
        else:
            self.host = host
        if user == "default":
            self.user = "root"
        else:
            self.user = user
        if password == "default":
            self.password = "uppsalalocalcoviddata"
        else:
            self.password = password
        if db_name == "default":
            self.db_name = "covid_data"
        else:
            self.db_name = db_name

    def connect(self) -> MySQLConnection:
        connection: MySQLConnection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name)
        return connection
