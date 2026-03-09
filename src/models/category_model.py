"""Category model"""
import uuid
from extensions import db

class Category(db.Model):
    """Model"""
    __tablename__ = "categories"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
        }

    def __repr__(self):
        return f"<Category {self.name}>"
