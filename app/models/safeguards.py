# app/models/safeguards.py
from app import db
from sqlalchemy import func
from app.utils import utc_to_local

class Safeguard(db.Model):
    __tablename__ = 'safeguards'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.Integer, db.ForeignKey('controls.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    # Use func.now() for both created and updated to automatically set timestamps
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # Default func.now()
    archived = db.Column(db.DateTime, nullable=True)  # Nullable, set when the safeguard is archived (for soft deletes)

    control = db.relationship('Control', backref=db.backref('safeguards', lazy=True))

    def __repr__(self):
        return f'<ControlSafeguard {self.name}>'
    
    @property
    def created_local(self):
        return utc_to_local(self.created)
    
    @property
    def updated_local(self):
        return utc_to_local(self.updated)
    
    @property
    def archived_local(self):
        return utc_to_local(self.archived)