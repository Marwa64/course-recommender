import flask
from flask import request
import json
from flask import jsonify
from flask_cors import CORS
from database_connection import get_database
from recommender import recommend_course

app = flask.Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})
app.config["DEBUG"] = True

db = get_database()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Recommender System</h1>"


# A route to return top 9 job recommendations
@app.route('/course/recommend', methods=['POST'])
def courses():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        payload = request.json

        recomm = recommend_course(payload["skill"], payload["user_id"])
        print(recomm)
        result_dict = []

        return jsonify(recomm)

    else:
        return 'Content-Type not supported!'


app.run()
