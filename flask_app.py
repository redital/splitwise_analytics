from flask import Flask,redirect,request
from main import main
from config import flask_app_config, DASHBOARD_HOSTNAME


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
    return redirect("http://{}.local/board".format(DASHBOARD_HOSTNAME))


if __name__ == '__main__':
    app.run(**flask_app_config)
