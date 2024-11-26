# import flask, flask_googleauth
import os
from flask import Flask, redirect, url_for, session, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from flask_restx import Namespace, Resource, reqparse, fields
from core import querycore

# Load Google client credentials
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP for local dev
GOOGLE_CLIENT_SECRETS_FILE = "googleclient.json"  # Your OAuth client secrets file

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    """User model for flask-login."""
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

# Store users in a dictionary for the example
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)
   

@app.route("/login/callback")
def callback():
    # Check for state mismatch
    if 'state' not in session:
        return "State missing in session", 400
    if session['state'] != request.args.get('state'):
        print("error")
        return "State mismatch error", 400
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        state=session['state'],
        redirect_uri=url_for('callback', _external=True)
    )
    # authorization_url, state = flow.authorization_url()
    # session['state'] = state
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = Request()

    try:
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, request_session, flow.client_config['client_id']
        )
    except ValueError as e:
        return "Invalid token: " + str(e)

    # Now, id_info contains the user info as a dictionary
    google_id = id_info["sub"]
    name = id_info["name"]
    email = id_info["email"]
    # Check if the email domain is allowed
    allowed_domain = "iitrpr.ac.in"  # Change this to your organization's domain
    if not email.endswith(f"@{allowed_domain}"):
        return "Access denied: External users are not allowed to log in.", 403

    # Create and store the user
    user = User(google_id, name, email)
    users[google_id] = user
    session['google_id'] = google_id
    
    # Login user with Flask-Login
    login_user(user)

    return redirect(url_for("home"))


@app.route('/login')
def login():
    session.clear()
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=url_for('callback', _external=True)
    )
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))

@app.route('/')
def home():
    if "google_id" in session:
        user = users.get(session["google_id"])
        return f"Hello, {user.name}! Welocome to RPR GPT<br> <a href='/logout'>Logout</a>"
    else:
        return "You are not logged in. <br> <a href='/login'>Login with Google</a>" 


api = Namespace('collection',description='Collection related OPERATIONS')

query_model = api.model('query_model', {
    'query': fields.String(required=True, description='What do you want to ask'),
    'year': fields.String(required=True, description='year of joining'),
    'pursuing': fields.String(required=True, description='UG/PG')
})
@api.route('/query')
class answerquery(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @api.expect(query_model)
    def post(self):
        try:
            args = query_model.parse_args()
            result = querycore.getResponse(args['query'])
            # result={}
            return result,200     
        except Exception as e:
            api.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")




if __name__ =="__main__":
    app.run(debug=True)