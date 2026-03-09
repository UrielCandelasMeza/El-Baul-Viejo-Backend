"""Routes for the category"""
from flask import Blueprint
from src.controllers.category_controller import (
    get_categories,
    create_category,
    delete_category,
)
from src.lib.jwt import jwt_required_cookie

category_bp = Blueprint("category", __name__)

@category_bp.route("/get", methods=["GET"])
def get():
    return get_categories()
@category_bp.route("/create", methods=["POST"])
@jwt_required_cookie
def create():
    return create_category()
@category_bp.route("/delete/<string:category_id>", methods=["DELETE"])
@jwt_required_cookie
def delete(category_id: str):
    return delete_category(category_id=category_id)
