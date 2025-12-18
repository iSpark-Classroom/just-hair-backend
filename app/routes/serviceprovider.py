from flask import Blueprint, request, jsonify
from app.models import ServiceProvider
from app import db
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token

serviceprovider_bp = Blueprint('serviceprovider_bp', __name__)

#this route is to get all service providers
@serviceprovider_bp.route ('/api/serviceproviders', methods=['GET'])
def get_serviceproviders():
    all_serviceproviders = ServiceProvider.query.all()
    return jsonify([serviceprovider.to_dict() for serviceprovider in all_serviceproviders])

#this route creates a new service provider
@serviceprovider_bp.route ('/api/serviceprovider' , methods=['POST'])
def add_serviceprovider():
    try:
        data = request.get_json()
        new_serviceprovider = ServiceProvider(role=data['role'], surname=data['surname'], given_name=data['given_name'], id_card_number=data['id_card_number'], phone_number=data['phone_number'], location=data['location'], about=data['about'], email=data['email'], password=data['password'])
        db.session.add(new_serviceprovider)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}"}), 400
    return jsonify(new_serviceprovider.to_dict()), 201



#this route updates all service provider
@serviceprovider_bp.route('/api/serviceprovider/<int:id>', methods=['PUT'])
def update_serviceprovider(id):
    data = request.get_json()
    serviceprovider = ServiceProvider.query.get(id)
    if not serviceprovider:
        return jsonify({"error": "service provider not avaliable"}), 404
    serviceprovider.role = data.get('role', serviceprovider.role)
    serviceprovider.surname = data.get('surname', serviceprovider.surname)
    serviceprovider.given_name =data.get('given_name', serviceprovider.given_name)
    serviceprovider.email = data.get('email', serviceprovider.email)
    serviceprovider.id_card_number = data.get('id_card_number', serviceprovider.id_card_number)
    serviceprovider.phone_number = data.get('phone_number', serviceprovider.phone_number)
    serviceprovider.location = data.get('location', serviceprovider.location)
    serviceprovider.about = data.get('about', serviceprovider.about)
    serviceprovider.password = data.get('password', serviceprovider.password)
    db.session.commit()
    return jsonify(serviceprovider.to_dict()), 200



#this route deletes a service provider based on id
@serviceprovider_bp.route('/api/serviceprovider/<int:id>', methods=['DELETE'])
def delete_serviceprovider(id):
    serviceprovider = ServiceProvider.query.get(id)
    if not serviceprovider:
        return jsonify({"error": "service provider not found"}), 404
    db.session.delete(serviceprovider)
    db.session.commit()
    return jsonify({"message": "service provider deleted successfully"}), 200