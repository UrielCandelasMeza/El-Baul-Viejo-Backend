"""Category controller"""
from flask import request, jsonify
from sqlalchemy import func
from extensions import db
from src.models.category_model import Category


def get_categories():
    """Returns all categories"""
    categories = db.session.execute(
        db.select(Category).order_by(Category.name)
    ).scalars().all()

    return jsonify({
        "success": True,
        "categories": [c.to_dict() for c in categories]
    }), 200


def create_category():
    """Creates a new category"""
    data = request.get_json()
    name = data.get("name", "").strip() if data else ""

    if not name:
        return jsonify({"success": False, "message": "El nombre es requerido"}), 400

    # Search duplicated
    existing = db.session.execute(
        db.select(Category).where(func.lower(Category.name) == name.lower())
    ).scalar_one_or_none()

    if existing:
        return jsonify({"success": False, "message": "Ya existe una categoría con ese nombre"}), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Categoría creada exitosamente",
        "category": category.to_dict()
    }), 201


def delete_category(category_id: str):
    """Deletes a category"""
    # Por PK — aquí sí aplica db.session.get()
    category = db.session.get(Category, category_id)

    if not category:
        return jsonify({"success": False, "message": "Categoría no encontrada"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"success": True, "message": "Categoría eliminada exitosamente"}), 200
