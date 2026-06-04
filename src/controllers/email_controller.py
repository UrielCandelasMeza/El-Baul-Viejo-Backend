"""Email Controller just to send messages to the owner"""
from flask import request, jsonify
from src.lib.email import send_email_to_user


def send_email():
    """Sends emails to the owner via one function on lib"""
    data = request.get_json()
    print(data)

    name = data.get("name", "").strip() if data else ""

    email = data.get("email", "").strip() if data else ""

    message = data.get("message", "").strip() if data else ""

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Todos los campos son requeridos"}), 400
    email = send_email_to_user(name, email, message)

    if not email:
        return jsonify({
            "success": False, 
            "message": "Hubo un error al momento de enviar los datos, por favor vuelva a intentarlo"
        }), 400

    return jsonify({
        "success": True,
        "message": "Email enviado correctamente"
    }), 200
