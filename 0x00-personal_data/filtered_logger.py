#!/usr/bin/env python3
"""
A function called filter_datum that returns the log message obfuscated
"""
import re
from typing import List


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
