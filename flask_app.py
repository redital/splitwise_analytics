from flask import Flask,redirect,request
from main import main
from config import flask_app_config, DASHBOARD_HOSTNAME


app = Flask(__name__)


@app.route("/")
def healt():
    return "Ok"

@app.route("/reload")
def reload():
    force = request.args.get('force',"false")
    force = (force.lower()=="true")
    main(force)
    return redirect("http://{}.local".format(DASHBOARD_HOSTNAME))


if __name__ == '__main__':
    app.run(**flask_app_config)
