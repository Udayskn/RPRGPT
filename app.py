# import flask, flask_googleauth
import os
from flask import Flask, redirect, url_for, session, request
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from flask_restx import Namespace, Resource, reqparse, fields,Api
from core import responsecore

app = Flask(__name__)
app.secret_key = os.urandom(24)

ns = Namespace('Home', description='Main operations')
api = Api(app)
query_model = ns.model('query_model', {
    'query': fields.String(required=True, description='What do you want to ask'),
    'pursuing':fields.String(required=True, description="UGYYYY or faculty or clubs")
})
@ns.route('/ask')
class answerquery(Resource):
    @ns.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @ns.expect(query_model)
    def post(self):
        try:
            payload = api.payload  # This will contain the JSON body of the request
        
             # Extract the 'query' field
            query_text = payload.get('query', None)
            query_year = payload.get('pursuing',None)

            if not query_text or not query_year:
                return {"error": "Query year or text is missing"}, 400
            result = responsecore.getResponse(query_text, query_year)
            # result={}
            return result,200     
        except Exception as e:
            api.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")

api.add_namespace(ns)
if __name__ =="__main__":
    app.run(debug=True)