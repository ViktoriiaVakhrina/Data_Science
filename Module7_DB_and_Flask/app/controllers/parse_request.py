from flask import request
from datetime import datetime as dt


def get_request_data():
    """
    Get keys & values from request
    """
    data = request.form

    # request.args: the key/value pairs in the URL query string
    # request.json: parsed JSON data. The request must have the application/json content type, or use request.get_json(force=True) to ignore the content type.
    return data
