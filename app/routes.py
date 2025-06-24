from flask import Blueprint, request, jsonify
from app.services import process_identity

identify_blueprint = Blueprint('identify', __name__)  # ✅ Correct blueprint name

@identify_blueprint.route('/identify', methods=['POST'])  # ✅ Correct path
def identify():
    data = request.get_json()

    email = data.get('email')
    phone = data.get('phoneNumber')

    if not email and not phone:
        return jsonify({"error": "email or phoneNumber required"}), 400

    result = process_identity(email=email, phone=phone)
    return jsonify(result), 200
