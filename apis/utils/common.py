from flask import make_response, jsonify, request
from random import randint
from datetime import datetime, date, time, timedelta
import datetime


def output_json(data,message,status=True,code=200,headers=None):
    """ 
    code :
        200 : Status ok, success
        201 : Failed opretion
        202 : ALready exists
    """
    datares=jsonify(data=data,status=status,message=message)
    resp = make_response(datares, code)
    resp.headers.extend(headers or {})
    return resp