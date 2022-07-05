from flask_restplus import Namespace, fields
import time
from datetime import datetime, date, time, timedelta
from flask import jsonify, request
import requests
import json
import urllib.request
from apis.utils.bnb_scraper import BnB_scraper
from apis.utils.common import output_json

import logging


def bnb(self):
    requestData = request.json
    print(requestData, "requestData")
    status = True
    message = ""
    responseData = {}
    responseData = BnB_scraper(requestData)
    response = output_json(responseData,message,status)
    logging.debug('notification_send_request: {}'.format(response))
    return response