from flask import Blueprint, request, jsonify
from app.models import Service
from app import db
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token


service_bp = Blueprint('service_bp', __name__)

#this route creates a new service
@service_bp.route   ('api/service',  methods=['POST'])
def add_service():
    try:
        data = request.get_json()
        new_service = Service(id=data['id'], name=data['name'], description=data['description'],)
        db.session.add(new_service)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}"}), 400
    return jsonify(new_service.to_dict()), 201


#this route gets all services
@service_bp.route  ('api/service', methods=['GET'])
def get_service():
    all_services = Service.query.all()
    return jsonify([service.to_dict() for service in all_services])

