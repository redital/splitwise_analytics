from flask import Flask,redirect,request
from main import main
from config import flask_app_config


app = Flask(__name__)


# Homepage a http://localhost:8033
@app.route("/")
def healt():
    return "Ok"

@app.route("/reload")
def reload():
    force = request.args.get('force')
    force = (force.lower()=="true")
    main(force)
    return redirect("http://raffosberry.local/board")


if __name__ == '__main__':
    app.run(**flask_app_config)
