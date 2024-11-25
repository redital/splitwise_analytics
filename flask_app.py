from flask import Flask, jsonify, make_response,redirect,render_template
from flask import request as flask_request
from urllib.parse import urlencode
from main import main


app = Flask(__name__)


# Homepage a http://localhost:8033
@app.route("/")
def hello_world():
    main()
    return redirect("http://raffosberry.local/board")




if __name__ == '__main__':
    app.run(port=8033,debug=True)
