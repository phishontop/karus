from flask import Blueprint, render_template

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/", methods=['GET'])
def home():
    return render_template('home/index.html')
