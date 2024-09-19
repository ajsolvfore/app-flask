from sqlalchemy.dialects.postgresql import UUID
from src import db
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)  # Store hashed password

    def __repr__(self):
        return f'<User {self.name}>'

    # Method to convert the model instance to a dictionary
    def as_dict(self):
        return {
            'id': str(self.id),  # Convert UUID to string for JSON serialization
            'name': self.name,
            'email': self.email
        }
