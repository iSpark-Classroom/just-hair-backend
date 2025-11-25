from flask import Blueprint, request, jsonify

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/test")
def test():
    return jsonify({"message": "Routes working!"})
