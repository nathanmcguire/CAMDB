# app/models/safeguards.py
from app import db
from sqlalchemy import func
from app.utils import utc_to_local

class Safeguard(db.Model):
    __tablename__ = 'safeguards'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=True)  # Safeguard number as a string
    control_id = db.Column(db.Integer, db.ForeignKey('controls.id'), nullable=False)
    security_function_id = db.Column(db.Integer, db.ForeignKey('security_functions.id'), nullable=True)
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_types.id'), nullable=True)
    implementation_group_id = db.Column(db.Integer, db.ForeignKey('implementation_groups.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    # Use func.now() for both created and updated to automatically set timestamps
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # Default func.now()
    archived = db.Column(db.DateTime, nullable=True)  # Nullable, set when the safeguard is archived (for soft deletes)

    control = db.relationship('Control', backref=db.backref('safeguards', lazy=True))
    security_function = db.relationship('SecurityFunction', backref=db.backref('safeguards', lazy=True))
    asset_type = db.relationship('AssetType', backref=db.backref('safeguards', lazy=True))
    implementation_group = db.relationship('ImplementationGroup', backref=db.backref('safeguards', lazy=True))

    def __repr__(self):
        return f'<Safeguard {self.name}>'
    
    @property
    def created_local(self):
        return utc_to_local(self.created)
    
    @property
    def updated_local(self):
        return utc_to_local(self.updated)
    
    @property
    def archived_local(self):
        return utc_to_local(self.archived)