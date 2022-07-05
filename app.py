from flask import Flask,jsonify, request
import os, sys
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import logging

def create_app(object):
    app = Flask(__name__)
    
    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(status=code,error=str(e),message="Something went wrong"), code

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    
    return app
    
    



