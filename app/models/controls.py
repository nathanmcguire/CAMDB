from datetime import datetime, timezone
from app import db

class Control(db.Model):
    __tablename__ = 'controls'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # New datetime fields with UTC timezone
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Automatically set to UTC when created
    updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))  # Automatically updated to UTC when modified
    deleted = db.Column(db.DateTime, nullable=True)  # Nullable, set when the asset is deleted

    def __repr__(self):
        return f'<Control {self.name}>'
