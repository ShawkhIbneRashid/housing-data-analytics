from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#app = Flask(__name__, template_folder='../../frontend/src')
app.secret_key = "@##WDSA,xhfef1231223&*(((}}"
CORS(app)