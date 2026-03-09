"""User model"""
import uuid
from extensions import db


class User(db.Model):
    """Modelo de usuario."""

    __tablename__ = "users"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    pieces = db.relationship("Piece", backref="seller", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
