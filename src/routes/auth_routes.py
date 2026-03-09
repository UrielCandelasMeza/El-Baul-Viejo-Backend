"""Auth Routes"""

from flask import Blueprint
from src.controllers.auth_controller import register_user, login_user, verify_token, logout_user
from src.lib.jwt import jwt_required_cookie

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register",methods=["POST"])
def register():
    """Controller"""
    return register_user()

@auth_bp.route("/login", methods=["POST"])
def login():
    """Controller"""
    return login_user()

@auth_bp.route("/verify", methods=["GET"])
@jwt_required_cookie
def verify():
    """Verifica el token JWT y retorna el usuario autenticado"""
    return verify_token()

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Cierra la sesión eliminando las cookies JWT"""
    return logout_user()
