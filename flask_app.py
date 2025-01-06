from flask import Flask,redirect,make_response
from main import main
from config import flask_app_config


app = Flask(__name__)


# Homepage a http://localhost:8033
@app.route("/")
def healt():
    return "Ok"

@app.route("/reload")
def reload():
    main()
    return redirect("http://raffosberry.local/board")


if __name__ == '__main__':
    app.run(**flask_app_config)
