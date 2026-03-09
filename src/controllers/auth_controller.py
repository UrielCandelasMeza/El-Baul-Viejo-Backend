"""Auth controller to manage register, login and verify tokens from user"""
from flask import request, jsonify, make_response
from extensions import db, bcrypt
from src.models.user_model import User
from src.lib.jwt import generate_tokens
from flask_jwt_extended import get_jwt_identity, unset_jwt_cookies

def register_user():
    """Register a new user"""
    data = request.get_json()

    name = data.get("name")
    username = data.get("username")
    password = data.get("password")

    if not name or not username or not password:
        return jsonify({
            "success": False,
            "message": "Hay datos faltantes"
        }),400

    user_found = User.query.filter_by(username=username).first()

    if user_found:
        return jsonify({
            "success": False,
            "message": "Usuario existente"
        }), 409
    hashed_password = bcrypt.generate_password_hash(password=password).decode("utf-8")

    new_user = User(
        username=username,
        password=hashed_password,
        name=name
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Usuario creado exitosamente"
    })

def login_user():
    """User login into his account"""
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Hay datos faltantes"
        }), 400

    user_found = User.query.filter_by(username=username).first()

    if not user_found:
        return jsonify({
            "success": False,
            "message": "El usuario no existe"
        }), 404

    hashed_password = bcrypt.check_password_hash(user_found.password, password)

    if not hashed_password:
        return jsonify({
            "success": False,
            "message": "La contraseña es incorrecta"
        }), 401

    user_data = {
        "id": str(user_found.id),
        "username": user_found.username,
        "name": user_found.name
    }
    return generate_tokens(user_found.id, user_data)

def verify_token():
    """Verifica el token JWT y retorna el usuario autenticado"""
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    return jsonify({
        "success": True,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "name": user.name
        }
    }), 200


def logout_user():
    """Limpia las cookies JWT del navegador"""
    response = make_response(jsonify({"success": True, "message": "Sesión cerrada"}))
    unset_jwt_cookies(response)
    return response, 200
