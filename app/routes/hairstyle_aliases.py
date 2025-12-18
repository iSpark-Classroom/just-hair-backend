from flask import Blueprint, request, jsonify
from app.models import HairStyleAlias
from app import db
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token    

hairstyle_aliases_bp = Blueprint('hairstyle_aliases_bp', __name__ )

#this route creates a new hairstyle alias
@hairstyle_aliases_bp.route ('/api/hairstyle_aliases',  methods=['POST'])
def add_hairstyle_alias():
    try:
        data = request.get_json()
        new_hairstyle_alias = HairStyleAlias(id=data['id'], alias_name=data['alias_name'], service_provider_hairstyle_id=data['service_provider_hairstyle_id'])
        db.session.add(new_hairstyle_alias)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}"}), 400
    return jsonify(new_hairstyle_alias.to_dict()), 201

#this route gets all hairstyle aliases
@hairstyle_aliases_bp.route ('/api/hairstyle_aliases', methods=['GET'])
def get_hairstyle_aliases():
    all_hairstyle_aliases = HairStyleAlias.query.all()
    return jsonify([hairstyle_alias.to_dict() for hairstyle_alias in all_hairstyle_aliases])
    

#this route gets hairstyle aliases by hairstyle id
@hairstyle_aliases_bp.route ('/api/hairstyle_aliases/<int:service_provider_hairstyle_id>', methods=['GET'])
def get_hairstyle_aliases_by_service_provider_hairstyle_id(service_provider_hairstyle_id):
    aliases = HairStyleAlias.query.filter_by(service_provider_hairstyle_id=service_provider_hairstyle_id).all()
    return jsonify([alias.to_dict() for alias in aliases])


#this route updates a hairstyle alias based on id
@hairstyle_aliases_bp.route ('/api/hairstyle_aliases/<int:id>', methods=['PUT'])
def update_hairstyle_alias(id):
    try:
        data = request.get_json()
        hairstyle_alias = HairStyleAlias.query.get(id)
        if not hairstyle_alias:
            return jsonify({"message": "error", "error": "hairstyle alias not found"}), 404
        hairstyle_alias.service_provider_hairstyle_id = data['service_provider_hairstyle_id']
        hairstyle_alias.alias_name = data['alias_name']
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}"}), 400
    return jsonify(hairstyle_alias.to_dict()), 200


#this route deletes a hairstyle alias based on id
@hairstyle_aliases_bp.route ('/api/hairstyle_aliases/<int:id>', methods=['DELETE'])
def delete_hairstyle_alias(id):
    hairstyle_alias = HairStyleAlias.query.get(id)
    if not hairstyle_alias:
        return jsonify({"message": "error", "error": "hairstyle alias not found"}), 404
    db.session.delete(hairstyle_alias)
    db.session.commit()
    return jsonify({"message": "hairstyle alias deleted"}), 200