from flask import Blueprint, render_template

lookup_blueprint = Blueprint('lookup', __name__, url_prefix='/lookup')


@lookup_blueprint.route("/username", methods=['GET'])
def username_lookup():
    return render_template('username/index.html')


@lookup_blueprint.route("/fullname", methods=['GET'])
def fullname_lookup():
    return render_template('fullname/index.html')


@lookup_blueprint.route("/discord", methods=['GET'])
def discord_lookup():
    return render_template('discord/index.html')
