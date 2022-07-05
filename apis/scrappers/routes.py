from flask import request, Response, make_response, jsonify
from flask_restplus import Resource,Namespace, marshal_with
from bson import json_util
import json
from .model import bnb


ns = Namespace('scrappers', description='Spa projects notifications related operations')


@ns.route('/')
class Scrappers(Resource):
    #@ns.marshal_with(_post)
    #@ns.expect(_post, validate=True)
    @ns.response(201, 'User successfully created.')
    @ns.doc('create new post')
    def post(self):
        """Creates a new User """
        # data = request.json
        return bnb(self)