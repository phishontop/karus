from flask import Blueprint, jsonify, request
from .modules import LookupFactory

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/api/lookup/", methods=['POST'])
def lookup():

    payload = request.get_json()
    modules = payload["modules"]

    lookup_objects = [
        LookupFactory.create_lookup_object(module=module, kwargs={"name": payload["name"]})
        for module in modules
    ]
    data = {}
    for lookup_object in lookup_objects:
        data = {
            **data,
            **lookup_object.run()
        }

    return jsonify(data)
