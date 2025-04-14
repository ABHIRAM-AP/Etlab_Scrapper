from flask import Flask, request
from web import fetch_data

app = Flask(__name__)


@app.route("/get_data", methods=['POST'])
def get_data():
  data = request.get_json()
  userID = data.get('userID')
  password = data.get('password')
  return fetch_data(userID, password)


if __name__ == "__main__":
     from os import getenv
     port = int(getenv('PORT', 5000))  
     app.run(host='0.0.0.0', port=port)
