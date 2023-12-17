from flask import Flask, request
from flask_cors import CORS, cross_origin
from main import interacter_ask, summarize
import re

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
    response = summarize(url)
    return {"text": response}

@app.route('/askQuestion',methods = ['POST'])
@cross_origin()
def askQuestion():
    try:
      data = request.get_json()
      url = data.get('url')
      question = data.get('question')
      if 'summary' in question.lower() or 'summarize' in question.lower() : 
        response = summarize(url)
      elif 'time' in question.lower() or 'timestamp' in question.lower():
        time = interacter_ask(url, question)
        timeStamps = re.findall(r'\d+', time)
        if len(timeStamps) > 0:
            response = url + '&t=' + timeStamps[0] + 's'
        else:
            response = "the text you are searching is not explained in this video"
      else:
        response = interacter_ask(url, question)
      return {"text": response}
    except:
       return {"text": "please try after some time"}

if __name__ == "__main__":
  app.run()