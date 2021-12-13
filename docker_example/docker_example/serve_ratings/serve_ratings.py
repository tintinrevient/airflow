import pandas as pd
import time
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import os
from werkzeug.security import generate_password_hash, check_password_hash


def _load_ratings(input_path):
    """Load ratings into memory"""
    ratings = pd.read_csv(input_path)
    ratings = ratings.sample(n=100000, random_state=0)
    ratings = ratings.sort_values(by=["timestamp", "userId", "movieId"])

    return ratings


def _date_to_timestamp(date_str):
    if date_str is None:
        return None
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d")))


app = Flask(__name__)
app.config["ratings"] = _load_ratings("data/ratings.csv")

auth = HTTPBasicAuth()
users = {os.environ["API_USER"]: generate_password_hash(os.environ["API_PASSWORD"])}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route("/")
def hello():
    return "Hello"

@app.route("/ratings")
@auth.login_required()
def ratings():
    start_date_ts = _date_to_timestamp(request.args.get("start_date", None))
    end_date_ts = _date_to_timestamp(request.args.get("end_date", None))
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 100))

    ratings = app.config.get("ratings")

    if start_date_ts:
        ratings = ratings.loc[ratings["timestamp"] >= start_date_ts]
    if end_date_ts:
        ratings = ratings.loc[ratings["timestamp"] < end_date_ts]

    subset = ratings.iloc[offset:offset+limit]

    return jsonify(
        {
            "result": subset.to_dict(orient="records"),
            "offset": offset,
            "limit": limit,
            "total": ratings.shape[0]
        }
    )

if __name__ == "__main__":
    app.run()
