from flask import Blueprint
from src.controllers.email_controller import send_email

email_bp = Blueprint("email", __name__)

email_bp.route("/send", methods=["POST"])(send_email)
