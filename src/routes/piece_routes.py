"""Routes for the piece"""
from flask import Blueprint
from src.controllers.piece_controller import (
    create_piece,
    get_all_pieces,
    get_available_pieces,
    get_one_piece,
    update_piece,
    delete_piece,
)
from src.lib.jwt import jwt_required_cookie

piece_bp = Blueprint("piece", __name__)

piece_bp.route("/create", methods=["POST"])(jwt_required_cookie(create_piece))
piece_bp.route("/update/<string:piece_id>", methods=["PUT"])(jwt_required_cookie(update_piece))
piece_bp.route("/delete/<string:piece_id>", methods=["DELETE"])(jwt_required_cookie(delete_piece))
piece_bp.route("/get", methods=["GET"])(get_all_pieces)
piece_bp.route("/get/available", methods=["GET"])(get_available_pieces)
piece_bp.route("/get/<string:piece_id>", methods=["GET"])(get_one_piece)
