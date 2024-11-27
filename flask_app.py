from flask import Flask,redirect,url_for
from main import main
from config import flask_app_config


app = Flask(__name__)


# Homepage a http://localhost:8033
@app.route("/")
def index():
    main()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(**flask_app_config)
