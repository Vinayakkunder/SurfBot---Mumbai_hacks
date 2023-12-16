from flask import Flask, request
from flask_cors import CORS, cross_origin
from main import interacter_ask, summarize

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
@cross_origin()
def hello():
  return "Hello World!"

@app.route('/summary',methods = ['POST'])
@cross_origin()
def summarize__():
    url = request.get_json().get('url')
    response = summarize("https://www.youtube.com/watch?v=pApPGFwbigI", "video")
    return {"text": response}

@app.route('/askQuestion',methods = ['POST'])
@cross_origin()
def askQuestion():
    data = request.get_json()
    url = data.get('url')
    question = data.get('question')
    response = interacter_ask("some-url", "video", "query")
    return {"text": response}

if __name__ == "__main__":
  app.run()