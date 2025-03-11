from app import db
from sqlalchemy import func

class SecurityFunction(db.Model):
    __tablename__ = 'security_functions'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    # Use func.now() for both created and updated to automatically set timestamps
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # Default func.now()

    def __repr__(self):
        return f'<SecurityFunction {self.name}>'