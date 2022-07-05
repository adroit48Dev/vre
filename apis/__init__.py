'''
Refer below link for API metadata
https://flask-restplus.readthedocs.io/en/stable/api.html

'''

from flask_restplus import Api
from flask import Blueprint
from .scrappers.routes import ns as NSScrappers

bp_api_v1 = Blueprint('api', __name__)

api = Api(
    bp_api_v1,
    title='Notifications API',
    version='1.0',
    description='A description',
    doc='/docs', #Path of documents,
    validate=True

     
    # All API metadatas
)

api.add_namespace(NSScrappers,path='/scrappers')
