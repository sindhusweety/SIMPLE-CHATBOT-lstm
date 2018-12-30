from flask import Flask, render_template, request
from flask import jsonify
from model import response


app = Flask(__name__, static_url_path="/static")
@app.route('/message', methods=['POST'])
def reply():
    text = request.form['msg']
    result = response(text)
    return jsonify({'text':result})
@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

    # start app
if (__name__ == "__main__"):
    app.run(port=5000)
