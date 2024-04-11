#!/usr/bin/env python3
"""
A function called filter_datum that returns the log message obfuscated
"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates sensitive fields in a log message.

    Arguments:
    fields:
        list of strings representing fields to obfuscate.
    redaction:
        string representing the value to replace sensitive fields with.
    message:
        string representing the log line.
    separator:
        string representing the character separating fields in the log line.

    Returns:
    string:
        The log message with sensitive fields obfuscated.
    """
    for field in fields:
        message = re.sub(rf"{field}=(.*?)\{separator}",
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize method
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format method
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    A function that takes no arguments and returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    A function that returns a connector to the MySQL database
    """
    db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return db


def main() -> None:
    """
    A function that will obtain a database connection using get_db
    and retrieve all rows in the users table
    and display each row under a filtered format
    """
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        message = "; ".join(
            f"{field}={value} " for field, value in zip(PII_FIELDS, rows)
        )
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
