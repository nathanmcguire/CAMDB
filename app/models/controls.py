from app import db
from sqlalchemy import func
from app.utils import utc_to_local

class Control(db.Model):
    __tablename__ = 'controls'  # Explicitly define the table name
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=True)  # Control number as a string
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)  # Control description
    framework_id = db.Column(db.Integer, db.ForeignKey('control_frameworks.id'), nullable=False)
    
    # Use func.now() for both created and updated to automatically set timestamps
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # Default func.now()
    archived = db.Column(db.DateTime, nullable=True)  # Nullable, set when the asset is archived (for soft deletes)

    # Relationship with control framework
    framework = db.relationship('ControlFramework', backref=db.backref('controls', lazy=True))

    def __repr__(self):
        return f'<Control {self.name}>'
    
    @property
    def created_local(self):
        return utc_to_local(self.created)
    
    @property
    def updated_local(self):
        return utc_to_local(self.updated)
    
    @property
    def archived_local(self):
        return utc_to_local(self.archived)