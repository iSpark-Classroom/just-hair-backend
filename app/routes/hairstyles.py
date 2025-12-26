from flask import Blueprint, request, jsonify
from app.models import HairStyle
from app import db
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token

hairstyles_bp = Blueprint('hairstyles_bp', __name__ )

#this route creates a new hairstyle
@hairstyles_bp.route ('/api/hairstyles',  methods=['POST'])
def add_hairstyle():
    try:
        data = request.get_json()
        new_hairstyle = HairStyle(id=data['id'], name=data['name'], picture=data['picture'], category=data['category'], attachments=data['attachments'])
        db.session.add(new_hairstyle)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}"}), 400
    return jsonify(new_hairstyle.to_dict()), 201

#this route gets all hairstyles
@hairstyles_bp.route ('/api/hairstyles', methods=['GET'])
def get_hairstyles():
    all_hairstyles = HairStyle.query.all()
    return jsonify([hairstyle.to_dict() for hairstyle in all_hairstyles])


#this route gets a hairstyle by id
@hairstyles_bp.route('/api/hairstyle/<int:id>', methods=['GET'])
def get_hairstyle_by_id(id):
    hairstyle = HairStyle.query.get(id)
    if not hairstyle:
        return jsonify({"error": "hairstyle not found"}), 404
    return jsonify(hairstyle.to_dict()), 200


#this route updates a hairstyle based on id
@hairstyles_bp.route('/api/hairstyle/<int:id>', methods=['PUT'])
def update_hairstyle(id):
    data = request.get_json()
    hairstyle = HairStyle.query.get(id)
    if not hairstyle:
        return jsonify({"error": "hairstyle not found"}), 404
    hairstyle.name = data.get('name', hairstyle.name)
    hairstyle.picture = data.get('picture', hairstyle.picture)
    hairstyle.category = data.get('category', hairstyle.category)
    hairstyle.attachments = data.get('attachments', hairstyle.attachments)
    db.session.commit()
    return jsonify(hairstyle.to_dict()), 200


#this route deletes a hairstyle based on id
@hairstyles_bp.route('/api/hairstyle/<int:id>', methods=['DELETE'])
def delete_hairstyle(id):
    hairstyle = HairStyle.query.get(id)
    if not hairstyle:
        return jsonify({"error": "hairstyle not found"}), 404
    db.session.delete(hairstyle)
    db.session.commit()
    return jsonify({"message": "hairstyle deleted"}), 200

